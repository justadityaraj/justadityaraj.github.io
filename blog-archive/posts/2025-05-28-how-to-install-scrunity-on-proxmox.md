---
title: "How to Install Scrunity on Proxmox"
date: "2025-05-28T20:44:30"
modified: "2025-05-30T14:31:42"
slug: "how-to-install-scrunity-on-proxmox"
original_url: "https://adityarajsingh.com/how-to-install-scrunity-on-proxmox/"
categories: ["Homelab"]
tags: ["Proxmox"]
excerpt: "Scrutiny (S.M.A.R.T Monitoring) runs on Docker Compose. You can install Docker and Compose manually or use Dockge LXC (recommended). Install Scrutiny Paste the following into docker-compose.yml, change the TZ to your local timezone. Save the compose file. Start Scrutiny Scrutiny will be available on port 8080. Collector Script on Proxmox Node Head over to Proxmox […]"
featured_image: "../images/818-featured.png"
---

# How to Install Scrunity on Proxmox

<a href="https://github.com/AnalogJ/scrutiny" class="ek-link" aria-label="Scrutiny (opens in a new tab)" target="_blank" rel="noreferrer noopener">Scrutiny</a> (S.M.A.R.T Monitoring) runs on Docker Compose. You can install Docker and Compose manually or use <a href="https://github.com/louislam/dockge" class="ek-link" aria-label="Dockge (opens in a new tab)" target="_blank" rel="noreferrer noopener">Dockge</a> LXC (recommended).

## Install Scrutiny

``` wp-block-code
mkdir -p /opt/scrutiny/{influxdb,config} && cd /opt/scrutiny
nano docker-compose.yml
```

Paste the following into docker-compose.yml, change the TZ to your local timezone.

``` wp-block-code
version: '2.4'

services:
  scrutiny-influxdb:
    image: influxdb:2.2
    container_name: scrutiny-influxdb
    ports:
      - 8086:8086
    restart: unless-stopped
    volumes:
      - ./influxdb:/var/lib/influxdb2
    environment:
      TZ: Asia/Kolkata # CHANGE THIS
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8086/health"]
      interval: 5s
      timeout: 10s
      retries: 20

  scrutiny-web:
    image: 'ghcr.io/analogj/scrutiny:master-web'
    container_name: scrutiny-web
    ports:
      - 8080:8080
    restart: unless-stopped
    volumes:
      - ./config:/opt/scrutiny/config
    environment:
      SCRUTINY_WEB_INFLUXDB_HOST: scrutiny-influxdb
      TZ: Asia/Kolkata # CHANGE THIS
    depends_on:
      scrutiny-influxdb:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/api/health"]
      interval: 5s
      timeout: 10s
      retries: 20
      start_period: 10s
```

Save the compose file.

### Start Scrutiny

``` wp-block-code
docker-compose up -d
```

Scrutiny will be available on port 8080.

## Collector Script on Proxmox Node

Head over to Proxmox \> Node (e.g., pve) \> Shell, run this:

``` wp-block-code
cd /opt/scrutiny
nano scrutiny-collector-install.sh
```

Paste the following:

**Replace API_ENDPOINT** with your Scrutiny container's IP address.

``` wp-block-code
#!/bin/bash

API_ENDPOINT="http://192.168.XX.XX:8080" # CHANGE THIS

apt install smartmontools -y

INSTALL_DIR="/opt/scrutiny"
BIN_DIR="$INSTALL_DIR/bin"
LATEST_RELEASE_URL=$(curl -s https://api.github.com/repos/AnalogJ/scrutiny/releases/latest | grep "browser_download_url.*scrutiny-collector-metrics-linux-amd64" | cut -d '"' -f 4)

mkdir -p $BIN_DIR
curl -L $LATEST_RELEASE_URL -o $BIN_DIR/scrutiny-collector-metrics-linux-amd64
chmod +x $BIN_DIR/scrutiny-collector-metrics-linux-amd64

mkdir -p /root/scrutiny
cat << EOF > /root/scrutiny/scrutiny.sh
#!/bin/bash
/opt/scrutiny/bin/scrutiny-collector-metrics-linux-amd64 run --api-endpoint "$API_ENDPOINT" 2>&1 | tee /var/log/scrutiny.log
EOF
chmod +x /root/scrutiny/scrutiny.sh

cat << 'EOF' > /etc/systemd/system/scrutiny.service
[Unit]
Description=Scrutiny Collector
Requires=scrutiny.timer

[Service]
Type=simple
ExecStart=/root/scrutiny/scrutiny.sh
User=root
EOF

cat << 'EOF' > /etc/systemd/system/scrutiny.timer
[Unit]
Description=Timer for the scrutiny.service

[Timer]
Unit=scrutiny.service
OnBootSec=5min
OnUnitActiveSec=60min

[Install]
WantedBy=timers.target
EOF

systemctl enable scrutiny.timer
systemctl start scrutiny.timer
systemctl status scrutiny.timer
```

### Run the Script

``` wp-block-code
chmod +x scrutiny-collector-install.sh
./scrutiny-collector-install.sh
```

Now Scrutiny should be running at http://\<container-ip\>:8080
