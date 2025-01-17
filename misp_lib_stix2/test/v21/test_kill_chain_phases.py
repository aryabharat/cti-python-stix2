"""Tests for stix.ExternalReference"""

import pytest

import misp_lib_stix2

LMCO_RECON = """{
    "kill_chain_name": "lockheed-martin-cyber-kill-chain",
    "phase_name": "reconnaissance"
}"""


def test_lockheed_martin_cyber_kill_chain():
    recon = misp_lib_stix2.v21.KillChainPhase(
        kill_chain_name="lockheed-martin-cyber-kill-chain",
        phase_name="reconnaissance",
    )

    assert recon.serialize(pretty=True) == LMCO_RECON


FOO_PRE_ATTACK = """{
    "kill_chain_name": "foo",
    "phase_name": "pre-attack"
}"""


def test_kill_chain_example():
    preattack = misp_lib_stix2.v21.KillChainPhase(
        kill_chain_name="foo",
        phase_name="pre-attack",
    )

    assert preattack.serialize(pretty=True) == FOO_PRE_ATTACK


def test_kill_chain_required_properties():

    with pytest.raises(misp_lib_stix2.exceptions.MissingPropertiesError) as excinfo:
        misp_lib_stix2.v21.KillChainPhase()

    assert excinfo.value.cls == misp_lib_stix2.v21.KillChainPhase
    assert excinfo.value.properties == ["kill_chain_name", "phase_name"]


def test_kill_chain_required_property_chain_name():

    with pytest.raises(misp_lib_stix2.exceptions.MissingPropertiesError) as excinfo:
        misp_lib_stix2.v21.KillChainPhase(phase_name="weaponization")

    assert excinfo.value.cls == misp_lib_stix2.v21.KillChainPhase
    assert excinfo.value.properties == ["kill_chain_name"]


def test_kill_chain_required_property_phase_name():

    with pytest.raises(misp_lib_stix2.exceptions.MissingPropertiesError) as excinfo:
        misp_lib_stix2.v21.KillChainPhase(kill_chain_name="lockheed-martin-cyber-kill-chain")

    assert excinfo.value.cls == misp_lib_stix2.v21.KillChainPhase
    assert excinfo.value.properties == ["phase_name"]
