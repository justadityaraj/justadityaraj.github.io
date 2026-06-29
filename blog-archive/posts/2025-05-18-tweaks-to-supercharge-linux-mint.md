---
title: "4 Advanced Tweaks to Supercharge Linux Mint"
date: "2025-05-18T22:14:56"
modified: "2025-05-27T04:04:07"
slug: "tweaks-to-supercharge-linux-mint"
original_url: "https://adityarajsingh.com/tweaks-to-supercharge-linux-mint/"
categories: ["Productivity"]
tags: ["Linux Mint"]
excerpt: "Changing themes, icons, or fonts are fun, but they don’t really improve how the system works. Instead, Iet's focus on tweaks that make Linux Mint faster, smoother, and more secure. These are not usually found in beginner guides, but they’ve made a big difference for me. 1. Turn on zswap When your RAM is full, […]"
---

# 4 Advanced Tweaks to Supercharge Linux Mint

Changing themes, icons, or fonts are fun, but they don’t really improve how the system works. Instead, Iet's focus on tweaks that make Linux Mint faster, smoother, and more secure.

These are not usually found in beginner guides, but they’ve made a big difference for me.

## 1. Turn on zswap

When your RAM is full, Linux uses swap space on the disk, which is much slower.

zswap helps by compressing memory before it gets written to disk, which keeps things running more smoothly. This is useful on systems with limited RAM and also helps avoid slowdowns when multitasking or running heavy apps.

<a href="https://easylinuxtipsproject.blogspot.com/p/speed-mint.html#ID1.1" class="ek-link" target="_blank" aria-label="Here&#39;s a great zswap guide. (opens in a new tab)" rel="noreferrer noopener">Here's a great zswap guide.</a>

## 2. Mount /tmp as tmpfs

<a href="https://docs.kernel.org/filesystems/tmpfs.html" class="ek-link">Tmpfs</a> tells Linux to store temporary files in RAM instead of the disk. Since these files are short-lived and not that important, using RAM makes access faster and reduces wear on SSDs. It’s a simple change that helps apps open quicker and keeps the system snappy - especially if you have 8GB of RAM or more.

## 3. Enable UFW Firewall

Linux is already secure, but having a basic firewall is just a smart idea. UFW (Uncomplicated Firewall) quietly blocks unwanted network connections in the background.

## 4. Switch to Fish Shell

The default terminal shell works fine, but <a href="https://fishshell.com/" class="ek-link">Fish Shell</a> is way more user-friendly.

It gives real-time command suggestions, highlights mistakes, and generally makes working in the terminal easier and more pleasant.I get more done and make fewer typos, and it just feels more modern than the usual bash shell.

These tweaks aren’t about looks - they’re about **making Linux Mint run better** from day one. If you haven’t tried them yet, give them a shot.
