import datetime as dt

import pytest
import pytz

import misp_lib_stix2

from .constants import IDENTITY_ID

EXPECTED = """{
    "type": "identity",
    "id": "identity--311b2d2d-f010-4473-83ec-1edf84858f4c",
    "created": "2015-12-21T19:59:11.000Z",
    "modified": "2015-12-21T19:59:11.000Z",
    "name": "John Smith",
    "identity_class": "individual"
}"""


def test_identity_example():
    identity = misp_lib_stix2.v20.Identity(
        id=IDENTITY_ID,
        created="2015-12-21T19:59:11.000Z",
        modified="2015-12-21T19:59:11.000Z",
        name="John Smith",
        identity_class="individual",
    )

    assert identity.serialize(pretty=True) == EXPECTED


@pytest.mark.parametrize(
    "data", [
        EXPECTED,
        {
            "created": "2015-12-21T19:59:11.000Z",
            "id": IDENTITY_ID,
            "identity_class": "individual",
            "modified": "2015-12-21T19:59:11.000Z",
            "name": "John Smith",
            "type": "identity",
        },
    ],
)
def test_parse_identity(data):
    identity = misp_lib_stix2.parse(data, version="2.0")

    assert identity.type == 'identity'
    assert identity.id == IDENTITY_ID
    assert identity.created == dt.datetime(2015, 12, 21, 19, 59, 11, tzinfo=pytz.utc)
    assert identity.modified == dt.datetime(2015, 12, 21, 19, 59, 11, tzinfo=pytz.utc)
    assert identity.name == "John Smith"


def test_parse_no_type():
    with pytest.raises(misp_lib_stix2.exceptions.ParseError):
        misp_lib_stix2.parse(
            """
        {
            "id": "identity--311b2d2d-f010-4473-83ec-1edf84858f4c",
            "created": "2015-12-21T19:59:11.000Z",
            "modified": "2015-12-21T19:59:11.000Z",
            "name": "John Smith",
            "identity_class": "individual"
        }""", version="2.0",
        )


def test_identity_with_custom():
    identity = misp_lib_stix2.v20.Identity(
        name="John Smith",
        identity_class="individual",
        custom_properties={'x_foo': 'bar'},
    )

    assert identity.x_foo == "bar"
    assert "x_foo" in identity

# TODO: Add other examples
