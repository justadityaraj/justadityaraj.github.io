---
title: "How to Install n8n with MCP on Proxmox"
date: "2025-06-08T17:38:42"
modified: "2025-06-08T17:40:43"
slug: "install-n8n-with-mcp-on-proxmox"
original_url: "https://adityarajsingh.com/install-n8n-with-mcp-on-proxmox/"
categories: ["Homelab"]
tags: ["n8n", "Proxmox"]
excerpt: "Get the Proxmox VE n8n Helper Script from here or copy the command below and run in your proxmox node (pve) shell. It will setup as a LXC. Once n8n is up and running, go to Settings > Usage and activate your instance using the n8n activation key. Enable MCP Node Support MCP (Model Context […]"
---

# How to Install n8n with MCP on Proxmox

Get the Proxmox VE n8n Helper Script from <a href="https://community-scripts.github.io/ProxmoxVE/scripts?id=n8n" class="ek-link">here</a> or copy the command below and run in your proxmox node (pve) shell. It will setup as a LXC.

``` wp-block-code
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/n8n.sh)"
```

Once n8n is up and running, go to Settings \> Usage and activate your instance using the n8n activation key.

## Enable MCP Node Support

MCP (Model Context Protocol) is a protocol that enables AI models to interact with external tools and data sources in a standardized way.

<a href="https://github.com/nerding-io/n8n-nodes-mcp" class="ek-link">n8n-nodes-mcp</a> allows you to connect to MCP servers, access resources, execute tools, and use prompts.

This node can be used as a tool in n8n AI Agents.

To enable this node as a tool, you need to set the **N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE** environment variable to **true**.

Since n8n is installed globally via npm (it's at /usr/lib/node_modules/n8n/) in proxmox, It runs as a **systemd n8n.service** where we will inject the environment variable.

To confirm, run this command to look for a systemd service in your n8n LXC console.

``` wp-block-code
systemctl list-units --type=service | grep n8n
```

If it shows a result like n8n.service, continue with:

``` wp-block-code
systemctl cat n8n.service
```

That will show how it’s being run.

### Set MCP Environment Variable

Run:

``` wp-block-code
systemctl edit n8n.service
```

Add these lines under \[Service\] in the editor:

``` wp-block-code
Environment="N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true"
```

Save and exit, reload and restart.

``` wp-block-code
systemctl daemon-reexec
systemctl daemon-reload
systemctl restart n8n.service
```

### Confirm the variable

``` wp-block-code
cat /proc/$(pgrep -f 'n8n')/environ | tr '\0' '\n' | grep N8N_COMMUNITY_PACKAGES
```

Restart your n8n LXC, then log into it.

## Install the MCP Node in n8n

Go to n8n \> settings \> community nodes \> click Install.

Write **n8n-nodes-mcp** for the npm Package Name, click install, and that should be it.

To confirm, create a workflow, open nodes panel and search for MCP and "MCP Client" will show up.

Your n8n instance on Proxmox is now MCP-ready.

You can build powerful AI Agent workflows by connecting external tools and resources using the MCP Client node.

If you run into issues or want to explore more AI integrations, check out the <a href="https://docs.n8n.io/" class="ek-link">n8n documentation</a>.
