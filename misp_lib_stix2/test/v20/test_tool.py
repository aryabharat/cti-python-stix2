import datetime as dt

import pytest
import pytz

import misp_lib_stix2

from .constants import IDENTITY_ID, TOOL_ID

EXPECTED = """{
    "type": "tool",
    "id": "tool--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
    "created_by_ref": "identity--311b2d2d-f010-4473-83ec-1edf84858f4c",
    "created": "2016-04-06T20:03:48.000Z",
    "modified": "2016-04-06T20:03:48.000Z",
    "name": "VNC",
    "labels": [
        "remote-access"
    ]
}"""

EXPECTED_WITH_REVOKED = """{
    "type": "tool",
    "id": "tool--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
    "created_by_ref": "identity--311b2d2d-f010-4473-83ec-1edf84858f4c",
    "created": "2016-04-06T20:03:48.000Z",
    "modified": "2016-04-06T20:03:48.000Z",
    "name": "VNC",
    "revoked": false,
    "labels": [
        "remote-access"
    ]
}"""


def test_tool_example():
    tool = misp_lib_stix2.v20.Tool(
        id=TOOL_ID,
        created_by_ref=IDENTITY_ID,
        created="2016-04-06T20:03:48.000Z",
        modified="2016-04-06T20:03:48.000Z",
        labels=["remote-access"],
        name="VNC",
    )

    assert tool.serialize(pretty=True) == EXPECTED


@pytest.mark.parametrize(
    "data", [
        EXPECTED,
        {
            "created": "2016-04-06T20:03:48Z",
            "created_by_ref": IDENTITY_ID,
            "id": TOOL_ID,
            "modified": "2016-04-06T20:03:48Z",
            "labels": ["remote-access"],
            "name": "VNC",
            "type": "tool",
        },
    ],
)
def test_parse_tool(data):
    tool = misp_lib_stix2.parse(data, version="2.0")

    assert tool.type == 'tool'
    assert tool.id == TOOL_ID
    assert tool.created == dt.datetime(2016, 4, 6, 20, 3, 48, tzinfo=pytz.utc)
    assert tool.modified == dt.datetime(2016, 4, 6, 20, 3, 48, tzinfo=pytz.utc)
    assert tool.created_by_ref == IDENTITY_ID
    assert tool.labels == ["remote-access"]
    assert tool.name == "VNC"


def test_tool_no_workbench_wrappers():
    tool = misp_lib_stix2.v20.Tool(name='VNC', labels=['remote-access'])
    with pytest.raises(AttributeError):
        tool.created_by()


def test_tool_serialize_with_defaults():
    tool = misp_lib_stix2.v20.Tool(
        id=TOOL_ID,
        created_by_ref=IDENTITY_ID,
        created="2016-04-06T20:03:48.000Z",
        modified="2016-04-06T20:03:48.000Z",
        labels=["remote-access"],
        name="VNC",
    )

    assert tool.serialize(pretty=True, include_optional_defaults=True) == EXPECTED_WITH_REVOKED


# TODO: Add other examples
