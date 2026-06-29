---
title: "How To Install Argon Theme on OpenWrt"
date: "2025-01-27T01:27:45"
modified: "2025-01-27T01:29:08"
slug: "how-to-install-argon-theme-on-openwrt"
original_url: "https://adityarajsingh.com/how-to-install-argon-theme-on-openwrt/"
categories: ["Homelab"]
excerpt: "Create a backup before doing any of this, in System > Backup > Download Backup: GENERATE ARCHIVE. Update the list Log into OpenWrt, go to System > Software: UPDATE LISTS. If the update fails, check if you added DNS or not in Interfaces > your interface, e.g., LAN: EDIT > Advanced Settings > Use Custom […]"
---

# How To Install Argon Theme on OpenWrt

Create a backup before doing any of this, in System \> Backup \> Download Backup: GENERATE ARCHIVE.

## Update the list

Log into OpenWrt, go to System \> Software: UPDATE LISTS.

If the update fails, check if you added DNS or not in Interfaces \> your interface, e.g., LAN: EDIT \> Advanced Settings \> Use Custom DNS servers, e.g., 1.1.1.1 - This should fix the failure.

## Install Luci-compat

Search "luci-compat" in the Filter and install it.

## Install Luci-lib-ipkg

Repeat the same for Luci-lib-ipkg.

## Install Argon theme files

Download this config file: <a href="https://github.com/jerrykuku/luci-theme-argon/releases/download/v1.7.2/luci-app-argon-config_0.9-20210309_all.ipk" class="ek-link">luci-app-argon-config_0.9-20210309_all.ipk</a>, then click on UPLOAD PACKAGE next to the update lists and install it.

Repeat the same for this file: <a href="https://github.com/jerrykuku/luci-theme-argon/releases/download/v2.3.1/luci-theme-argon_2.3.1_all.ipk" class="ek-link">luci-theme-argon</a>, or you can try to grab the latest from the GitHub <a href="https://github.com/jerrykuku/luci-theme-argon/" class="ek-link">release page</a> of Argon.

You should be able to see the theme now. If you don't, go to System \> System \> Language and Style \> Design: Argon \> SAVE & APPLY.

## Try other themes

Go to System \> Software \> Filter: and type "theme." You will see a few options that can be installed with just one click. I personally use the <a href="https://openwrt.org/docs/guide-user/luci/luci.themes#material_theme" class="ek-link">Material theme</a>.
