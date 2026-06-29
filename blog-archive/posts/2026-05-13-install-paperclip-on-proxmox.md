---
title: "How to Install Paperclip on Proxmox (with Tailscale or Cloudflare Tunnel)"
date: "2026-05-13T18:09:24"
modified: "2026-05-14T00:46:46"
slug: "install-paperclip-on-proxmox"
original_url: "https://adityarajsingh.com/install-paperclip-on-proxmox/"
categories: ["Homelab"]
tags: ["Proxmox"]
excerpt: "Paperclip is a self-hosted AI workforce platform — you set up a \"company\", define agents, and assign them tasks. It's still in active development on the ProxmoxVED (dev) repo, so don't trust it with real data yet. Here's how I got it running on Proxmox and reachable remotely. I'll cover two ways to expose it: Tailscale (private, recommended) […]"
---

# How to Install Paperclip on Proxmox (with Tailscale or Cloudflare Tunnel)

<a href="https://github.com/paperclipai/paperclip" target="_blank" rel="noreferrer noopener">Paperclip</a> is a self-hosted AI workforce platform — you set up a "company", define agents, and assign them tasks. It's still in active development on the <a href="https://github.com/community-scripts/ProxmoxVED" target="_blank" rel="noreferrer noopener">ProxmoxVED</a> (dev) repo, so don't trust it with real data yet.

Here's how I got it running on Proxmox and reachable remotely. I'll cover two ways to expose it: Tailscale (private, recommended) and Cloudflare Tunnel (public URL with optional auth).

## Create the LXC Container

SSH into your Proxmox host and run the community-scripts ProxmoxVED installer:

``` wp-block-code
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVED/main/ct/paperclip.sh)"
```

It spins up a Debian 13 LXC, installs Postgres and Node, and prints a bootstrap invite URL like:

``` wp-block-code
http://<lan-ip>:3100/invite/pcp_bootstrap_<token>
```

Note the container ID (dummy id for this blog 000). If you're on the same LAN, open that URL and skip ahead to onboarding. If you're remote, keep reading.

## Install Tailscale Inside the Container

I installed Tailscale inside the LXC instead of on the Proxmox host. Safer if anything breaks — no subnet routes, no host-level networking changes.

Enter the container and install:

``` wp-block-code
pct enter 000
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
```

It will fail with:

``` wp-block-code
is CONFIG_TUN enabled in your kernel? `modprobe tun` failed
```

Unprivileged LXCs don't have `/dev/net/tun` by default. Need to expose it from the host.

### Expose TUN to the Container

Exit back to the Proxmox host and append two lines to the container's config:

``` wp-block-code
cat >> /etc/pve/lxc/000.conf <<EOF
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net/tun dev/net/tun none bind,create=file
EOF
```

Reboot the container:

``` wp-block-code
pct reboot 000
```

Re-enter and confirm TUN is now visible:

``` wp-block-code
pct enter 000
ls -la /dev/net/tun
tailscale up
```

You'll get an auth URL. Log in, and the container picks up a Tailscale IP like `100.x.x.x`. Grab it with:

``` wp-block-code
tailscale ip -4
```

## First-Time Access (the Hostname Allowlist Trap)

Paperclip enforces a strict hostname allowlist. The installer bakes `PAPERCLIP_PUBLIC_URL=http://<lan-ip>:3100` into `/opt/paperclip/.env`, so the bootstrap invite URL only accepts requests from that LAN IP. Hit it via the Tailscale IP and you get:

``` wp-block-code
Hostname '<tailscale-ip>' is not allowed for this Paperclip instance.
```

Swap the public URL to your Tailscale IP and restart:

``` wp-block-code
sed -i 's|PAPERCLIP_PUBLIC_URL=http://<lan-ip>:3100|PAPERCLIP_PUBLIC_URL=http://<tailscale-ip>:3100|' /opt/paperclip/.env
systemctl restart paperclip
```

Now open the invite URL with the Tailscale IP from your laptop:

``` wp-block-code
http://<tailscale-ip>:3100/invite/pcp_bootstrap_<token>
```

Complete admin onboarding in the browser.

## Add the Hostnames You Actually Want

After onboarding, the CLI works — but it won't find the config unless you load the env first:

``` wp-block-code
cd /opt/paperclip
set -a; source /opt/paperclip/.env; set +a
pnpm paperclipai allowed-hostname <tailscale-ip>
systemctl restart paperclip
```

Confirm the allowlist:

``` wp-block-code
cat /opt/paperclip-data/instances/default/config.json
```

You should see your hostnames under `server.allowedHostnames`.

At this point Paperclip is fully working over Tailscale at `http://<tailscale-ip>:3100`. If you're happy hitting it via IP from your tailnet devices, you're done. If you want a clean URL, pick one of the next two options.

## Option A: Pretty URL Over Tailscale (Private, Recommended)

Stays inside your tailnet. Zero public exposure. Best for personal use.

Pick any domain you control. In your DNS provider, add an `A` record for `paperclip.your-domain.com` pointing to your Tailscale IP (`100.x.x.x`). If your DNS provider is Cloudflare, set the record to **DNS only** (grey cloud) — never proxy a private IP through Cloudflare's edge.

Add the hostname to Paperclip's allowlist and update the public URL:

``` wp-block-code
cd /opt/paperclip
set -a; source /opt/paperclip/.env; set +a
pnpm paperclipai allowed-hostname paperclip.your-domain.com
sed -i 's|PAPERCLIP_PUBLIC_URL=http://<tailscale-ip>:3100|PAPERCLIP_PUBLIC_URL=http://paperclip.your-domain.com:3100|' /opt/paperclip/.env
systemctl restart paperclip
```

Now `http://paperclip.your-domain.com:3100` resolves to your Tailscale IP and only works when you're on the tailnet. To anyone off your tailnet, the URL points to a private IP that goes nowhere.

If you want HTTPS and no port number, run <a href="https://tailscale.com/kb/1242/tailscale-serve" class="ek-link" target="_blank" rel="noreferrer noopener">Tailscale Serve</a> inside the container:

``` wp-block-code
tailscale serve --bg --https=443 http://localhost:3100
```

Then point a CNAME at `paperclip.<your-tailnet>.ts.net`. Cleanest setup for tailnet-only access.

## Option B: Pretty URL Over Cloudflare Tunnel (Public, Optionally Gated)

Public URL on the internet. Use this if you want to access Paperclip from a device that's not on your tailnet, or share with a non-tailnet collaborator.

Install `cloudflared` on the Paperclip container (or any device that can reach it):

``` wp-block-code
curl -fsSL https://pkg.cloudflare.com/install.sh | sh
apt install cloudflared
cloudflared tunnel login
```

Create a tunnel and route a hostname through it. In the Cloudflare dashboard, go to **Zero Trust → Networks → Tunnels → \[your tunnel\] → Public Hostnames** and add:

- Subdomain: `paperclip`
- Domain: `your-domain.com`
- Type: `HTTP`
- URL: `localhost:3100` (if cloudflared runs in the same container) or `<lan-ip>:3100` / `<tailscale-ip>:3100` from wherever cloudflared is running

Update Paperclip's allowlist and public URL to match:

``` wp-block-code
cd /opt/paperclip
set -a; source /opt/paperclip/.env; set +a
pnpm paperclipai allowed-hostname paperclip.your-domain.com
sed -i 's|PAPERCLIP_PUBLIC_URL=http://<tailscale-ip>:3100|PAPERCLIP_PUBLIC_URL=https://paperclip.your-domain.com|' /opt/paperclip/.env
systemctl restart paperclip
```

Open `https://paperclip.your-domain.com`. Clean URL, valid cert, no port number, Cloudflare's edge in front.

**Heads up: this puts Paperclip's login page on the public internet.** Anyone who knows the URL can hit it. I'd strongly recommend layering Cloudflare Access on top — free for up to 50 users:

In **Zero Trust → Access → Applications → Add → Self-hosted**, add `paperclip.your-domain.com` and create a policy like "Emails → equals → your-email@example.com". Now Cloudflare requires Google/email auth before Paperclip's login is even reachable.

## Done

You have Paperclip running on Proxmox, accessible the way you want it. Personal use → Option A. Shared use → Option B with Cloudflare Access.

Paperclip's repo is at <a href="https://github.com/paperclipai/paperclip" target="_blank" rel="noreferrer noopener">github.com/paperclipai/paperclip</a>. It moves fast, so expect the install to drift a bit from this guide over the next few weeks.
