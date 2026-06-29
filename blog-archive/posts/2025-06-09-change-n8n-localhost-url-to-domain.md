---
title: "Change n8n localhost Webhook or OAuth2 URL to Your Domain"
date: "2025-06-09T22:12:10"
modified: "2025-08-17T03:23:56"
slug: "change-n8n-localhost-url-to-domain"
original_url: "https://adityarajsingh.com/change-n8n-localhost-url-to-domain/"
categories: ["Homelab"]
tags: ["n8n", "Proxmox"]
excerpt: "Self-hosting n8n and seeing something like http://localhost:5678/rest/oauth2-credential/callback or similar localhost when you expect your public domain like https://n8n.your-domain.com? Here’s the quick fix. The Solution: Explicit Environment Variables Since I'm running n8n on my Proxmox hypervisor and using Cloudflared Tunnel for the domain, I had to just go to my n8n LXC, and edit the n8n.service […]"
---

# Change n8n localhost Webhook or OAuth2 URL to Your Domain

Self-hosting n8n and seeing something like<span class="mark has-inline-color" style="background-color:#fcb900"> *http://localhost:5678/rest/oauth2-credential/callback* </span>or similar localhost when you expect your public domain like https://n8n.your-domain.com?

Here’s the quick fix.

## The Solution: Explicit Environment Variables

Since I'm running n8n on my <a href="https://adityarajsingh.com/tag/proxmox/" class="ek-link">Proxmox</a> hypervisor and using Cloudflared Tunnel for the domain, I had to just go to my n8n LXC, and edit the n8n.service service from console.

But you should be able to SSH into your n8n server and do the same.

Edit your n8n.service file:

``` wp-block-code
sudo nano /etc/systemd/system/n8n.service
```

Modify the content to include N8N_EXTERNAL_URL, WEBHOOK_URL and N8N_PROTOCOL. Add this anywhere inside of \[Service\].

``` wp-block-code
Environment="N8N_EXTERNAL_URL=https://n8n.yourdomain.com/"
Environment="WEBHOOK_URL=https://n8n.yourdomain.com/"
Environment="N8N_PROTOCOL=https"
```

Save and exit nano, reload and restart systemd configuration.

``` wp-block-code
sudo systemctl daemon-reload
sudo systemctl restart n8n
```

That's it, even tho N8N_EXTERNAL_URL is the primary variable for n8n's external address, being explicit with WEBHOOK_URL and N8N_PROTOCOL can be the key to resolving those stubborn localhost callback issues.
