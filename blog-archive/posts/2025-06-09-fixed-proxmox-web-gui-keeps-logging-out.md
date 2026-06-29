---
title: "FIXED - Proxmox Web GUI Keeps Logging Out"
date: "2025-06-09T12:40:36"
modified: "2025-06-09T12:40:37"
slug: "fixed-proxmox-web-gui-keeps-logging-out"
original_url: "https://adityarajsingh.com/fixed-proxmox-web-gui-keeps-logging-out/"
categories: ["Homelab"]
tags: ["Proxmox"]
excerpt: "Proxmox relies on accurate system time to manage sessions properly. If your network blocks NTP (like mine does), here’s a quick fix to avoid web GUI session timeout. Make sure your hardware clock is correct, run this in your pve node shell. Ensure system time is in sync with it: Run these two commands to […]"
---

# FIXED - Proxmox Web GUI Keeps Logging Out

Proxmox relies on accurate system time to manage sessions properly.

If your network blocks NTP (like mine does), here’s a quick fix to avoid web GUI session timeout.

Make sure your hardware clock is correct, run this in your pve node shell.

``` wp-block-code
hwclock
```

Ensure system time is in sync with it:

``` wp-block-code
date
```

Run these two commands to reset auth keys:

``` wp-block-code
touch /etc/pve/authkey.pub
touch /etc/pve/authkey.pub.old
```

That’s it, your session issues should be resolved.
