---
title: "wpa_supplicant.conf for Raspberry Pi"
date: "2025-01-28T20:50:12"
modified: "2025-01-28T20:50:13"
slug: "wpa_supplicant-conf-for-raspberry-pi"
original_url: "https://adityarajsingh.com/wpa_supplicant-conf-for-raspberry-pi/"
categories: ["Homelab"]
excerpt: "This code works. I've tested it with a Raspberry Pi Zero 2 W. That's it!"
---

# wpa_supplicant.conf for Raspberry Pi

This code works. I've tested it with a Raspberry Pi Zero 2 W.

1.  Create a new text file, copy the code from below, paste it, and replace the following:
2.  country= with your country Alpha'a code (e.g., US, IN, list <a href="https://www.iban.com/country-codes" class="ek-link">here</a>).
3.  ssid="your WiFi name" (remove any spaces).
4.  psk="your WiFi password" (remove any spaces).
5.  Save the file, rename it to **wpa_supplicant.conf**, and move it to the root of your freshly installed Pi.

That's it!

``` wp-block-code
country=IN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="yourWifiName"
psk="yourWifiPassword"
key_mgmt=WPA-PSK
}
```
