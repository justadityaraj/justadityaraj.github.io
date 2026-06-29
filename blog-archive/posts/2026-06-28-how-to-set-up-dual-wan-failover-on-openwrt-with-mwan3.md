---
title: "How to Set Up Dual-WAN Failover on OpenWrt with mwan3"
date: "2026-06-28T23:48:44"
modified: "2026-06-28T23:57:07"
slug: "how-to-set-up-dual-wan-failover-on-openwrt-with-mwan3"
original_url: "https://adityarajsingh.com/how-to-set-up-dual-wan-failover-on-openwrt-with-mwan3/"
categories: ["Homelab"]
tags: ["OpenWrt"]
excerpt: "mwan3 is OpenWrt's built-in multi-WAN package. It watches two (or more) internet lines and auto-switches traffic to the backup when the primary drops, no second box required. This post is exactly how I wired two ISP connections into one OpenWrt router and got automatic failover live, including every gotcha that made mwan3 status lie to me before […]"
---

# How to Set Up Dual-WAN Failover on OpenWrt with mwan3

mwan3 is OpenWrt's built-in multi-WAN package. It watches two (or more) internet lines and auto-switches traffic to the backup when the primary drops, no second box required. This post is exactly how I wired two ISP connections into one OpenWrt router and got automatic failover live, including every gotcha that made `mwan3 status` lie to me before it worked.

Heads up before you start: I run this in **pure failover** mode, where one line carries everything and the other is hot standby. That's the safe default. No IP-hopping, so banking, captchas and VoIP don't break. Load-balancing across both lines is a separate, fussier job and I'll flag where it diverges.

All IPs, ISP names and tokens below are placeholders. Swap in your own.

## My Setup

Two lines, one OpenWrt router doing the failover:

- **ISP-A**, the faster line (say 200 Mbps), comes in through the ISP's own router at 192.168.50.1. This is my **primary**.
- **ISP-B**, the slower line (say 100 Mbps), an ONT/modem at 192.168.60.1. This is my **backup**.
- **The OpenWrt router**, a TP-Link Archer C6 (any mwan3-capable OpenWrt box works). Its LAN lives on its own subnet, 192.168.10.0/24, gateway 192.168.10.1.

The one architecture decision worth copying: **put your LAN on a third subnet that neither ISP owns.** ISP-A is `192.168.50.x`, ISP-B is `192.168.60.x`, my LAN is `192.168.10.x`. Both WAN sides only have to differ from the LAN, and now the core network doesn't depend on either ISP's router config. If I swap an ISP tomorrow, the LAN doesn't move.

Port map on the OpenWrt box:

``` wp-block-code
WAN  = ISP-A (primary)
LAN1 = ISP-B  (reassigned to a second WAN, "wanb")
LAN2 = desktop (static IP, my management lifeline)
LAN3 = switch / homelab
LAN4 = spare
```

## Step 1: Wire Both Lines In

ISP-A's ethernet goes into the OpenWrt **WAN** port. ISP-B's ethernet goes into a **LAN** port (I used LAN1) that we're about to convert into a second WAN. Your LAN switch/homelab hangs off another LAN port.

Before touching anything, give your desktop a **static IP on the LAN** (mine is `192.168.10.76`, gateway `192.168.10.1`). This is your lifeline. You're about to change DHCP and subnets, and a static box means a botched step never locks you out of the router. Plug it straight into a LAN port.

## Step 2: Turn a LAN Port Into a Second WAN

By default LAN1 is part of the `br-lan` bridge. Pull it out and make it its own WAN interface (`wanb`) pulling DHCP from ISP-B. Over SSH (`ssh root@192.168.10.1`):

``` wp-block-code
uci del_list network.@bridge-vlan[0].ports='lan1'   # remove lan1 from the LAN bridge (port name varies by device)
uci set network.wanb=interface
uci set network.wanb.proto='dhcp'
uci set network.wanb.device='lan1'
uci commit network
/etc/init.d/network restart
```

A gotcha specific to converting a LAN port: the L3 device for `wanb` is the physical port (`lan1`), not an interface called `wanb`. So when you check it later, use `ifstatus wanb`. Running `ip addr show wanb` will show you nothing and make you think it's dead.

Confirm both WANs have leases:

``` wp-block-code
ifstatus wan  | grep -o '"address": *"[^"]*"'   # ISP-A, e.g. 192.168.50.x
ifstatus wanb | grep -o '"address": *"[^"]*"'   # ISP-B, e.g. 192.168.60.x
```

If `wanb` has no address, the port name in the `del_list` step was wrong for your device. Check `swconfig dev switch0 show` or the LuCI Switch page for the real label.

## Step 3: Set the LAN Subnet and DHCP

Move the LAN onto its own subnet and set a DHCP pool that won't collide with your static homelab boxes:

``` wp-block-code
uci set network.lan.ipaddr='192.168.10.1'
uci set network.lan.netmask='255.255.255.0'
uci set dhcp.lan.start='200'      # pool 192.168.10.200 to .250, keeps statics below .200 safe
uci set dhcp.lan.limit='50'
uci commit
/etc/init.d/network restart
```

Reconnect at `http://192.168.10.1`. If your homelab boxes use device-set static IPs (mine do), re-IP them to the new subnet. Keep the last octet, just change the third one. That's a separate job. For failover itself you only need the router and your lifeline desktop reachable.

## Step 4: Turn On Flow Offloading

A cheap MediaTek SoC will choke trying to NAT ~200 Mbps in software. Enable hardware/software flow offloading first or your "working" failover will feel like dial-up:

``` wp-block-code
uci set firewall.@defaults[0].flow_offloading='1'
uci commit firewall
/etc/init.d/firewall restart
```

## Step 5: Install <a href="https://openwrt.org/docs/guide-user/network/wan/multiwan/mwan3" class="ek-link">mwan3</a>

``` wp-block-code
opkg update
opkg install mwan3 luci-app-mwan3
```

Now the config. This is the part where everything looks right and `mwan3 status` still reports `wan is error`, so read the traps in the next section *before* you blame your ISP.

Edit `/etc/config/mwan3` to this (failover, ISP-A primary):

``` wp-block-code
config interface 'wan'          # ISP-A (primary)
    option enabled '1'
    list track_ip '8.8.8.8'
    list track_ip '8.8.4.4'
    option reliability '1'
    option count '1'
    option timeout '2'
    option interval '5'
    option down '3'
    option up '3'

config interface 'wanb'         # ISP-B (backup)
    option enabled '1'
    list track_ip '1.1.1.1'
    list track_ip '9.9.9.9'
    option reliability '1'
    option count '1'
    option timeout '2'
    option interval '5'
    option down '3'
    option up '3'

config member 'isp_a_primary'
    option interface 'wan'
    option metric '1'

config member 'isp_b_backup'
    option interface 'wanb'
    option metric '2'

config policy 'failover'
    list use_member 'isp_a_primary'
    list use_member 'isp_b_backup'

config rule 'default'
    option dest_ip '0.0.0.0/0'
    option use_policy 'failover'
```

Lower member metric wins, so ISP-A carries everything. If its health check fails, all traffic moves to ISP-B, and when ISP-A comes back, traffic fails back.

``` wp-block-code
/etc/init.d/mwan3 restart
mwan3 status
```

Success looks like this, both interfaces `online (tracking active)` and the policy showing your primary at 100%:

``` wp-block-code
interface wan is online ...
interface wanb is online ...
Policy failover:
 wan (100%)
```

## The mwan3 Trap (why it says "error" when the line is fine)

I lost two rounds of debugging to these. If `mwan3 status` shows a working line as `error`, it's almost always one of three things.

**1. Each WAN needs a UNIQUE network metric.** Not the mwan3 member metric, the one in `/etc/config/network`. If both default routes are metric 0, mwan3 can't tell them apart and flags one as error:

``` wp-block-code
uci set network.wan.metric='10'
uci set network.wanb.metric='20'
uci commit network
/etc/init.d/network restart
```

**2. Track IPs must not overlap between the two WANs.** I had `1.1.1.1` on both, and ISP-A kept tracking as error because the health probes got tangled. Give each line its own targets (note the config above: `wan` uses `8.8.8.8`/`8.8.4.4`, `wanb` uses `1.1.1.1`/`9.9.9.9`).

**3. Commit before you reboot.** Staged `uci` changes live in RAM. Reboot before `uci commit` and they vanish silently, and you'll swear you set something you didn't. Always:

``` wp-block-code
uci commit
uci get network.wan.metric    # verify it actually stuck
```

then apply with `reload_config` or a reboot.

One more, if your primary is behind the ISP's own router (mine is, and it's CGNAT): the OpenWrt WAN pulls a private `192.168.50.x` lease from that router, which is double-NAT. That's **fine for failover**. Outbound traffic and outbound tunnels don't care. It only costs you inbound port-forwarding on that line, which I'll touch on at the end.

## Step 6: Test It Both Ways

Don't trust failover you haven't pulled the plug on. Test in both directions:

``` wp-block-code
mwan3 status            # baseline: failover: wan (100%)
```

- **Pull ISP-A's cable.** Within ~5 to 15s, `mwan3 status` should flip to `wanb`, and a `ping 1.1.1.1` from a LAN box keeps running after a brief blip. Existing sessions (SSH, calls, VPN) reconnect because the public IP changed. Plain web browsing just continues.
- **Plug ISP-A back in.** It fails back to `wan` automatically.
- **Pull ISP-B instead.** Nothing should change. You were on ISP-A anyway.

If anything misbehaves, `mwan3 stop` instantly reverts the box to plain single-line routing while you debug. A useful panic button to know.

## Bonus: See Each Line's Uptime Independently

Here's the catch with failover working *too* well: when ISP-A dies, the house stays online via ISP-B, so you never notice ISP-A was down. If you want to actually hold your ISP accountable, you need per-line monitoring.

You can't just point Uptime Kuma at `1.1.1.1`. It's behind the router and only ever sees "internet up" via whichever line mwan3 picked. The fix is to relay mwan3's per-line health to two Kuma **Push** monitors.

In Kuma, create two Push monitors (`ISP-A`, `ISP-B`), Heartbeat Interval **120s**, and copy each push token. Then a script on the OpenWrt box, `/root/kuma-wan-push.sh`:

``` wp-block-code
#!/bin/sh
# relay per-WAN mwan3 health to Uptime Kuma push monitors
KUMA="http://<kuma-ip>:3001/api/push"
A_TOKEN="PASTE_ISP_A_TOKEN"
B_TOKEN="PASTE_ISP_B_TOKEN"

S=$(mwan3 status)
echo "$S" | grep -q "interface wan is online" \
  && wget -q -O /dev/null "$KUMA/$A_TOKEN?status=up&msg=online" \
  || wget -q -O /dev/null "$KUMA/$A_TOKEN?status=down&msg=offline"
echo "$S" | grep -q "interface wanb is online" \
  && wget -q -O /dev/null "$KUMA/$B_TOKEN?status=up&msg=online" \
  || wget -q -O /dev/null "$KUMA/$B_TOKEN?status=down&msg=offline"
```

Run it every minute:

``` wp-block-code
echo '* * * * * /root/kuma-wan-push.sh' >> /etc/crontabs/root
/etc/init.d/cron enable
/etc/init.d/cron restart
```

A small thing that bit me: `grep "interface wan is online"` does NOT false-match `wanb`. The next character is `b`, not a space, so the pattern is safe. The script pushes `down` (not just a missing heartbeat) when a line is offline, so a dead line goes red immediately instead of waiting for the heartbeat to lapse. Wire Slack/Pushover notifications on both monitors and you get a ping the moment either line drops, even though the house never noticed.

## A Few Things I Deliberately Skipped

**Load-balancing both lines.** Tempting, but it splits connections across both public IPs, which breaks banking sessions, some logins and captchas unless you add stickiness rules. Pure failover has none of that. I'll graduate to it later, not on day one.

**Bridge mode on the backup ONT** to kill its double-NAT. It's a later optimization. Failover works fine double-NATted. Only worth it if you need inbound port-forwarding on that line.

**Inbound services.** Because my primary is CGNAT, I can't port-forward on it at all. Anything I expose goes through Cloudflare Tunnel instead. It's outbound, so it's WAN-independent and survives failover for free. If you rely on port-forwards, pin them to whichever line has a real public IP.

**Power.** Half of "ISP downtime" is actually a power blip rebooting your gear. Put the ONT, the ISP routers, the switch and the OpenWrt box on one UPS or the whole exercise is pointless.

## Done

That's automatic dual-WAN failover on a single OpenWrt box. Primary carries everything, backup takes over in seconds when it drops, and you get a per-line alert so you actually know it happened. Start in pure failover like I did. It's the version that just works without breaking your banking app. The mwan3 docs cover load-balancing when you're ready to push your luck.
