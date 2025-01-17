import uuid

import pytest

import misp_lib_stix2

from .constants import (
    FAKE_TIME, INDICATOR_KWARGS, MALWARE_KWARGS, RELATIONSHIP_KWARGS,
)


# Inspired by: http://stackoverflow.com/a/24006251
@pytest.fixture
def clock(monkeypatch):

    class mydatetime(misp_lib_stix2.utils.STIXdatetime):
        @classmethod
        def now(cls, tz=None):
            return FAKE_TIME

    monkeypatch.setattr(misp_lib_stix2.utils, 'STIXdatetime', mydatetime)


@pytest.fixture
def uuid4(monkeypatch):
    def wrapper():
        data = [0]

        def wrapped():
            data[0] += 1
            return "00000000-0000-4000-8000-00000000%04x" % data[0]

        return wrapped
    monkeypatch.setattr(uuid, "uuid4", wrapper())


@pytest.fixture
def indicator(uuid4, clock):
    return misp_lib_stix2.v20.Indicator(**INDICATOR_KWARGS)


@pytest.fixture
def malware(uuid4, clock):
    return misp_lib_stix2.v20.Malware(**MALWARE_KWARGS)


@pytest.fixture
def relationship(uuid4, clock):
    return misp_lib_stix2.v20.Relationship(**RELATIONSHIP_KWARGS)


@pytest.fixture
def stix_objs1():
    ind1 = {
        "created": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000001",
        "labels": [
            "malicious-activity",
        ],
        "modified": "2017-01-27T13:49:53.935Z",
        "name": "Malicious site hosting downloader",
        "pattern": "[url:value = 'http://x4z9arb.cn/4712']",
        "type": "indicator",
        "valid_from": "2017-01-27T13:49:53.935382Z",
    }
    ind2 = {
        "created": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000001",
        "labels": [
            "malicious-activity",
        ],
        "modified": "2017-01-27T13:49:53.935Z",
        "name": "Malicious site hosting downloader",
        "pattern": "[url:value = 'http://x4z9arb.cn/4712']",
        "type": "indicator",
        "valid_from": "2017-01-27T13:49:53.935382Z",
    }
    ind3 = {
        "created": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000001",
        "labels": [
            "malicious-activity",
        ],
        "modified": "2017-01-27T13:49:53.936Z",
        "name": "Malicious site hosting downloader",
        "pattern": "[url:value = 'http://x4z9arb.cn/4712']",
        "type": "indicator",
        "valid_from": "2017-01-27T13:49:53.935382Z",
    }
    ind4 = {
        "created": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000002",
        "labels": [
            "malicious-activity",
        ],
        "modified": "2017-01-27T13:49:53.935Z",
        "name": "Malicious site hosting downloader",
        "pattern": "[url:value = 'http://x4z9arb.cn/4712']",
        "type": "indicator",
        "valid_from": "2017-01-27T13:49:53.935382Z",
    }
    ind5 = {
        "created": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000002",
        "labels": [
            "malicious-activity",
        ],
        "modified": "2017-01-27T13:49:53.935Z",
        "name": "Malicious site hosting downloader",
        "pattern": "[url:value = 'http://x4z9arb.cn/4712']",
        "type": "indicator",
        "valid_from": "2017-01-27T13:49:53.935382Z",
    }
    return [ind1, ind2, ind3, ind4, ind5]


@pytest.fixture
def stix_objs1_manifests():
    # Tests against latest medallion (TAXII 2.1)
    ind1 = {
        "date_added": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000001",
        "media_type": "application/stix+json;version=2.1",
        "version": "2017-01-27T13:49:53.935Z",
    }
    ind2 = {
        "date_added": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000001",
        "media_type": "application/stix+json;version=2.1",
        "version": "2017-01-27T13:49:53.935Z",
    }
    ind3 = {
        "date_added": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000001",
        "media_type": "application/stix+json;version=2.1",
        "version": "2017-01-27T13:49:53.936Z",
    }
    ind4 = {
        "date_added": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000002",
        "media_type": "application/stix+json;version=2.1",
        "version": "2017-01-27T13:49:53.935Z",
    }
    ind5 = {
        "date_added": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000002",
        "media_type": "application/stix+json;version=2.1",
        "version": "2017-01-27T13:49:53.935Z",
    }
    return [ind1, ind2, ind3, ind4, ind5]


@pytest.fixture
def stix_objs2():
    ind6 = {
        "created": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000001",
        "labels": [
            "malicious-activity",
        ],
        "modified": "2017-01-31T13:49:53.935Z",
        "name": "Malicious site hosting downloader",
        "pattern": "[url:value = 'http://x4z9arb.cn/4712']",
        "type": "indicator",
        "valid_from": "2017-01-27T13:49:53.935382Z",
    }
    ind7 = {
        "created": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000002",
        "labels": [
            "malicious-activity",
        ],
        "modified": "2017-01-27T13:49:53.935Z",
        "name": "Malicious site hosting downloader",
        "pattern": "[url:value = 'http://x4z9arb.cn/4712']",
        "type": "indicator",
        "valid_from": "2017-01-27T13:49:53.935382Z",
    }
    ind8 = {
        "created": "2017-01-27T13:49:53.935Z",
        "id": "indicator--00000000-0000-4000-8000-000000000002",
        "labels": [
            "malicious-activity",
        ],
        "modified": "2017-01-27T13:49:53.935Z",
        "name": "Malicious site hosting downloader",
        "pattern": "[url:value = 'http://x4z9arb.cn/4712']",
        "type": "indicator",
        "valid_from": "2017-01-27T13:49:53.935382Z",
    }
    return [ind6, ind7, ind8]


@pytest.fixture
def real_stix_objs2(stix_objs2):
    return [misp_lib_stix2.parse(x, version="2.0") for x in stix_objs2]
