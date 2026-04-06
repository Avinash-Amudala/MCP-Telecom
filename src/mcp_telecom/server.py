"""MCP-Telecom Server — The first MCP server for network equipment.

Exposes network device operations as MCP tools, resources, and prompts
so AI agents (Claude, GPT, etc.) can interact with Nokia SR OS, Cisco IOS-XR,
Juniper Junos, and other network equipment through natural language.
"""

from __future__ import annotations

import json
import logging
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from mcp_telecom.audit import AuditLogger
from mcp_telecom.connection import DeviceManager
from mcp_telecom.safety import validate_command
from mcp_telecom.vendors.mappings import get_command, list_operations

load_dotenv()

logging.basicConfig(
    level=getattr(logging, os.getenv("MCP_TELECOM_LOG_LEVEL", "INFO")),
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("mcp_telecom")

# ── Initialize core components ──────────────────────────────────────────────

mcp = FastMCP(
    "MCP-Telecom",
    version="0.1.0",
    description=(
        "The first MCP server for network equipment. "
        "Interact with Nokia SR OS, Cisco IOS-XR, Juniper Junos, "
        "Arista EOS, and Cisco NX-OS routers through AI agents."
    ),
)

config_path = os.getenv("MCP_TELECOM_DEVICES_FILE", "devices.yaml")
device_manager = DeviceManager(config_path)
audit = AuditLogger()


# ═══════════════════════════════════════════════════════════════════════════
#  MCP TOOLS — Network Operations
# ═══════════════════════════════════════════════════════════════════════════


# ── Routing Protocol Tools ──────────────────────────────────────────────────

@mcp.tool()
def show_bgp_summary(device: str) -> str:
    """Show BGP neighbor summary on a network device.

    Returns the BGP peering table with neighbor states, prefixes received,
    and session uptime. Works across all supported vendors.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "bgp_summary")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_bgp_summary", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_bgp_summary", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_bgp_neighbors(device: str) -> str:
    """Show detailed BGP neighbor information on a network device.

    Returns per-neighbor details including state, AS number, messages
    sent/received, and hold time.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "bgp_neighbors")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_bgp_neighbors", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_bgp_neighbors", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_routing_table(device: str) -> str:
    """Show the IP routing table on a network device.

    Returns all routes with protocol, next-hop, metric, and preference.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "routing_table")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_routing_table", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_routing_table", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_ospf_neighbors(device: str) -> str:
    """Show OSPF neighbor adjacencies on a network device.

    Returns OSPF neighbor states, interface associations, and dead intervals.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "ospf_neighbors")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_ospf_neighbors", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_ospf_neighbors", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_mpls_lsp(device: str) -> str:
    """Show MPLS Label Switched Paths on a network device.

    Returns LSP status, tunnel endpoints, and label bindings.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "mpls_lsp")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_mpls_lsp", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_mpls_lsp", False, error=str(e))
        return f"Error: {e}"


# ── Interface Tools ─────────────────────────────────────────────────────────

@mcp.tool()
def show_interfaces(device: str) -> str:
    """Show interface status summary on a network device.

    Returns all interfaces with admin/operational status, speed, and description.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "interfaces")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_interfaces", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_interfaces", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_interface_detail(device: str, interface: str) -> str:
    """Show detailed statistics for a specific interface.

    Returns counters, errors, CRC, drops, utilization, MTU, and speed
    for the specified interface.

    Args:
        device: Name of the device as defined in devices.yaml
        interface: Interface name (e.g., 'Gi0/0/0', '1/1/1', 'ge-0/0/0')
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "interface_detail", interface=interface)
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_interface_detail", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_interface_detail", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_lldp_neighbors(device: str) -> str:
    """Show LLDP neighbor discovery information.

    Returns connected neighbors with their system name, port ID,
    and capabilities — useful for topology discovery.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "lldp_neighbors")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_lldp_neighbors", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_lldp_neighbors", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_lag_status(device: str) -> str:
    """Show Link Aggregation Group (LAG/Port-Channel/Bundle) status.

    Returns LAG member ports, their states, and aggregate bandwidth.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "lag_status")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_lag_status", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_lag_status", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_arp_table(device: str) -> str:
    """Show the ARP table on a network device.

    Returns IP-to-MAC address mappings for all entries in the ARP cache.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "arp_table")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_arp_table", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_arp_table", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_mac_table(device: str) -> str:
    """Show the MAC address table on a network device.

    Returns MAC addresses, VLANs, and associated interfaces.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "mac_table")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_mac_table", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_mac_table", False, error=str(e))
        return f"Error: {e}"


# ── System Monitoring Tools ─────────────────────────────────────────────────

@mcp.tool()
def show_system_info(device: str) -> str:
    """Show system information including version, uptime, and hardware.

    Returns device platform, software version, uptime, serial number,
    and hardware details.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "system_info")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_system_info", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_system_info", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_alarms(device: str) -> str:
    """Show active alarms and alerts on a network device.

    Returns current alarm conditions including severity, timestamp, and description.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "alarms")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_alarms", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_alarms", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_ntp_status(device: str) -> str:
    """Show NTP synchronization status on a network device.

    Returns NTP peers, stratum, offset, and synchronization state.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "ntp_status")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_ntp_status", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_ntp_status", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_cpu(device: str) -> str:
    """Show CPU utilization on a network device.

    Returns CPU usage per core/process to identify resource bottlenecks.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "cpu")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_cpu", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_cpu", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_memory(device: str) -> str:
    """Show memory utilization on a network device.

    Returns memory pool usage, free/used/total memory statistics.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "memory")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_memory", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_memory", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_environment(device: str) -> str:
    """Show environmental monitoring on a network device.

    Returns power supply, fan, and temperature sensor readings.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "environment")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_environment", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_environment", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def show_log_events(device: str) -> str:
    """Show recent log/syslog messages from a network device.

    Returns the most recent event log entries for troubleshooting.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "log_events")
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, "show_log_events", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", "show_log_events", False, error=str(e))
        return f"Error: {e}"


# ── Configuration & Backup Tools ────────────────────────────────────────────

@mcp.tool()
def backup_config(device: str) -> str:
    """Backup the running configuration of a network device.

    Fetches the full running config and saves a timestamped copy locally.
    Returns the configuration content and the backup file path.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        from mcp_telecom.tools.system import backup_config as _backup
        return _backup(device_manager, audit, device)
    except Exception as e:
        audit.log_command(device, "", "backup_config", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def compare_configs(device: str, backup_file: str) -> str:
    """Compare the current running config with a previous backup.

    Performs a diff between the live running configuration and a saved
    backup file, highlighting additions and removals.

    Args:
        device: Name of the device as defined in devices.yaml
        backup_file: Path to the backup file to compare against
    """
    try:
        import difflib
        from pathlib import Path

        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, "config_running")
        with device_manager.connect(device) as conn:
            current = conn.send_command(cmd, read_timeout=60)

        backup_path = Path(backup_file)
        if not backup_path.exists():
            return f"Error: Backup file not found: {backup_file}"

        previous = backup_path.read_text()

        diff = difflib.unified_diff(
            previous.splitlines(keepends=True),
            current.splitlines(keepends=True),
            fromfile=f"backup ({backup_file})",
            tofile=f"running ({device})",
            lineterm="",
        )
        diff_text = "\n".join(diff)

        audit.log_command(device, cmd, "compare_configs", True, len(diff_text))
        return diff_text if diff_text else "No differences found — configs are identical."
    except Exception as e:
        audit.log_command(device, "", "compare_configs", False, error=str(e))
        return f"Error: {e}"


# ── Generic Command Execution ───────────────────────────────────────────────

@mcp.tool()
def run_command(device: str, command: str) -> str:
    """Run any read-only (show) command on a network device.

    For safety, only read-only commands are permitted. Configuration commands
    are blocked. Use this when you need a specific command not covered by
    the dedicated tools.

    Args:
        device: Name of the device as defined in devices.yaml
        command: The CLI command to execute
            (must start with 'show', 'display', 'ping', or 'traceroute')
    """
    error = validate_command(command)
    if error:
        audit.log_command(device, command, "run_command", False, error=error)
        return f"Error: {error}"

    try:
        with device_manager.connect(device) as conn:
            output = conn.send_command(command)
        audit.log_command(device, command, "run_command", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, command, "run_command", False, error=str(e))
        return f"Error: {e}"


@mcp.tool()
def run_vendor_operation(device: str, operation: str) -> str:
    """Run a named operation using the vendor-specific command mapping.

    This automatically translates the operation name to the correct CLI
    command for the device's vendor. Use 'list_device_capabilities' to see
    available operations.

    Args:
        device: Name of the device as defined in devices.yaml
        operation: Operation name (e.g., 'bgp_summary', 'interfaces', 'alarms')
    """
    try:
        config = device_manager.get_device(device)
        cmd = get_command(config.device_type, operation)
        with device_manager.connect(device) as conn:
            output = conn.send_command(cmd)
        audit.log_command(device, cmd, f"run_vendor_operation:{operation}", True, len(output))
        return output
    except Exception as e:
        audit.log_command(device, "", f"run_vendor_operation:{operation}", False, error=str(e))
        return f"Error: {e}"


# ── Device Management Tools ─────────────────────────────────────────────────

@mcp.tool()
def list_devices() -> str:
    """List all configured network devices.

    Returns the names, hosts, vendors, and ports of all devices
    available for interaction.
    """
    devices = device_manager.list_devices()
    if not devices:
        return "No devices configured. Add devices to devices.yaml."

    lines = ["Configured Devices:", "=" * 60]
    for d in devices:
        lines.append(f"  {d.name:20s}  {d.host:15s}  {d.vendor.value:15s}  port:{d.port}")
    return "\n".join(lines)


@mcp.tool()
def list_device_capabilities(device: str) -> str:
    """List all supported operations for a specific device.

    Shows what commands are available for this device based on its vendor type.
    Use the operation names with the 'run_vendor_operation' tool.

    Args:
        device: Name of the device as defined in devices.yaml
    """
    try:
        config = device_manager.get_device(device)
        ops = list_operations(config.device_type)
        lines = [
            f"Capabilities for '{device}' ({config.device_type.value}):",
            "-" * 50,
        ]
        for op in ops:
            cmd = get_command(config.device_type, op)
            lines.append(f"  {op:25s} → {cmd}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def health_check(device: str | None = None) -> str:
    """Check reachability and response time for devices.

    Tests SSH connectivity and measures response time. If no device is
    specified, checks all configured devices.

    Args:
        device: Optional device name. If omitted, checks all devices.
    """
    if device:
        status = device_manager.check_health(device)
        state = "REACHABLE" if status.reachable else "UNREACHABLE"
        result = f"{device}: {state}"
        if status.reachable:
            result += f" (response: {status.response_time_ms}ms)"
        else:
            result += f" (error: {status.error})"
        return result

    from mcp_telecom.tools.system import health_check_all
    return health_check_all(device_manager)


@mcp.tool()
def get_audit_log(count: int = 25) -> str:
    """Retrieve recent entries from the command audit log.

    Shows what commands have been executed, when, on which device,
    and whether they succeeded.

    Args:
        count: Number of recent entries to retrieve (default: 25)
    """
    entries = audit.get_recent_entries(count)
    if not entries:
        return "No audit log entries found."

    lines = ["Recent Audit Log:", "=" * 80]
    for entry in entries:
        ts = entry.get("timestamp", "?")[:19]
        dev = entry.get("device", "?")
        cmd = entry.get("command", "?")
        ok = "OK" if entry.get("success") else "FAIL"
        lines.append(f"  [{ts}] {ok:4s} {dev:15s} {cmd}")
    return "\n".join(lines)


# ── Nokia SR OS Specific Tools ──────────────────────────────────────────────

@mcp.tool()
def show_nokia_services(device: str) -> str:
    """Show Nokia SR OS service summary (VPRN, VPLS, SAP).

    Nokia-specific tool for viewing all configured services.
    Only works on Nokia SR OS devices.

    Args:
        device: Name of a Nokia SR OS device
    """
    try:
        config = device_manager.get_device(device)
        if "nokia" not in config.device_type.value:
            return "Error: This tool only works on Nokia SR OS devices."

        results = []
        with device_manager.connect(device) as conn:
            for op in ["vprn_service", "vpls_service", "sap_status"]:
                try:
                    cmd = get_command(config.device_type, op)
                    output = conn.send_command(cmd)
                    results.append(f"--- {op} ---\n{output}")
                except ValueError:
                    pass

        combined = "\n\n".join(results)
        audit.log_command(device, "show services", "show_nokia_services", True, len(combined))
        return combined
    except Exception as e:
        audit.log_command(device, "", "show_nokia_services", False, error=str(e))
        return f"Error: {e}"


# ═══════════════════════════════════════════════════════════════════════════
#  MCP RESOURCES — Device Information
# ═══════════════════════════════════════════════════════════════════════════

@mcp.resource("telecom://devices")
def resource_device_inventory() -> str:
    """Full inventory of all configured network devices."""
    devices = device_manager.list_devices()
    inventory = [
        {
            "name": d.name,
            "host": d.host,
            "vendor": d.vendor.value,
            "port": d.port,
        }
        for d in devices
    ]
    return json.dumps(inventory, indent=2)


@mcp.resource("telecom://devices/{device_name}/info")
def resource_device_info(device_name: str) -> str:
    """Configuration metadata for a specific device (no secrets)."""
    try:
        config = device_manager.get_device(device_name)
        info = {
            "name": device_name,
            "host": config.host,
            "vendor": config.device_type.value,
            "port": config.port,
            "timeout": config.timeout,
            "supported_operations": list_operations(config.device_type),
        }
        return json.dumps(info, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.resource("telecom://vendors")
def resource_supported_vendors() -> str:
    """List of all supported network equipment vendors."""
    from mcp_telecom.models import VendorType
    vendors = [
        {
            "type": v.value,
            "operations_count": len(list_operations(v)),
        }
        for v in VendorType
    ]
    return json.dumps(vendors, indent=2)


@mcp.resource("telecom://audit-log")
def resource_audit_log() -> str:
    """Recent command audit log entries."""
    entries = audit.get_recent_entries(100)
    return json.dumps(entries, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
#  MCP PROMPTS — Troubleshooting Templates
# ═══════════════════════════════════════════════════════════════════════════

@mcp.prompt()
def troubleshoot_bgp(device: str) -> str:
    """Step-by-step BGP troubleshooting workflow for a device."""
    return f"""You are a senior network engineer troubleshooting BGP on device '{device}'.

Follow this systematic approach:

1. **Check BGP Summary** — Use show_bgp_summary('{device}') to see all BGP peers.
   - Look for peers in non-Established states
   - Check if prefix counts look normal

2. **Examine Specific Neighbors** — Use show_bgp_neighbors('{device}') for detailed neighbor info.
   - Check hold-time and keepalive timers
   - Look for notification messages

3. **Verify Routing Table** — Use show_routing_table('{device}') to check if expected routes exist.
   - Confirm next-hop reachability
   - Check for missing prefixes

4. **Check Interfaces** — Use show_interfaces('{device}') to verify the peering interface is up.
   - Confirm IP addressing
   - Check for errors/drops

5. **Review Logs** — Use show_log_events('{device}') for recent BGP-related events.

6. **System Resources** — Use show_cpu('{device}') and show_memory('{device}')
   to rule out resource issues.

Provide a diagnosis with:
- Root cause analysis
- Impact assessment
- Recommended remediation steps
"""


@mcp.prompt()
def troubleshoot_interface(device: str, interface: str) -> str:
    """Step-by-step interface troubleshooting workflow."""
    return f"""You are a senior network engineer troubleshooting \
interface '{interface}' on device '{device}'.

Follow this systematic approach:

1. **Interface Status** — Use show_interface_detail('{device}', '{interface}') for detailed stats.
   - Check admin/oper status
   - Look for errors, CRC, drops
   - Verify speed/duplex

2. **Interface Summary** — Use show_interfaces('{device}') to see this interface in context.

3. **LLDP Neighbors** — Use show_lldp_neighbors('{device}') to check physical connectivity.
   - Verify the expected neighbor is connected

4. **ARP Table** — Use show_arp_table('{device}') to check Layer 3 reachability.

5. **Log Events** — Use show_log_events('{device}') for interface-related events.
   - Look for flap events
   - Check for error messages

Provide a diagnosis with:
- Current interface state summary
- Identified issues
- Recommended actions
"""


@mcp.prompt()
def network_health_audit(device: str) -> str:
    """Comprehensive network device health audit."""
    return f"""You are performing a comprehensive health audit on device '{device}'.

Execute these checks systematically:

1. **System Overview**
   - show_system_info('{device}') — Version, uptime, hardware
   - show_environment('{device}') — Power, fans, temperature

2. **Resource Utilization**
   - show_cpu('{device}') — CPU usage
   - show_memory('{device}') — Memory usage

3. **Active Alarms**
   - show_alarms('{device}') — Any active alarms

4. **Network State**
   - show_interfaces('{device}') — Interface health
   - show_bgp_summary('{device}') — BGP peering state
   - show_ospf_neighbors('{device}') — OSPF adjacencies
   - show_routing_table('{device}') — Route count and sources

5. **Time Sync**
   - show_ntp_status('{device}') — NTP synchronization

6. **Recent Activity**
   - show_log_events('{device}') — Recent logs

Generate a health report with:
- Overall health score (Critical / Warning / Healthy)
- Summary of findings per category
- List of issues found (sorted by severity)
- Recommended actions
"""


@mcp.prompt()
def compare_device_pair(device_a: str, device_b: str) -> str:
    """Compare two devices side-by-side for consistency checks."""
    return f"""You are comparing devices '{device_a}' and '{device_b}' for consistency.

Collect data from both devices:

1. **System Info** — show_system_info for both devices
   - Compare software versions
   - Compare uptime

2. **Interfaces** — show_interfaces for both devices
   - Compare interface states
   - Identify mismatches

3. **BGP State** — show_bgp_summary for both devices
   - Compare peer counts
   - Check if they peer with each other

4. **Routing** — show_routing_table for both devices
   - Compare route counts
   - Look for asymmetric routes

Generate a comparison report highlighting:
- Matching configurations
- Discrepancies found
- Potential issues
- Recommendations for alignment
"""


# ═══════════════════════════════════════════════════════════════════════════
#  Server Entry Point
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Run the MCP-Telecom server."""
    logger.info("Starting MCP-Telecom server v0.1.0")
    logger.info("Loaded %d devices", len(device_manager.list_devices()))
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
