---
title: "How to Mount Disks to OpenMediaVault in Proxmox"
date: "2025-05-26T13:26:24"
modified: "2025-05-28T22:32:32"
slug: "mount-disks-to-omv-in-proxmox"
original_url: "https://adityarajsingh.com/mount-disks-to-omv-in-proxmox/"
categories: ["Homelab"]
tags: ["OpenMediaVault", "Proxmox"]
excerpt: "Once you’ve created your OMV virtual machine in Proxmox, the next step is to pass your physical hard drives (HDDs) through to the VM so OMV can use them for storage. If you're still deciding whether to handle RAID in OMV or at the Proxmox level using ZFS, I covered the pros and cons in […]"
---

# How to Mount Disks to OpenMediaVault in Proxmox

Once you’ve created your OMV virtual machine in Proxmox, the next step is to pass your physical hard drives (HDDs) through to the VM so OMV can use them for storage.

*If you're still deciding whether to handle RAID in OMV or at the Proxmox level using ZFS, I covered the pros and cons <a href="https://adityarajsingh.com/openmediavault-or-proxmox-raid/" class="ek-link">in this post</a>.*

## Verify That Your HDDs Are Detected in Proxmox

1.  In the Proxmox web interface, navigate to: **Node \> Disks**
2.  Ensure all your HDDs are visible here.

## Identify the Disk IDs via Proxmox Shell

Open the Proxmox shell and run:

``` wp-block-code
ls /dev/disk/by-id
```

You’ll see a list of drives similar to this:

**ata-WDC_MODELID_WD-XXXXXXX**

### Match Disk IDs to Actual Drives

Head back to **Proxmox \> Disks** and cross-reference the IDs you found to confirm which physical drive each one represents.

## Pass the Drives Through to the OMV VM

Now, we’ll attach the drives to your OMV VM using Proxmox’s qm set command.

**Note:** If your OMV system disk uses sata0 or scsi0, begin attaching additional drives from sata1 or scsi1. I personally prefer SATA over SCSI for better compatibility with OMV.

For example, assuming you’re using SATA and your OMV VM ID is 108:

``` wp-block-code
qm set 108 -sata1 /dev/disk/by-id/ata-WDC_MODELID_WD-XXXXXXX
```

And if you're listing multiple drives:

``` wp-block-code
qm set 108 -sata2 /dev/disk/by-id/ata-ST4000DM000_MODELID_Z4XXXXXXX
qm set 108 -sata3 /dev/disk/by-id/ata-HGST_MODELID_PKXXXXXXX
```

## Confirm Disks Are Attached in OMV

Go to your OMV VM:

1.  In Proxmox: **OMV VM \> Hardware**
2.  Check that the drives are now listed as attached SATA or SCSI devices.
3.  Boot into OMV and check **Storage \> Disks** to verify they’re visible to OMV as well.

That’s it!
