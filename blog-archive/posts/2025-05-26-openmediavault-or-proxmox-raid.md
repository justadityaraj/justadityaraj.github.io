---
title: "OpenMediaVault or Proxmox ZFS – Where Should You Set Up RAID?"
date: "2025-05-26T12:44:17"
modified: "2025-05-28T22:32:35"
slug: "openmediavault-or-proxmox-raid"
original_url: "https://adityarajsingh.com/openmediavault-or-proxmox-raid/"
categories: ["Homelab"]
tags: ["OpenMediaVault", "Proxmox"]
excerpt: "I recently went down a little rabbit hole while setting up my homelab, and I thought I’d share what I learned, hopefully, it helps someone else avoid the back-and-forth I went through. So here’s what I was working with: Now the big question was: Should I set up RAID 1 inside OMV, or use a […]"
---

# OpenMediaVault or Proxmox ZFS – Where Should You Set Up RAID?

I recently went down a little rabbit hole while setting up my homelab, and I thought I’d share what I learned, hopefully, it helps someone else avoid the back-and-forth I went through.

So here’s what I was working with:

- I’m running **OpenMediaVault** (OMV) as a VM inside **Proxmox**.
- I have **two HDDs** that I want to use in **RAID 1** (mirror), mainly for storing files.
- I want to access those files using tools like **Immich, Jellyfin**, etc, all running in their own VMs or containers.

Now the big question was: Should I set up RAID 1 inside OMV, or use a ZFS mirror in Proxmox and pass it through to OMV?

I wasn’t looking for anything too complex, just safe, reliable storage that I could access easily across my network.

After doing a bit of research and getting some helpful replies from folks online, here’s what I ended up doing:

## RAID inside OpenMediaVault

**Here’s why:**

**All my storage lives in OMV**, so it made more sense to manage the RAID directly there.

It keeps things simple, no need to mess around with ZFS passthroughs or worry about compatibility between Proxmox and OMV.

To get RAID working, I used the **openmediavault-md** plugin.

It added a "Multiple Device" option under the Storage tab in the OMV web interface. From there, I could easily create a RAID mirror.

Now that you’ve picked OMV for RAID, here’s <a href="https://adityarajsingh.com/mount-disks-to-omv-in-proxmox/" class="ek-link">how to mount disks to OpenMediaVault in Proxmox</a> to get started.

Happy homelabbing!
