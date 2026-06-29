---
title: "How To Install Orbital Sync (2 Pi-hole Sync)"
date: "2025-02-01T22:10:55"
modified: "2025-05-31T14:03:57"
slug: "how-to-install-orbital-sync"
original_url: "https://adityarajsingh.com/how-to-install-orbital-sync/"
categories: ["Homelab"]
excerpt: "NOTE: Orbital Sync was archived on Mar 31, 2025. See the announcement here. To use Orbital Sync, you'll need two (or more) Pi-holes. Make sure they are set up first. Orbital Sync runs on Docker Compose, so you'll need to install Docker and Docker Compose on your PRIMARY PI (your main DNS). We will only […]"
---

# How To Install Orbital Sync (2 Pi-hole Sync)

<span class="mark has-inline-color has-black-color" style="background-color:#fcb900">**NOTE:** Orbital Sync was archived on Mar 31, 2025. See the announcement <a href="https://github.com/mattwebbio/orbital-sync/issues/190#issuecomment-2766470506" class="ek-link" aria-label="here (opens in a new tab)" target="_blank" rel="noreferrer noopener">here</a>.</span>

To use Orbital Sync, you'll need two (or more) Pi-holes. Make sure they are set up first.

Orbital Sync runs on Docker Compose, so you'll need to install Docker and Docker Compose on your PRIMARY PI (your main DNS).

We will only make changes on the primary Pi.

SSH into your primary Pi and follow the instructions below.

## Update and Upgrade Your Pi

Make sure your pi is updated. Run this command to update and upgrade:

``` wp-block-code
sudo apt-get update && sudo apt-get upgrade
```

## Install Docker

Next, install Docker. Use Docker's official install script by running:

``` wp-block-code
curl -fsSL test.docker.com -o get-docker.sh && sh get-docker.sh
```

Add user to the 'docker' group (replace 'pi' with your username)

``` wp-block-code
sudo usermod -aG docker pi
```

Verify docker installation:

``` wp-block-code
docker --version
```

## Install Docker Compose

To install Docker Compose on a Raspberry Pi, you need a slightly different method because the Pi uses ARM architecture.

Install required dependencies:

``` wp-block-code
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip
```

Then, install Docker-Compose with:

``` wp-block-code
sudo apt install docker-compose
```

To check if Docker Compose is installed, run this:

``` wp-block-code
docker-compose --version
```

## Install Orbital Sync

Create a directory where you'll store the Orbital Sync and navigate to that location using the following command:

``` wp-block-code
mkdir -p ~/orbital-sync && cd ~/orbital-sync
```

### Create the docker-compose.yml

Create the docker-compose.yml file using nano:

``` wp-block-code
nano docker-compose.yml
```

### orbital-sync docker-compose file

Replace 9.9.9.9 with your primary Pi’s IP address and 1.1.1.1 with your secondary Pi’s IP address. Then, add the web interface password for both in the HOST PASSWORD fields.

``` wp-block-code
services:
  orbital-sync:
    image: mattwebbio/orbital-sync:1
    environment:
      PRIMARY_HOST_BASE_URL: 'http://9.9.9.9'
      PRIMARY_HOST_PASSWORD: 'your_password1'
      SECONDARY_HOSTS_1_BASE_URL: 'http://1.1.1.1'
      SECONDARY_HOSTS_1_PASSWORD: 'your_password2'
      INTERVAL_MINUTES: 60
```

I've slightly modified the docker-compose file, but you can check the original one <a href="https://github.com/mattwebbio/orbital-sync?tab=readme-ov-file#docker" class="ek-link">here</a>.

### Start the Docker Container

``` wp-block-code
docker compose up -d
```

This will pull the Orbital Sync Docker image and start the container in detached mode, meaning it will run in the background.

## Verify It's Running

``` wp-block-code
docker ps
```

You should see a container named orbital-sync in the output.

For any help related to orbital sync, check out the GitHub repo <a href="https://github.com/mattwebbio/orbital-sync" class="ek-link">here</a>.
