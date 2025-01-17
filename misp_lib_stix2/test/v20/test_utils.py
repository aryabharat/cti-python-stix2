# -*- coding: utf-8 -*-

import datetime as dt
from io import StringIO

import pytest
import pytz

import misp_lib_stix2.serialization
import misp_lib_stix2.utils

from .constants import IDENTITY_ID

amsterdam = pytz.timezone('Europe/Amsterdam')
eastern = pytz.timezone('US/Eastern')


@pytest.mark.parametrize(
    'dttm, timestamp', [
        (dt.datetime(2017, 1, 1, tzinfo=pytz.utc), '2017-01-01T00:00:00Z'),
        (amsterdam.localize(dt.datetime(2017, 1, 1)), '2016-12-31T23:00:00Z'),
        (eastern.localize(dt.datetime(2017, 1, 1, 12, 34, 56)), '2017-01-01T17:34:56Z'),
        (eastern.localize(dt.datetime(2017, 7, 1)), '2017-07-01T04:00:00Z'),
        (dt.datetime(2017, 7, 1), '2017-07-01T00:00:00Z'),
        (dt.datetime(2017, 7, 1, 0, 0, 0, 1), '2017-07-01T00:00:00.000001Z'),
        (misp_lib_stix2.utils.STIXdatetime(2017, 7, 1, 0, 0, 0, 1, precision='millisecond'), '2017-07-01T00:00:00.000Z'),
        (misp_lib_stix2.utils.STIXdatetime(2017, 7, 1, 0, 0, 0, 1, precision='second'), '2017-07-01T00:00:00Z'),
    ],
)
def test_timestamp_formatting(dttm, timestamp):
    assert misp_lib_stix2.utils.format_datetime(dttm) == timestamp


@pytest.mark.parametrize(
    'timestamp, dttm', [
        (dt.datetime(2017, 1, 1, 0, tzinfo=pytz.utc), dt.datetime(2017, 1, 1, 0, 0, 0, tzinfo=pytz.utc)),
        (dt.date(2017, 1, 1), dt.datetime(2017, 1, 1, 0, 0, 0, tzinfo=pytz.utc)),
        ('2017-01-01T00:00:00Z', dt.datetime(2017, 1, 1, 0, 0, 0, tzinfo=pytz.utc)),
    ],
)
def test_parse_datetime(timestamp, dttm):
    assert misp_lib_stix2.utils.parse_into_datetime(timestamp) == dttm


@pytest.mark.parametrize(
    'timestamp, dttm, precision', [
        ('2017-01-01T01:02:03.000001Z', dt.datetime(2017, 1, 1, 1, 2, 3, 0, tzinfo=pytz.utc), 'millisecond'),
        ('2017-01-01T01:02:03.001Z', dt.datetime(2017, 1, 1, 1, 2, 3, 1000, tzinfo=pytz.utc), 'millisecond'),
        ('2017-01-01T01:02:03.1Z', dt.datetime(2017, 1, 1, 1, 2, 3, 100000, tzinfo=pytz.utc), 'millisecond'),
        ('2017-01-01T01:02:03.45Z', dt.datetime(2017, 1, 1, 1, 2, 3, 450000, tzinfo=pytz.utc), 'millisecond'),
        ('2017-01-01T01:02:03.45Z', dt.datetime(2017, 1, 1, 1, 2, 3, tzinfo=pytz.utc), 'second'),
    ],
)
def test_parse_datetime_precision(timestamp, dttm, precision):
    assert misp_lib_stix2.utils.parse_into_datetime(timestamp, precision) == dttm


@pytest.mark.parametrize(
    'ts', [
        'foobar',
        1,
    ],
)
def test_parse_datetime_invalid(ts):
    with pytest.raises(ValueError):
        misp_lib_stix2.utils.parse_into_datetime('foobar')


@pytest.mark.parametrize(
    'data', [
        {"a": 1},
        '{"a": 1}',
        StringIO(u'{"a": 1}'),
        [("a", 1)],
    ],
)
def test_get_dict(data):
    assert misp_lib_stix2.utils._get_dict(data)


@pytest.mark.parametrize(
    'data', [
        1,
        [1],
        ['a', 1],
        "foobar",
    ],
)
def test_get_dict_invalid(data):
    with pytest.raises(ValueError):
        misp_lib_stix2.utils._get_dict(data)


@pytest.mark.parametrize(
    'stix_id, type', [
        ('malware--d69c8146-ab35-4d50-8382-6fc80e641d43', 'malware'),
        ('intrusion-set--899ce53f-13a0-479b-a0e4-67d46e241542', 'intrusion-set'),
    ],
)
def test_get_type_from_id(stix_id, type):
    assert misp_lib_stix2.utils.get_type_from_id(stix_id) == type


def test_deduplicate(stix_objs1):
    unique = misp_lib_stix2.utils.deduplicate(stix_objs1)

    # Only 3 objects are unique
    # 2 id's vary
    # 2 modified times vary for a particular id

    assert len(unique) == 3

    ids = [obj['id'] for obj in unique]
    mods = [obj['modified'] for obj in unique]

    assert "indicator--00000000-0000-4000-8000-000000000001" in ids
    assert "indicator--00000000-0000-4000-8000-000000000002" in ids
    assert "2017-01-27T13:49:53.935Z" in mods
    assert "2017-01-27T13:49:53.936Z" in mods


@pytest.mark.parametrize(
    'object, tuple_to_find, expected_index', [
        (
            misp_lib_stix2.v20.ObservedData(
                id="observed-data--b67d30ff-02ac-498a-92f9-32f845f448cf",
                created_by_ref=IDENTITY_ID,
                created="2016-04-06T19:58:16.000Z",
                modified="2016-04-06T19:58:16.000Z",
                first_observed="2015-12-21T19:00:00Z",
                last_observed="2015-12-21T19:00:00Z",
                number_observed=50,
                objects={
                    "0": {
                        "name": "foo.exe",
                        "type": "file",
                    },
                    "1": {
                        "type": "ipv4-addr",
                        "value": "198.51.100.3",
                    },
                    "2": {
                        "type": "network-traffic",
                        "src_ref": "1",
                        "protocols": [
                            "tcp",
                            "http",
                        ],
                        "extensions": {
                            "http-request-ext": {
                                "request_method": "get",
                                "request_value": "/download.html",
                                "request_version": "http/1.1",
                                "request_header": {
                                    "Accept-Encoding": "gzip,deflate",
                                    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6) Gecko/20040113",
                                    "Host": "www.example.com",
                                },
                            },
                        },
                    },
                },
            ), ('1', {"type": "ipv4-addr", "value": "198.51.100.3"}), 1,
        ),
        (
            {
                "type": "x-example",
                "id": "x-example--d5413db2-c26c-42e0-b0e0-ec800a310bfb",
                "created": "2018-06-11T01:25:22.063Z",
                "modified": "2018-06-11T01:25:22.063Z",
                "dictionary": {
                    "key": {
                        "key_one": "value",
                        "key_two": "value",
                    },
                },
            }, ('key', {'key_one': 'value', 'key_two': 'value'}), 0,
        ),
        (
            {
                "type": "language-content",
                "id": "language-content--b86bd89f-98bb-4fa9-8cb2-9ad421da981d",
                "created": "2017-02-08T21:31:22.007Z",
                "modified": "2017-02-08T21:31:22.007Z",
                "object_ref": "campaign--12a111f0-b824-4baf-a224-83b80237a094",
                "object_modified": "2017-02-08T21:31:22.007Z",
                "contents": {
                    "de": {
                        "name": "Bank Angriff 1",
                        "description": "Weitere Informationen über Banküberfall",
                    },
                    "fr": {
                        "name": "Attaque Bank 1",
                        "description": "Plus d'informations sur la crise bancaire",
                    },
                },
            }, ('fr', {"name": "Attaque Bank 1", "description": "Plus d'informations sur la crise bancaire"}), 1,
        ),
    ],
)
def test_find_property_index(object, tuple_to_find, expected_index):
    assert misp_lib_stix2.serialization.find_property_index(
        object,
        *tuple_to_find
    ) == expected_index


@pytest.mark.parametrize(
    'dict_value, tuple_to_find, expected_index', [
        (
            {
                "contents": {
                    "de": {
                        "name": "Bank Angriff 1",
                        "description": "Weitere Informationen über Banküberfall",
                    },
                    "fr": {
                        "name": "Attaque Bank 1",
                        "description": "Plus d'informations sur la crise bancaire",
                    },
                    "es": {
                        "name": "Ataque al Banco",
                        "description": "Mas informacion sobre el ataque al banco",
                    },
                },
            }, ('es', {"name": "Ataque al Banco", "description": "Mas informacion sobre el ataque al banco"}), 1,
        ),  # Sorted alphabetically
        (
            {
                'my_list': [
                    {"key_one": 1},
                    {"key_two": 2},
                ],
            }, ('key_one', 1), 0,
        ),
    ],
)
def test_iterate_over_values(dict_value, tuple_to_find, expected_index):
    assert misp_lib_stix2.serialization._find_property_in_seq(dict_value.values(), *tuple_to_find) == expected_index


@pytest.mark.parametrize(
    "type_", [
        "attack-pattern",
        "campaign",
        "course-of-action",
        "identity",
        "indicator",
        "intrusion-set",
        "malware",
        "observed-data",
        "report",
        "threat-actor",
        "tool",
        "vulnerability",
    ],
)
def test_is_sdo_dict(type_):
    d = {
        "type": type_,
    }
    assert misp_lib_stix2.utils.is_sdo(d, "2.0")


@pytest.mark.parametrize(
    "dict_", [
        {"type": "software", "spec_version": "2.1"},
        {"type": "software"},
        {"type": "identity", "spec_version": "2.1"},
        {"type": "marking-definition", "spec_version": "2.1"},
        {"type": "marking-definition"},
        {"type": "bundle", "spec_version": "2.1"},
        {"type": "bundle"},
        {"type": "language-content", "spec_version": "2.1"},
        {"type": "language-content"},
        {"type": "relationship", "spec_version": "2.1"},
        {"type": "relationship"},
        {"type": "foo", "spec_version": "2.1"},
        {"type": "foo"},
    ],
)
def test_is_not_sdo_dict(dict_):
    assert not misp_lib_stix2.utils.is_sdo(dict_, "2.0")


def test_is_sco_dict():
    d = {
        "type": "file",
    }

    assert misp_lib_stix2.utils.is_sco(d, "2.0")


@pytest.mark.parametrize(
    "dict_", [
        {"type": "identity"},
        {"type": "identity", "spec_version": "2.1"},
        {"type": "software", "spec_version": "2.1"},
        {"type": "marking-definition", "spec_version": "2.1"},
        {"type": "marking-definition"},
        {"type": "bundle", "spec_version": "2.1"},
        {"type": "bundle"},
        {"type": "language-content", "spec_version": "2.1"},
        {"type": "language-content"},
        {"type": "relationship", "spec_version": "2.1"},
        {"type": "relationship"},
        {"type": "foo", "spec_version": "2.1"},
        {"type": "foo"},
    ],
)
def test_is_not_sco_dict(dict_):
    assert not misp_lib_stix2.utils.is_sco(dict_, "2.0")


@pytest.mark.parametrize(
    "dict_", [
        {"type": "relationship"},
        {"type": "sighting"},
    ],
)
def test_is_sro_dict(dict_):
    assert misp_lib_stix2.utils.is_sro(dict_, "2.0")


@pytest.mark.parametrize(
    "dict_", [
        {"type": "identity", "spec_version": "2.1"},
        {"type": "identity"},
        {"type": "software", "spec_version": "2.1"},
        {"type": "software"},
        {"type": "marking-definition", "spec_version": "2.1"},
        {"type": "marking-definition"},
        {"type": "bundle", "spec_version": "2.1"},
        {"type": "bundle"},
        {"type": "language-content", "spec_version": "2.1"},
        {"type": "language-content"},
        {"type": "relationship", "spec_version": "2.1"},
        {"type": "sighting", "spec_version": "2.1"},
        {"type": "foo", "spec_version": "2.1"},
        {"type": "foo"},
    ],
)
def test_is_not_sro_dict(dict_):
    assert not misp_lib_stix2.utils.is_sro(dict_, "2.0")


@pytest.mark.parametrize(
    "dict_", [
        {"type": "identity"},
        {"type": "software"},
        {"type": "marking-definition"},
        # Presence of spec_version property implies a STIX 2.0 bundle,
        # regardless of the property's value.  STIX 2.1 bundles don't have a
        # "spec_version" property defined.
        {"type": "bundle", "spec_version": "2.1"},
        {
            "type": "bundle",
            "id": "bundle--8f431680-6278-4767-ba43-5edb682d7086",
            "spec_version": "2.0",
            "objects": [
                {"type": "identity"},
                {"type": "software"},
                {"type": "marking-definition"},
            ],
        },
    ],
)
def test_is_object_dict(dict_):
    assert misp_lib_stix2.utils.is_object(dict_, "2.0")


@pytest.mark.parametrize(
    "dict_", [
        {"type": "identity", "spec_version": "2.1"},
        {"type": "software", "spec_version": "2.1"},
        {"type": "marking-definition", "spec_version": "2.1"},
        {"type": "language-content", "spec_version": "2.1"},
        {"type": "relationship", "spec_version": "2.1"},
        {"type": "sighting", "spec_version": "2.1"},
        {"type": "foo", "spec_version": "2.1"},
        {"type": "foo"},
        {
            "type": "bundle",
            "id": "bundle--8f431680-6278-4767-ba43-5edb682d7086",
            "objects": [
                {"type": "identity"},
                {"type": "software"},
                {"type": "marking-definition"},
            ],
        },
    ],
)
def test_is_not_object_dict(dict_):
    assert not misp_lib_stix2.utils.is_object(dict_, "2.0")
