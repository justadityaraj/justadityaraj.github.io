---
title: "Pi-hole v6 NTP Error Fix"
date: "2025-03-15T23:01:20"
modified: "2025-03-15T23:01:20"
slug: "pihole-ntp-error-fix"
original_url: "https://adityarajsingh.com/pihole-ntp-error-fix/"
categories: ["Homelab"]
excerpt: "I upgraded my Pi-hole to V6 and started seeing the error \"No valid NTP replies received, check server and network connectivity\", but fixed it by disabling the NTP. Step 1: Open the Pi-hole Configuration File Run this command to edit the file: Step 2: Disable NTP Find the [ntp] section and make sure it looks […]"
---

# Pi-hole v6 NTP Error Fix

I upgraded my Pi-hole to V6 and started seeing the error "No valid NTP replies received, check server and network connectivity", but fixed it by disabling the NTP.

## Step 1: Open the Pi-hole Configuration File

Run this command to edit the file:

``` wp-block-code
sudo nano /etc/pihole/pihole.toml
```

## Step 2: Disable NTP

Find the \[ntp\] section and make sure it looks like this:

``` wp-block-code
[ntp.ipv4]
# Should FTL act as network time protocol (NTP) server (IPv4)?
active = false

[ntp.ipv6]
# Should FTL act as network time protocol (NTP) server (IPv6)?
active = false

[ntp.sync]
# Should FTL try to synchronize the system time with an upstream NTP server?
active = false
```

## Step 3: Save the File

Press CTRL + X, then Y, and hit Enter to save and exit.

## Step 4: Restart Pi-hole

Now restart the Pi-hole FTL service with this command:

``` wp-block-code
sudo systemctl restart pihole-FTL.service
```

Pi-hole will work fine without its built-in NTP feature as long as your system has another way to sync time. The key is making sure your device’s clock is accurate, so DNS queries and logs don’t get messed up.

Hope it helps!
