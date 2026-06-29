"""The diagnostic decision trees.

Each flow is an ordered set of steps. A "check" step asks you to run something
and tells you how to read it; depending on whether it passed, the engine moves
to on_pass or on_fail. A "conclusion" step names the likely cause, the fix, and
when to escalate. Commands are written for Windows first, since that is the
common desk environment, with a short note where the idea differs elsewhere.
"""
from __future__ import annotations

# Step shapes
#   check:      {kind, text, command, interpret, on_pass, on_fail}
#   conclusion: {kind, cause, fix, escalate}

FLOWS: dict[str, dict] = {
    "one-pc-no-internet": {
        "title": "One PC has no internet (others are fine)",
        "description": "A single machine cannot reach the internet while the rest of the office is working.",
        "start": "link",
        "steps": {
            "link": {
                "kind": "check",
                "text": "Is the network link up? Check the Ethernet icon / Wi-Fi status, and the cable or wireless connection.",
                "command": "ipconfig",
                "interpret": "If the adapter shows 'Media disconnected', the link is down. A connected adapter shows an IPv4 address.",
                "on_fail": "fix-link",
                "on_pass": "ipaddr",
            },
            "fix-link": {
                "kind": "conclusion",
                "cause": "Physical or wireless link is down on this PC.",
                "fix": "Reseat or replace the cable, try another wall port or switch port, or re-join the Wi-Fi network. Confirm the adapter is enabled in Network Connections.",
                "escalate": "If a known-good cable and port still show 'Media disconnected', escalate as a possible NIC or switch-port fault.",
            },
            "ipaddr": {
                "kind": "check",
                "text": "Does the PC have a valid IP address from DHCP?",
                "command": "ipconfig /all",
                "interpret": "A 169.254.x.x address (APIPA) means DHCP failed. A normal address in the office range (and a listed DHCP server) means DHCP is fine.",
                "on_fail": "fix-dhcp",
                "on_pass": "gateway",
            },
            "fix-dhcp": {
                "kind": "conclusion",
                "cause": "The PC did not get an address from DHCP (self-assigned 169.254.x.x).",
                "fix": "Run 'ipconfig /release' then 'ipconfig /renew'. If it still self-assigns, check the cable/port and confirm the DHCP scope is not exhausted.",
                "escalate": "If multiple PCs later show APIPA, escalate: the DHCP server or scope is the likely cause, not this PC.",
            },
            "gateway": {
                "kind": "check",
                "text": "Can the PC reach its default gateway (the local router)?",
                "command": "ping <default-gateway-from-ipconfig>",
                "interpret": "Replies mean the local network path is good. Timeouts mean the problem is between the PC and the router.",
                "on_fail": "fix-gateway",
                "on_pass": "dns",
            },
            "fix-gateway": {
                "kind": "conclusion",
                "cause": "The PC cannot reach the local gateway, so nothing beyond the LAN will work.",
                "fix": "Check for a wrong static IP or subnet mask, a VLAN mismatch on the switch port, or a firewall blocking local traffic. Set the adapter back to DHCP if it was set static.",
                "escalate": "If the addressing is correct and the gateway still does not answer, escalate to network/switch support.",
            },
            "dns": {
                "kind": "check",
                "text": "Can the PC resolve names? Test DNS directly.",
                "command": "nslookup microsoft.com",
                "interpret": "A returned address means DNS works. 'request timed out' or 'server can't find' means name resolution is broken even though the network path is fine.",
                "on_fail": "fix-dns",
                "on_pass": "outbound",
            },
            "fix-dns": {
                "kind": "conclusion",
                "cause": "Name resolution (DNS) is failing on this PC.",
                "fix": "Run 'ipconfig /flushdns'. Confirm the DNS servers in 'ipconfig /all' match the office DNS. If they are wrong, set the adapter back to DHCP so it gets the correct ones.",
                "escalate": "If DNS settings are correct and lookups still fail, escalate: the DNS server itself may be down.",
            },
            "outbound": {
                "kind": "check",
                "text": "Can the PC reach the internet by IP, bypassing DNS?",
                "command": "ping 8.8.8.8",
                "interpret": "Replies here but failures by name point at DNS or a proxy. Timeouts here point at the gateway or upstream line.",
                "on_fail": "fix-gateway",
                "on_pass": "fix-app",
            },
            "fix-app": {
                "kind": "conclusion",
                "cause": "Network, IP and DNS are all healthy, so the issue is above the network layer.",
                "fix": "Check the browser proxy settings, any local firewall or antivirus web filter, and the specific application. Test in a second browser or an InPrivate window.",
                "escalate": "If a proxy or web filter is enforced centrally, escalate to whoever manages that policy.",
            },
        },
    },

    "site-down-whole-office": {
        "title": "Whole office or store has no internet",
        "description": "Multiple users at one site cannot reach the internet at the same time.",
        "start": "scope",
        "steps": {
            "scope": {
                "kind": "check",
                "text": "Confirm the scope: are most or all users at this site affected (not just one)?",
                "command": "Ask two or three users at different desks, or check if Wi-Fi and wired are both down.",
                "interpret": "Many users affected points at shared kit (router, line, switch). Only one points back to the single-PC flow.",
                "on_fail": "use-single",
                "on_pass": "router",
            },
            "use-single": {
                "kind": "conclusion",
                "cause": "Only one user is actually affected.",
                "fix": "Switch to the 'one-pc-no-internet' flow, which isolates a single machine.",
                "escalate": "No site-wide escalation needed yet.",
            },
            "router": {
                "kind": "check",
                "text": "Are the router and modem powered and showing normal link lights?",
                "command": "Look at the router/ONT: power, internet/WAN and LAN lights.",
                "interpret": "A red or dark WAN/internet light usually means the line from the provider is down, not your LAN.",
                "on_fail": "fix-line",
                "on_pass": "switch",
            },
            "fix-line": {
                "kind": "conclusion",
                "cause": "The internet line from the provider appears down (WAN light is red/off).",
                "fix": "Power-cycle the router/modem once. If the WAN light stays down for several minutes, log a fault with the ISP and note the time it started.",
                "escalate": "Raise an ISP ticket and inform the IT manager; this is an outage, not a desk fix.",
            },
            "switch": {
                "kind": "check",
                "text": "Is the internal network healthy? Can a working PC reach the gateway?",
                "command": "ping <default-gateway>  (from a wired PC)",
                "interpret": "If even the gateway is unreachable site-wide, a core switch or router has likely failed.",
                "on_fail": "fix-switch",
                "on_pass": "fix-dns-site",
            },
            "fix-switch": {
                "kind": "conclusion",
                "cause": "The local network path is down for everyone (core switch or router fault).",
                "fix": "Check the main switch for power and link lights; reseat the uplink. If a switch is dead, swap to a spare if available.",
                "escalate": "Escalate to network support with the affected site and start time.",
            },
            "fix-dns-site": {
                "kind": "conclusion",
                "cause": "The LAN is up but the internet is not reachable for the site, commonly DNS or the upstream line.",
                "fix": "Test 'ping 8.8.8.8' (path) and 'nslookup microsoft.com' (DNS) from a working PC to decide which. Restart the router if DNS is served from it.",
                "escalate": "If the line is up but nothing resolves, escalate to whoever runs the DNS/firewall.",
            },
        },
    },

    "cant-reach-internal-vpn": {
        "title": "Can't reach an internal site or SharePoint (VPN connected)",
        "description": "The user is on VPN and online generally, but a specific internal resource will not load.",
        "start": "vpn",
        "steps": {
            "vpn": {
                "kind": "check",
                "text": "Is the VPN actually connected and showing an assigned address?",
                "command": "Check the VPN client status, and 'ipconfig' for the VPN adapter's IP.",
                "interpret": "If the VPN shows connected with an internal IP, the tunnel is up. If not, the tunnel is the problem.",
                "on_fail": "fix-vpn",
                "on_pass": "other-internal",
            },
            "fix-vpn": {
                "kind": "conclusion",
                "cause": "The VPN tunnel is not actually established.",
                "fix": "Reconnect the VPN, confirm credentials/MFA, and check the user has internet first (the tunnel needs a working base connection).",
                "escalate": "If the client connects then drops, escalate with the VPN logs.",
            },
            "other-internal": {
                "kind": "check",
                "text": "Can the user reach any other internal resource (a different intranet site or file share)?",
                "command": "Open a second known internal URL or \\\\server\\share.",
                "interpret": "If everything else internal works, the problem is that one service. If nothing internal works, it is routing/DNS over the tunnel.",
                "on_fail": "fix-tunnel-dns",
                "on_pass": "resolve-name",
            },
            "fix-tunnel-dns": {
                "kind": "conclusion",
                "cause": "Nothing internal resolves over the VPN, so split-tunnel DNS or routing is wrong.",
                "fix": "Disconnect and reconnect to refresh routes, run 'ipconfig /flushdns', and confirm the VPN is pushing the internal DNS servers.",
                "escalate": "Escalate to whoever owns the VPN profile if internal DNS is not being applied.",
            },
            "resolve-name": {
                "kind": "check",
                "text": "Does the specific resource's name resolve to an address?",
                "command": "nslookup sharepoint.yourcompany.local",
                "interpret": "No address returned means a DNS record issue for that host. An address returned means DNS is fine and the service itself may be down.",
                "on_fail": "fix-record",
                "on_pass": "fix-service",
            },
            "fix-record": {
                "kind": "conclusion",
                "cause": "That one resource does not resolve, even though other internal names do.",
                "fix": "Confirm the exact URL/hostname with the user (typos are common). If the host is genuinely missing from DNS, raise it with the DNS owner.",
                "escalate": "Escalate the missing DNS record to the systems team.",
            },
            "fix-service": {
                "kind": "conclusion",
                "cause": "The name resolves and the path is up, so the service itself is likely the problem.",
                "fix": "Check whether other users can reach the same site. If it is down for everyone, it is a server/service issue, not the user's machine.",
                "escalate": "Escalate to the owner of that application or SharePoint site with the time and affected users.",
            },
        },
    },

    "wifi-drops": {
        "title": "Wi-Fi keeps dropping or is slow",
        "description": "A user's wireless connection is unstable or slow while wired users are fine.",
        "start": "signal",
        "steps": {
            "signal": {
                "kind": "check",
                "text": "Is the Wi-Fi signal strong where the user is sitting?",
                "command": "Check the Wi-Fi bars, and whether moving closer to the access point helps.",
                "interpret": "Weak signal that improves nearer the AP points at coverage, not the PC.",
                "on_fail": "fix-coverage",
                "on_pass": "band",
            },
            "fix-coverage": {
                "kind": "conclusion",
                "cause": "Weak wireless coverage at the user's location.",
                "fix": "Relocate the user, add or reposition an access point, or move them to wired if the desk is fixed.",
                "escalate": "Escalate a coverage gap to whoever manages the wireless so an AP can be added.",
            },
            "band": {
                "kind": "check",
                "text": "Is the adapter dropping only on this one PC, or do others nearby also drop?",
                "command": "Compare with a neighbour on the same Wi-Fi, and check the PC's wireless adapter driver.",
                "interpret": "Only this PC points at the adapter/driver or power settings. Several PCs points at the AP or interference.",
                "on_fail": "fix-ap",
                "on_pass": "fix-adapter",
            },
            "fix-ap": {
                "kind": "conclusion",
                "cause": "Several devices drop in the same area, so the access point or local interference is the cause.",
                "fix": "Check the AP for overload or a recent change, and look for interference (microwaves, other dense APs). Reboot the AP out of trading hours.",
                "escalate": "Escalate persistent area-wide drops to wireless support.",
            },
            "fix-adapter": {
                "kind": "conclusion",
                "cause": "Only this PC drops, so the wireless adapter, its driver, or power-saving is the likely cause.",
                "fix": "Update the wireless driver, and in the adapter's power management turn off 'allow the computer to turn off this device to save power'.",
                "escalate": "If it still drops after a driver update on a known-good AP, escalate as possible hardware.",
            },
        },
    },
}


def get_flow(key: str) -> dict:
    """Return a flow by key, raising a clear error if the key is unknown."""
    try:
        return FLOWS[key]
    except KeyError:
        raise KeyError(f"Unknown flow '{key}'. Available: {', '.join(FLOWS)}")
