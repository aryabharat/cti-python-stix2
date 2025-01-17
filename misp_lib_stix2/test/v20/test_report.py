import datetime as dt

import pytest
import pytz

import misp_lib_stix2
from misp_lib_stix2.exceptions import InvalidValueError

from .constants import (
    CAMPAIGN_ID, IDENTITY_ID, INDICATOR_ID, INDICATOR_KWARGS, RELATIONSHIP_ID,
    REPORT_ID,
)

EXPECTED = """{
    "type": "report",
    "id": "report--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
    "created_by_ref": "identity--311b2d2d-f010-4473-83ec-1edf84858f4c",
    "created": "2015-12-21T19:59:11.000Z",
    "modified": "2015-12-21T19:59:11.000Z",
    "name": "The Black Vine Cyberespionage Group",
    "description": "A simple report with an indicator and campaign",
    "published": "2016-01-20T17:00:00Z",
    "object_refs": [
        "indicator--a740531e-63ff-4e49-a9e1-a0a3eed0e3e7",
        "campaign--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
        "relationship--df7c87eb-75d2-4948-af81-9d49d246f301"
    ],
    "labels": [
        "campaign"
    ]
}"""


def test_report_example():
    report = misp_lib_stix2.v20.Report(
        id=REPORT_ID,
        created_by_ref=IDENTITY_ID,
        created="2015-12-21T19:59:11.000Z",
        modified="2015-12-21T19:59:11.000Z",
        name="The Black Vine Cyberespionage Group",
        description="A simple report with an indicator and campaign",
        published="2016-01-20T17:00:00Z",
        labels=["campaign"],
        object_refs=[
            INDICATOR_ID,
            CAMPAIGN_ID,
            RELATIONSHIP_ID,
        ],
    )

    assert report.serialize(pretty=True) == EXPECTED


def test_report_example_objects_in_object_refs():
    report = misp_lib_stix2.v20.Report(
        id=REPORT_ID,
        created_by_ref=IDENTITY_ID,
        created="2015-12-21T19:59:11.000Z",
        modified="2015-12-21T19:59:11.000Z",
        name="The Black Vine Cyberespionage Group",
        description="A simple report with an indicator and campaign",
        published="2016-01-20T17:00:00Z",
        labels=["campaign"],
        object_refs=[
            misp_lib_stix2.v20.Indicator(id=INDICATOR_ID, **INDICATOR_KWARGS),
            CAMPAIGN_ID,
            RELATIONSHIP_ID,
        ],
    )

    assert report.serialize(pretty=True) == EXPECTED


def test_report_example_objects_in_object_refs_with_bad_id():
    with pytest.raises(misp_lib_stix2.exceptions.InvalidValueError) as excinfo:
        misp_lib_stix2.v20.Report(
            id=REPORT_ID,
            created_by_ref=IDENTITY_ID,
            created="2015-12-21T19:59:11.000Z",
            modified="2015-12-21T19:59:11.000Z",
            name="The Black Vine Cyberespionage Group",
            description="A simple report with an indicator and campaign",
            published="2016-01-20T17:00:00Z",
            labels=["campaign"],
            object_refs=[
                misp_lib_stix2.v20.Indicator(id=INDICATOR_ID, **INDICATOR_KWARGS),
                "campaign-83422c77-904c-4dc1-aff5-5c38f3a2c55c",   # the "bad" id, missing a "-"
                RELATIONSHIP_ID,
            ],
        )

    assert excinfo.value.cls == misp_lib_stix2.v20.Report
    assert excinfo.value.prop_name == "object_refs"


@pytest.mark.parametrize(
    "data", [
        EXPECTED,
        {
            "created": "2015-12-21T19:59:11.000Z",
            "created_by_ref": IDENTITY_ID,
            "description": "A simple report with an indicator and campaign",
            "id": REPORT_ID,
            "labels": [
                "campaign",
            ],
            "modified": "2015-12-21T19:59:11.000Z",
            "name": "The Black Vine Cyberespionage Group",
            "object_refs": [
                INDICATOR_ID,
                CAMPAIGN_ID,
                RELATIONSHIP_ID,
            ],
            "published": "2016-01-20T17:00:00Z",
            "type": "report",
        },
    ],
)
def test_parse_report(data):
    rept = misp_lib_stix2.parse(data, version="2.0")

    assert rept.type == 'report'
    assert rept.id == REPORT_ID
    assert rept.created == dt.datetime(2015, 12, 21, 19, 59, 11, tzinfo=pytz.utc)
    assert rept.modified == dt.datetime(2015, 12, 21, 19, 59, 11, tzinfo=pytz.utc)
    assert rept.created_by_ref == IDENTITY_ID
    assert rept.object_refs == [
        INDICATOR_ID,
        CAMPAIGN_ID,
        RELATIONSHIP_ID,
    ]
    assert rept.description == "A simple report with an indicator and campaign"
    assert rept.labels == ["campaign"]
    assert rept.name == "The Black Vine Cyberespionage Group"

# TODO: Add other examples


def test_report_on_custom():
    with pytest.raises(InvalidValueError):
        misp_lib_stix2.v20.Report(
            name="my report",
            labels=["a label"],
            published="2016-01-20T17:00:00Z",
            object_refs=[
                "indicator--a740531e-63ff-4e49-a9e1-a0a3eed0e3e7",
                "some-type--2672975a-ce1e-4473-a1c6-0d79868930c7",
            ],
        )

    report = misp_lib_stix2.v20.Report(
        name="my report",
        labels=["a label"],
        published="2016-01-20T17:00:00Z",
        object_refs=[
            "indicator--a740531e-63ff-4e49-a9e1-a0a3eed0e3e7",
            "some-type--2672975a-ce1e-4473-a1c6-0d79868930c7",
        ],
        allow_custom=True,
    )

    assert "some-type--2672975a-ce1e-4473-a1c6-0d79868930c7" \
        in report.object_refs
