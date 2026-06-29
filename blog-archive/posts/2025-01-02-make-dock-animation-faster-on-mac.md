---
title: "Make Dock Animation Faster on Mac"
date: "2025-01-02T02:39:39"
modified: "2025-01-02T02:41:12"
slug: "make-dock-animation-faster-on-mac"
original_url: "https://adityarajsingh.com/make-dock-animation-faster-on-mac/"
categories: ["Productivity"]
tags: ["Mac"]
excerpt: "Tired of waiting for the Dock to appear when you move your mouse? Here's a super quick fix to make the animation snappier! Steps to Speed Up Dock Animation That's all, you can adjust the -float time to increase or decrease the animation. Restore Default Settings Run this if you wish to restore the default […]"
---

# Make Dock Animation Faster on Mac

Tired of waiting for the Dock to appear when you move your mouse? Here's a super quick fix to make the animation snappier!

## Steps to Speed Up Dock Animation

1.  Open Terminal (you can find it in Applications \> Utilities).
2.  Run these commands:

``` wp-block-code
defaults write com.apple.dock autohide-delay -int 0
defaults write com.apple.dock autohide-time-modifier -float 0.40
killall Dock
```

That's all, you can adjust the -float time to increase or decrease the animation.

## Restore Default Settings

Run this if you wish to restore the default settings:

``` wp-block-code
defaults delete com.apple.dock autohide-delay
defaults delete com.apple.dock autohide-time-modifier
killall Dock
```

## How This Works

The first command, **defaults write com.apple.dock autohide-delay -int 0**, removes the delay for the Dock to appear when you move your mouse to its hidden location. By setting the delay to 0, the Dock shows up instantly without any waiting time.

The second command, **defaults write com.apple.dock autohide-time-modifier -float 0.40**, adjusts the speed of the animation when the Dock slides in and out. The **0.40 value** makes the animation faster, but you can tweak this value to make it even quicker or slower, depending on your preference.

The **killall Dock** command restarts the Dock to apply these changes immediately. Without this restart, you would need to log out or reboot your Mac to see the effects.
