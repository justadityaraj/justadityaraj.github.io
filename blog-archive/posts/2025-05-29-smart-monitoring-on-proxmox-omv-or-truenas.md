---
title: "How I Monitor SMART on Proxmox - OMV or TrueNAS"
date: "2025-05-29T01:46:07"
modified: "2025-05-29T01:51:57"
slug: "smart-monitoring-on-proxmox-omv-or-truenas"
original_url: "https://adityarajsingh.com/smart-monitoring-on-proxmox-omv-or-truenas/"
categories: ["Homelab"]
tags: ["OpenMediaVault", "Proxmox"]
excerpt: "I run OpenMediaVault inside a Proxmox VM. It works great for a home NAS, but there was one big issue: S.M.A.R.T. monitoring didn’t work. Here’s what I found and how I fixed it without messing around with SATA controller passthrough. Why SMART Doesn’t Work in OMV (in Proxmox) If you're passing disks to your OMV […]"
featured_image: "../images/840-featured.png"
---

# How I Monitor SMART on Proxmox - OMV or TrueNAS

I run OpenMediaVault inside a Proxmox VM. It works great for a home NAS, but there was one big issue: S.M.A.R.T. monitoring didn’t work.

Here’s what I found and how I fixed it without messing around with SATA controller passthrough.

## Why SMART Doesn’t Work in OMV (in Proxmox)

If you're <a href="https://adityarajsingh.com/mount-disks-to-omv-in-proxmox/" class="ek-link">passing disks to your OMV virtual machine using disk IDs</a>, OMV sees them as virtual drives.

The problem is, these virtual disks don’t carry over any SMART data. So OMV has no way of checking things like drive temperature, health status, or whether the disk is starting to fail.

The only way to get SMART working directly in OMV is to pass through your entire SATA controller to the VM. But that’s a pretty advanced setup. It **can be risky**, especially if the same controller is also being used for the Proxmox system drive or other tasks.

## The Fix: Monitor SMART on the Proxmox Host

Proxmox has full access to the physical drives, so it can read SMART data without any extra configuration.

I tried using the built-in SMART tools that come with Proxmox but they’re not great. The interface is hard to understand, and it’s not something I wanted to check regularly.

### Install Scrutiny on Proxmox

<a href="https://adityarajsingh.com/how-to-install-scrunity-on-proxmox/" class="ek-link">Scrutiny</a> is a modern, web-based tool that shows all the SMART data in a clear and organized way. I installed it in a docker container with it's agent installed directly on the Proxmox host, and now I can check the health of all my drives from the browser.

I’ve already written a separate guide on how to install Scrutiny in Proxmox. You can follow it step-by-step here:

- <a href="https://adityarajsingh.com/how-to-install-scrunity-on-proxmox/" class="ek-link"><em>How to Install Scrutiny in Proxmox – Guide</em></a>

Don’t waste time trying to pass through your SATA controller. It’s not worth the complexity, especially when there’s a much easier option.

Just monitor the disks from the Proxmox host and use Scrutiny. It’s safe, simple, and gives you all the info you need to keep your drives healthy.
