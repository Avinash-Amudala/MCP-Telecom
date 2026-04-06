# MCP-Telecom

### Let AI agents talk to your network equipment.

**The first MCP server for Nokia SR OS, Cisco IOS-XR, Juniper Junos, Arista EOS, and Cisco NX-OS routers.**

> _"Hey Claude, show me the BGP summary on nokia-pe1 and check if any peers are down."_

MCP-Telecom bridges the gap between AI assistants and network infrastructure. It implements the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) to give AI agents like Claude and GPT secure, read-only access to your network devices via SSH — no custom scripts, no fragile automation, just natural language.

---

## Why MCP-Telecom?

| Problem | Solution |
|---|---|
| Network engineers SSH into devices one-by-one | AI queries multiple devices in parallel |
| Vendor CLI syntax differs across Nokia, Cisco, Juniper | Unified interface — one tool works across all vendors |
| Junior engineers struggle with complex troubleshooting | AI-guided workflows with built-in troubleshooting prompts |
| No audit trail for ad-hoc show commands | Every command logged with timestamps |
| Automation scripts break across vendor upgrades | Vendor-abstracted command mappings maintained in one place |

## Features

- **Multi-Vendor Support** — Nokia SR OS, Cisco IOS / IOS-XR / NX-OS, Juniper Junos, Arista EOS
- **25+ Network Tools** — BGP, OSPF, MPLS, interfaces, alarms, NTP, ARP, MAC tables, and more
- **Vendor Abstraction** — Say `bgp_summary` and get the right command for any vendor
- **Safety First** — Only read-only commands allowed; destructive commands are blocked
- **Audit Logging** — Every command execution recorded in structured JSONL format
- **Config Backup & Diff** — Backup running configs and compare against previous versions
- **Health Checks** — Test device reachability with response time measurement
- **MCP Resources** — Device inventory and vendor info exposed as browseable resources
- **Troubleshooting Prompts** — Built-in BGP, interface, and health audit workflows
- **Nokia Service Tools** — VPRN, VPLS, and SAP inspection for Nokia SR OS
- **Docker Support** — Run containerized with docker-compose
- **CI/CD** — GitHub Actions with multi-Python-version testing

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AI Agent (Claude/GPT)                 │
│                                                         │
│  "Show me BGP neighbors on nokia-pe1 that are down"     │
└─────────────────────┬───────────────────────────────────┘
                      │  MCP Protocol (stdio)
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   MCP-Telecom Server                    │
│                                                         │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐  │
│  │  Tools  │  │Resources │  │ Prompts │  │  Safety  │  │
│  │ (25+)   │  │(inventory│  │(trouble-│  │(command  │  │
│  │         │  │ vendors) │  │ shoot)  │  │ filter)  │  │
│  └────┬────┘  └──────────┘  └─────────┘  └──────────┘  │
│       │                                                 │
│  ┌────▼─────────────────────────────────────────────┐   │
│  │           Vendor Command Mappings                │   │
│  │  Nokia ─── Cisco ─── Juniper ─── Arista          │   │
│  └────┬─────────┬──────────┬───────────┬────────────┘   │
│       │         │          │           │                 │
│  ┌────▼─────────▼──────────▼───────────▼────────────┐   │
│  │        Connection Manager (Netmiko/SSH)          │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────▼───────────────────────────┐   │
│  │              Audit Logger (JSONL)                │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────┘
                          │  SSH
                          ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Nokia    │  │ Cisco    │  │ Juniper  │  │ Arista   │
│ SR OS    │  │ IOS-XR   │  │ Junos    │  │ EOS      │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- SSH access to your network devices

### Installation

```bash
# Clone the repository
git clone https://github.com/Avinash-Amudala/MCP-Telecom.git
cd MCP-Telecom

# Install with uv
uv sync

# Or install with pip
pip install -e .
```

### Configure Your Devices

```bash
# Copy the example config and edit with your device details
cp devices.yaml.example devices.yaml
```

Edit `devices.yaml` with your actual device credentials:

```yaml
nokia-pe1:
  device_type: nokia_sros
  host: 192.168.1.1
  username: admin
  password: your_password
  port: 22

cisco-xr1:
  device_type: cisco_xr
  host: 192.168.2.1
  username: admin
  password: your_password

juniper-mx1:
  device_type: juniper_junos
  host: 192.168.3.1
  username: admin
  password: your_password
```

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run mcp-telecom
```

### Use with Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mcp-telecom": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/MCP-Telecom",
        "mcp-telecom"
      ],
      "env": {
        "MCP_TELECOM_DEVICES_FILE": "/path/to/MCP-Telecom/devices.yaml"
      }
    }
  }
}
```

## Available Tools

### Routing & Protocols

| Tool | Description |
|------|-------------|
| `show_bgp_summary` | BGP neighbor summary with peer states |
| `show_bgp_neighbors` | Detailed BGP neighbor information |
| `show_routing_table` | Full IP routing table |
| `show_ospf_neighbors` | OSPF neighbor adjacencies |
| `show_mpls_lsp` | MPLS Label Switched Paths |

### Interfaces & Layer 2

| Tool | Description |
|------|-------------|
| `show_interfaces` | Interface status summary |
| `show_interface_detail` | Detailed per-interface statistics |
| `show_lldp_neighbors` | LLDP neighbor discovery |
| `show_lag_status` | LAG/Port-Channel/Bundle status |
| `show_arp_table` | IP-to-MAC ARP cache |
| `show_mac_table` | MAC address table |

### System Monitoring

| Tool | Description |
|------|-------------|
| `show_system_info` | Version, uptime, hardware |
| `show_alarms` | Active alarms and alerts |
| `show_ntp_status` | NTP synchronization state |
| `show_cpu` | CPU utilization |
| `show_memory` | Memory utilization |
| `show_environment` | Power, fans, temperature |
| `show_log_events` | Recent syslog messages |

### Configuration & Operations

| Tool | Description |
|------|-------------|
| `backup_config` | Backup running config with timestamp |
| `compare_configs` | Diff live config against a backup |
| `run_command` | Execute any safe read-only command |
| `run_vendor_operation` | Run named operation with auto vendor translation |
| `list_devices` | List all configured devices |
| `list_device_capabilities` | Show supported operations per device |
| `health_check` | Test device reachability |
| `get_audit_log` | View command execution history |
| `show_nokia_services` | Nokia VPRN/VPLS/SAP services |

## Supported Platforms

| Vendor | Device Types | Netmiko Type |
|--------|-------------|--------------|
| **Nokia** | 7750 SR, 7950 XRS, 7250 IXR | `nokia_sros` |
| **Cisco** | IOS, IOS-XE | `cisco_ios` |
| **Cisco** | IOS-XR (NCS, ASR) | `cisco_xr` |
| **Cisco** | NX-OS (Nexus) | `cisco_nxos` |
| **Juniper** | MX, QFX, EX, SRX | `juniper_junos` |
| **Arista** | 7000, 7500 series | `arista_eos` |

## Safety & Security

MCP-Telecom enforces strict read-only access:

- **Allowed**: `show`, `display`, `ping`, `traceroute` commands
- **Blocked**: `configure`, `set`, `delete`, `commit`, `reload`, `shutdown`, `write`, `clear`, `reset`, `debug`, and 20+ other dangerous patterns
- **Audit Trail**: Every command execution is logged with timestamp, device, success/failure, and output length

```
[2026-04-06T12:00:00Z] OK   nokia-pe1       show router bgp summary
[2026-04-06T12:00:05Z] OK   cisco-xr1       show ip interface brief
[2026-04-06T12:00:10Z] FAIL cisco-xr1       configure terminal  ← BLOCKED
```

## Docker

```bash
# Build and run
docker-compose up -d

# Or build manually
docker build -t mcp-telecom .
docker run -v ./devices.yaml:/app/devices.yaml:ro mcp-telecom
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
uv run pytest tests/ -v

# Lint
uv run ruff check src/ tests/

# Test with MCP Inspector
npx @modelcontextprotocol/inspector uv run mcp-telecom
```

## Project Structure

```
MCP-Telecom/
├── src/mcp_telecom/
│   ├── __init__.py          # Package init
│   ├── server.py            # MCP server (tools + resources + prompts)
│   ├── connection.py        # Device connection manager
│   ├── models.py            # Pydantic data models
│   ├── safety.py            # Command safety validation
│   ├── audit.py             # Audit logging
│   ├── vendors/
│   │   ├── __init__.py
│   │   └── mappings.py      # Vendor-specific command mappings
│   └── tools/
│       ├── __init__.py
│       ├── routing.py       # Routing protocol tools
│       ├── interfaces.py    # Interface monitoring tools
│       └── system.py        # System monitoring tools
├── tests/                   # Comprehensive test suite
├── examples/                # Usage examples and configs
├── docs/                    # Documentation
├── .github/workflows/       # CI/CD pipeline
├── pyproject.toml           # Project configuration
├── Dockerfile               # Container support
├── docker-compose.yml       # Docker Compose config
├── devices.yaml.example     # Example device config
└── README.md                # This file
```

## Roadmap

- [ ] **SNMP support** — Poll SNMP MIBs alongside SSH
- [ ] **NETCONF/YANG** — gNMI and NETCONF transport support
- [ ] **Connection pooling** — Persistent SSH sessions for faster queries
- [ ] **Streaming telemetry** — Real-time gRPC telemetry ingestion
- [ ] **Topology discovery** — Auto-build network topology from LLDP/CDP
- [ ] **Config compliance** — Check configs against golden templates
- [ ] **Multi-device queries** — Run commands across device groups simultaneously
- [ ] **Web dashboard** — Real-time device status dashboard
- [ ] **Prometheus metrics** — Export network metrics for Grafana

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE) — Avinash Amudala

---

**Built with [MCP](https://modelcontextprotocol.io) + [Netmiko](https://github.com/ktbyers/netmiko) + [FastMCP](https://github.com/jlowin/fastmcp)**
