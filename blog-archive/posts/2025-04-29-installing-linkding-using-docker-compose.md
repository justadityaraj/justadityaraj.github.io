---
title: "Installing Linkding using Docker Compose"
date: "2025-04-29T00:42:38"
modified: "2025-05-26T12:50:47"
slug: "installing-linkding-using-docker-compose"
original_url: "https://adityarajsingh.com/installing-linkding-using-docker-compose/"
categories: ["Homelab"]
excerpt: "Linkding is a fast, simple, and self-hosted bookmarking service. Let's install it using docker compose. (demo) Step 1: Create a Folder for Linkding Step 2: Create docker-compose.yml Copy the below docker compose file or from the official github repo here. Step 3: Create .env File Copy the below env file or from the official github […]"
---

# Installing Linkding using Docker Compose

<a href="https://linkding.link/" class="ek-link">Linkding</a> is a fast, simple, and self-hosted bookmarking service. Let's install it using docker compose. (<a href="https://demo.linkding.link/login/" class="ek-link">demo</a>)

## Step 1: Create a Folder for Linkding

``` wp-block-code
mkdir ~/linkding
cd ~/linkding
```

## Step 2: Create docker-compose.yml

``` wp-block-code
nano docker-compose.yml
```

Copy the below docker compose file or from the official github repo <a href="https://github.com/sissbruecker/linkding/blob/master/docker-compose.yml" class="ek-link">here</a>.

``` wp-block-code
services:
linkding:
container_name: "linkding"
image: sissbruecker/linkding:latest
ports:
- "${LD_HOST_PORT:-9090}:9090"
volumes:
- "${LD_HOST_DATA_DIR:-./data}:/etc/linkding/data"
env_file:
- .env
restart: unless-stopped
```

## Step 3: Create .env File

``` wp-block-code
nano .env
```

Copy the below env file or from the official github repo <a href="https://github.com/sissbruecker/linkding/blob/master/.env.sample" class="ek-link">here</a>.

``` wp-block-code
# Docker container name
LD_CONTAINER_NAME=linkding
# Port on the host system that the application should be published on
LD_HOST_PORT=9090
# Directory on the host system that should be mounted as data dir into the Docker container
LD_HOST_DATA_DIR=./data

# Can be used to run linkding under a context path, for example: linkding/
# Must end with a slash `/`
LD_CONTEXT_PATH=
# Username of the initial superuser to create, leave empty to not create one
LD_SUPERUSER_NAME=username
# Password for the initial superuser, leave empty to disable credentials authentication and rely on proxy authentication instead
LD_SUPERUSER_PASSWORD=password
# Option to disable background tasks
LD_DISABLE_BACKGROUND_TASKS=False
# Option to disable URL validation for bookmarks completely
LD_DISABLE_URL_VALIDATION=False
# Enables support for authentication proxies such as Authelia
LD_ENABLE_AUTH_PROXY=False
# Name of the request header that the auth proxy passes to the application to identify the user
# See docs/Options.md for more details
LD_AUTH_PROXY_USERNAME_HEADER=
# The URL that linkding should redirect to after a logout, when using an auth proxy
# See docs/Options.md for more details
LD_AUTH_PROXY_LOGOUT_URL=
# List of trusted origins from which to accept POST requests
# See docs/Options.md for more details
LD_CSRF_TRUSTED_ORIGINS=

# Database settings
# These are currently only required for configuring PostreSQL.
# By default, linkding uses SQLite for which you don't need to configure anything.

# Database engine, can be sqlite (default) or postgres
LD_DB_ENGINE=
# Database name (default: linkding)
LD_DB_DATABASE=
# Username to connect to the database server  (default: linkding)
LD_DB_USER=
# Password to connect to the database server
LD_DB_PASSWORD=
# The hostname where the database is hosted (default: localhost)
LD_DB_HOST=
# Port use to connect to the database server
# Should use the default port if not set
LD_DB_PORT=
# Any additional options to pass to the database (default: {})
LD_DB_OPTIONS=
```

## Step 4: Start Linkding with Docker Compose

``` wp-block-code
docker-compose up -d
```

This will start the service in detached mode. You can then access Linkding at http://\<your-ip\>:9090
