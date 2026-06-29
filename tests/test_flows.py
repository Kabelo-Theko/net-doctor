"""Tests for net_doctor: tree integrity and that scripted answers land on the
right conclusion.
"""
from net_doctor.engine import run_flow, validate_flow
from net_doctor.flows import FLOWS, get_flow


def test_all_flows_are_structurally_sound():
    for key in FLOWS:
        problems = validate_flow(get_flow(key))
        assert problems == [], f"{key}: {problems}"


def test_one_pc_link_down_lands_on_link_fix():
    # First check (link) fails -> link fix conclusion.
    r = run_flow(get_flow("one-pc-no-internet"), [False])
    assert r.reached_conclusion
    assert "link" in r.conclusion["cause"].lower()


def test_one_pc_apipa_lands_on_dhcp_fix():
    # link passes, IP check fails -> DHCP conclusion.
    r = run_flow(get_flow("one-pc-no-internet"), [True, False])
    assert "dhcp" in r.conclusion["cause"].lower()


def test_one_pc_all_healthy_lands_above_network():
    # link, ip, gateway, dns, outbound all pass -> application-layer conclusion.
    r = run_flow(get_flow("one-pc-no-internet"), [True, True, True, True, True])
    assert "above the network" in r.conclusion["cause"].lower()


def test_vpn_specific_service_down():
    # vpn up, other internal works, name resolves -> service issue.
    r = run_flow(get_flow("cant-reach-internal-vpn"), [True, True, True])
    assert "service itself" in r.conclusion["cause"].lower()


def test_site_single_user_redirects():
    # scope check fails (only one user) -> use single-PC flow.
    r = run_flow(get_flow("site-down-whole-office"), [False])
    assert "one user" in r.conclusion["cause"].lower()


def test_running_out_of_answers_is_an_error():
    import pytest
    with pytest.raises(ValueError):
        run_flow(get_flow("one-pc-no-internet"), [True])  # not enough to conclude
