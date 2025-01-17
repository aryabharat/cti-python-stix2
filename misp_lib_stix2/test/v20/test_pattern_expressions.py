import datetime

import pytest
import pytz

import misp_lib_stix2
from misp_lib_stix2.pattern_visitor import create_pattern_object
import misp_lib_stix2.patterns
import misp_lib_stix2.utils

# flake8 does not approve of star imports.
# flake8: noqa: F405
from .pattern_ast_overrides import *


def test_create_comparison_expression():
    exp = misp_lib_stix2.EqualityComparisonExpression(
        "file:hashes.'SHA-256'",
        misp_lib_stix2.HashConstant("aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f", "SHA-256"),
    )   # noqa

    assert str(exp) == "file:hashes.'SHA-256' = 'aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f'"


def test_boolean_expression():
    exp1 = misp_lib_stix2.MatchesComparisonExpression(
        "email-message:from_ref.value",
        misp_lib_stix2.StringConstant(".+\\@example\\.com$"),
    )
    exp2 = misp_lib_stix2.MatchesComparisonExpression(
        "email-message:body_multipart[*].body_raw_ref.name",
        misp_lib_stix2.StringConstant("^Final Report.+\\.exe$"),
    )
    exp = misp_lib_stix2.AndBooleanExpression([exp1, exp2])

    assert str(exp) == "email-message:from_ref.value MATCHES '.+\\\\@example\\\\.com$' AND email-message:body_multipart[*].body_raw_ref.name MATCHES '^Final Report.+\\\\.exe$'"  # noqa


def test_boolean_expression_with_parentheses():
    exp1 = misp_lib_stix2.MatchesComparisonExpression(
        misp_lib_stix2.ObjectPath(
            "email-message",
            [
                misp_lib_stix2.ReferenceObjectPathComponent("from_ref"),
                misp_lib_stix2.BasicObjectPathComponent("value", False),
            ],
        ),
        misp_lib_stix2.StringConstant(".+\\@example\\.com$"),
    )
    exp2 = misp_lib_stix2.MatchesComparisonExpression(
        "email-message:body_multipart[*].body_raw_ref.name",
        misp_lib_stix2.StringConstant("^Final Report.+\\.exe$"),
    )
    exp = misp_lib_stix2.ParentheticalExpression(misp_lib_stix2.AndBooleanExpression([exp1, exp2]))
    assert str(exp) == "(email-message:from_ref.value MATCHES '.+\\\\@example\\\\.com$' AND email-message:body_multipart[*].body_raw_ref.name MATCHES '^Final Report.+\\\\.exe$')"  # noqa


def test_hash_followed_by_registryKey_expression_python_constant():
    hash_exp = misp_lib_stix2.EqualityComparisonExpression(
        "file:hashes.MD5",
        misp_lib_stix2.HashConstant("79054025255fb1a26e4bc422aef54eb4", "MD5"),
    )
    o_exp1 = misp_lib_stix2.ObservationExpression(hash_exp)
    reg_exp = misp_lib_stix2.EqualityComparisonExpression(
        misp_lib_stix2.ObjectPath("windows-registry-key", ["key"]),
        misp_lib_stix2.StringConstant("HKEY_LOCAL_MACHINE\\foo\\bar"),
    )
    o_exp2 = misp_lib_stix2.ObservationExpression(reg_exp)
    fb_exp = misp_lib_stix2.FollowedByObservationExpression([o_exp1, o_exp2])
    para_exp = misp_lib_stix2.ParentheticalExpression(fb_exp)
    qual_exp = misp_lib_stix2.WithinQualifier(300)
    exp = misp_lib_stix2.QualifiedObservationExpression(para_exp, qual_exp)
    assert str(exp) == "([file:hashes.MD5 = '79054025255fb1a26e4bc422aef54eb4'] FOLLOWEDBY [windows-registry-key:key = 'HKEY_LOCAL_MACHINE\\\\foo\\\\bar']) WITHIN 300 SECONDS"  # noqa


def test_hash_followed_by_registryKey_expression():
    hash_exp = misp_lib_stix2.EqualityComparisonExpression(
        "file:hashes.MD5",
        misp_lib_stix2.HashConstant("79054025255fb1a26e4bc422aef54eb4", "MD5"),
    )
    o_exp1 = misp_lib_stix2.ObservationExpression(hash_exp)
    reg_exp = misp_lib_stix2.EqualityComparisonExpression(
        misp_lib_stix2.ObjectPath("windows-registry-key", ["key"]),
        misp_lib_stix2.StringConstant("HKEY_LOCAL_MACHINE\\foo\\bar"),
    )
    o_exp2 = misp_lib_stix2.ObservationExpression(reg_exp)
    fb_exp = misp_lib_stix2.FollowedByObservationExpression([o_exp1, o_exp2])
    para_exp = misp_lib_stix2.ParentheticalExpression(fb_exp)
    qual_exp = misp_lib_stix2.WithinQualifier(misp_lib_stix2.IntegerConstant(300))
    exp = misp_lib_stix2.QualifiedObservationExpression(para_exp, qual_exp)
    assert str(exp) == "([file:hashes.MD5 = '79054025255fb1a26e4bc422aef54eb4'] FOLLOWEDBY [windows-registry-key:key = 'HKEY_LOCAL_MACHINE\\\\foo\\\\bar']) WITHIN 300 SECONDS"  # noqa


def test_file_observable_expression():
    exp1 = misp_lib_stix2.EqualityComparisonExpression(
        "file:hashes.'SHA-256'",
        misp_lib_stix2.HashConstant(
            "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f",
            'SHA-256',
        ),
    )
    exp2 = misp_lib_stix2.EqualityComparisonExpression("file:mime_type", misp_lib_stix2.StringConstant("application/x-pdf"))
    bool_exp = misp_lib_stix2.ObservationExpression(misp_lib_stix2.AndBooleanExpression([exp1, exp2]))
    assert str(bool_exp) == "[file:hashes.'SHA-256' = 'aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f' AND file:mime_type = 'application/x-pdf']"  # noqa


@pytest.mark.parametrize(
    "observation_class, op", [
        (misp_lib_stix2.AndObservationExpression, 'AND'),
        (misp_lib_stix2.OrObservationExpression, 'OR'),
    ],
)
def test_multiple_file_observable_expression(observation_class, op):
    exp1 = misp_lib_stix2.EqualityComparisonExpression(
        "file:hashes.'SHA-256'",
        misp_lib_stix2.HashConstant(
            "bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c",
            'SHA-256',
        ),
    )
    exp2 = misp_lib_stix2.EqualityComparisonExpression(
        "file:hashes.MD5",
        misp_lib_stix2.HashConstant("cead3f77f6cda6ec00f57d76c9a6879f", "MD5"),
    )
    bool1_exp = misp_lib_stix2.OrBooleanExpression([exp1, exp2])
    exp3 = misp_lib_stix2.EqualityComparisonExpression(
        "file:hashes.'SHA-256'",
        misp_lib_stix2.HashConstant(
            "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f",
            'SHA-256',
        ),
    )
    op1_exp = misp_lib_stix2.ObservationExpression(bool1_exp)
    op2_exp = misp_lib_stix2.ObservationExpression(exp3)
    exp = observation_class([op1_exp, op2_exp])
    assert str(exp) == "[file:hashes.'SHA-256' = 'bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c' OR file:hashes.MD5 = 'cead3f77f6cda6ec00f57d76c9a6879f'] {} [file:hashes.'SHA-256' = 'aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f']".format(op)  # noqa


def test_root_types():
    ast = misp_lib_stix2.ObservationExpression(
            misp_lib_stix2.AndBooleanExpression(
                [
                    misp_lib_stix2.ParentheticalExpression(
                       misp_lib_stix2.OrBooleanExpression([
                           misp_lib_stix2.EqualityComparisonExpression("a:b", misp_lib_stix2.StringConstant("1")),
                           misp_lib_stix2.EqualityComparisonExpression("b:c", misp_lib_stix2.StringConstant("2")),
                       ]),
                    ),
                    misp_lib_stix2.EqualityComparisonExpression(u"b:d", misp_lib_stix2.StringConstant("3")),
                ],
            ),
    )
    assert str(ast) == "[(a:b = '1' OR b:c = '2') AND b:d = '3']"


def test_artifact_payload():
    exp1 = misp_lib_stix2.EqualityComparisonExpression(
        "artifact:mime_type",
        "application/vnd.tcpdump.pcap",
    )
    exp2 = misp_lib_stix2.MatchesComparisonExpression(
        "artifact:payload_bin",
        misp_lib_stix2.StringConstant("\\xd4\\xc3\\xb2\\xa1\\x02\\x00\\x04\\x00"),
    )
    and_exp = misp_lib_stix2.ObservationExpression(misp_lib_stix2.AndBooleanExpression([exp1, exp2]))
    assert str(and_exp) == "[artifact:mime_type = 'application/vnd.tcpdump.pcap' AND artifact:payload_bin MATCHES '\\\\xd4\\\\xc3\\\\xb2\\\\xa1\\\\x02\\\\x00\\\\x04\\\\x00']"  # noqa


def test_greater_than_python_constant():
    exp1 = misp_lib_stix2.GreaterThanComparisonExpression("file:extensions.'windows-pebinary-ext'.sections[*].entropy", 7.0)
    exp = misp_lib_stix2.ObservationExpression(exp1)
    assert str(exp) == "[file:extensions.'windows-pebinary-ext'.sections[*].entropy > 7.0]"


def test_greater_than():
    exp1 = misp_lib_stix2.GreaterThanComparisonExpression(
        "file:extensions.'windows-pebinary-ext'.sections[*].entropy",
        misp_lib_stix2.FloatConstant(7.0),
    )
    exp = misp_lib_stix2.ObservationExpression(exp1)
    assert str(exp) == "[file:extensions.'windows-pebinary-ext'.sections[*].entropy > 7.0]"


def test_less_than():
    exp = misp_lib_stix2.LessThanComparisonExpression("file:size", 1024)
    assert str(exp) == "file:size < 1024"


def test_greater_than_or_equal():
    exp = misp_lib_stix2.GreaterThanEqualComparisonExpression(
        "file:size",
        1024,
    )

    assert str(exp) == "file:size >= 1024"


def test_less_than_or_equal():
    exp = misp_lib_stix2.LessThanEqualComparisonExpression(
        "file:size",
        1024,
    )
    assert str(exp) == "file:size <= 1024"


def test_not():
    exp = misp_lib_stix2.LessThanComparisonExpression(
        "file:size",
        1024,
        negated=True,
    )
    assert str(exp) == "file:size NOT < 1024"


def test_and_observable_expression():
    exp1 = misp_lib_stix2.AndBooleanExpression([
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:account_type",
            "unix",
        ),
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:user_id",
            misp_lib_stix2.StringConstant("1007"),
        ),
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:account_login",
            "Peter",
        ),
    ])
    exp2 = misp_lib_stix2.AndBooleanExpression([
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:account_type",
            "unix",
        ),
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:user_id",
            misp_lib_stix2.StringConstant("1008"),
        ),
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:account_login",
            "Paul",
        ),
    ])
    exp3 = misp_lib_stix2.AndBooleanExpression([
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:account_type",
            "unix",
        ),
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:user_id",
            misp_lib_stix2.StringConstant("1009"),
        ),
        misp_lib_stix2.EqualityComparisonExpression(
            "user-account:account_login",
            "Mary",
        ),
    ])
    exp = misp_lib_stix2.AndObservationExpression([
        misp_lib_stix2.ObservationExpression(exp1),
        misp_lib_stix2.ObservationExpression(exp2),
        misp_lib_stix2.ObservationExpression(exp3),
    ])
    assert str(exp) == "[user-account:account_type = 'unix' AND user-account:user_id = '1007' AND user-account:account_login = 'Peter'] AND [user-account:account_type = 'unix' AND user-account:user_id = '1008' AND user-account:account_login = 'Paul'] AND [user-account:account_type = 'unix' AND user-account:user_id = '1009' AND user-account:account_login = 'Mary']"  # noqa


def test_invalid_and_observable_expression():
    with pytest.raises(ValueError):
        misp_lib_stix2.AndBooleanExpression([
            misp_lib_stix2.EqualityComparisonExpression(
                "user-account:display_name",
                "admin",
            ),
            misp_lib_stix2.EqualityComparisonExpression(
                "email-addr:display_name",
                misp_lib_stix2.StringConstant("admin"),
            ),
        ])


def test_hex():
    exp_and = misp_lib_stix2.AndBooleanExpression([
        misp_lib_stix2.EqualityComparisonExpression(
            "file:mime_type",
            "image/bmp",
        ),
        misp_lib_stix2.EqualityComparisonExpression(
            "file:magic_number_hex",
            misp_lib_stix2.HexConstant("ffd8"),
        ),
    ])
    exp = misp_lib_stix2.ObservationExpression(exp_and)
    assert str(exp) == "[file:mime_type = 'image/bmp' AND file:magic_number_hex = h'ffd8']"


def test_multiple_qualifiers():
    exp_and = misp_lib_stix2.AndBooleanExpression([
        misp_lib_stix2.EqualityComparisonExpression(
            "network-traffic:dst_ref.type",
            "domain-name",
        ),
        misp_lib_stix2.EqualityComparisonExpression(
            "network-traffic:dst_ref.value",
            "example.com",
        ),
    ])
    exp_ob = misp_lib_stix2.ObservationExpression(exp_and)
    qual_rep = misp_lib_stix2.RepeatQualifier(5)
    qual_within = misp_lib_stix2.WithinQualifier(misp_lib_stix2.IntegerConstant(1800))
    exp = misp_lib_stix2.QualifiedObservationExpression(misp_lib_stix2.QualifiedObservationExpression(exp_ob, qual_rep), qual_within)
    assert str(exp) == "[network-traffic:dst_ref.type = 'domain-name' AND network-traffic:dst_ref.value = 'example.com'] REPEATS 5 TIMES WITHIN 1800 SECONDS"  # noqa


def test_set_op():
    exp = misp_lib_stix2.ObservationExpression(
        misp_lib_stix2.IsSubsetComparisonExpression(
            "network-traffic:dst_ref.value",
            "2001:0db8:dead:beef:0000:0000:0000:0000/64",
        ),
    )
    assert str(exp) == "[network-traffic:dst_ref.value ISSUBSET '2001:0db8:dead:beef:0000:0000:0000:0000/64']"


def test_timestamp():
    ts = misp_lib_stix2.StringConstant('2014-01-13T07:03:17Z')
    assert str(ts) == "'2014-01-13T07:03:17Z'"


def test_boolean():
    exp = misp_lib_stix2.EqualityComparisonExpression(
        "email-message:is_multipart",
        True,
    )
    assert str(exp) == "email-message:is_multipart = true"


def test_binary():
    const = misp_lib_stix2.BinaryConstant("dGhpcyBpcyBhIHRlc3Q=")
    exp = misp_lib_stix2.EqualityComparisonExpression(
        "artifact:payload_bin",
        const,
    )
    assert str(exp) == "artifact:payload_bin = b'dGhpcyBpcyBhIHRlc3Q='"


def test_list():
    exp = misp_lib_stix2.InComparisonExpression(
        "process:name",
        ['proccy', 'proximus', 'badproc'],
    )
    assert str(exp) == "process:name IN ('proccy', 'proximus', 'badproc')"


def test_list2():
    # alternate way to construct an "IN" Comparison Expression
    exp = misp_lib_stix2.EqualityComparisonExpression(
        "process:name",
        ['proccy', 'proximus', 'badproc'],
    )
    assert str(exp) == "process:name IN ('proccy', 'proximus', 'badproc')"


def test_invalid_constant_type():
    with pytest.raises(ValueError):
        misp_lib_stix2.EqualityComparisonExpression(
            "artifact:payload_bin",
            {'foo': 'bar'},
        )


def test_invalid_integer_constant():
    with pytest.raises(ValueError):
        misp_lib_stix2.IntegerConstant('foo')


def test_invalid_float_constant():
    with pytest.raises(ValueError):
        misp_lib_stix2.FloatConstant('foo')


@pytest.mark.parametrize(
    "data, result", [
        (True, True),
        (False, False),
        ('True', True),
        ('False', False),
        ('true', True),
        ('false', False),
        ('t', True),
        ('f', False),
        ('T', True),
        ('F', False),
        (1, True),
        (0, False),
    ],
)
def test_boolean_constant(data, result):
    boolean = misp_lib_stix2.BooleanConstant(data)
    assert boolean.value == result


def test_invalid_boolean_constant():
    with pytest.raises(ValueError):
        misp_lib_stix2.BooleanConstant('foo')


@pytest.mark.parametrize(
    "hashtype, data", [
        ('MD5', 'zzz'),
        ('ssdeep', 'zzz=='),
    ],
)
def test_invalid_hash_constant(hashtype, data):
    with pytest.raises(ValueError):
        misp_lib_stix2.HashConstant(data, hashtype)


def test_invalid_hex_constant():
    with pytest.raises(ValueError):
        misp_lib_stix2.HexConstant('mm')


def test_invalid_binary_constant():
    with pytest.raises(ValueError):
        misp_lib_stix2.BinaryConstant('foo')


def test_escape_quotes_and_backslashes():
    exp = misp_lib_stix2.MatchesComparisonExpression(
        "file:name",
        "^Final Report.+\\.exe$",
    )
    assert str(exp) == "file:name MATCHES '^Final Report.+\\\\.exe$'"


def test_like():
    exp = misp_lib_stix2.LikeComparisonExpression(
        "directory:path",
        "C:\\Windows\\%\\foo",
    )
    assert str(exp) == "directory:path LIKE 'C:\\\\Windows\\\\%\\\\foo'"


def test_issuperset():
    exp = misp_lib_stix2.IsSupersetComparisonExpression(
        "ipv4-addr:value",
        "198.51.100.0/24",
    )
    assert str(exp) == "ipv4-addr:value ISSUPERSET '198.51.100.0/24'"


def test_repeat_qualifier():
    qual = misp_lib_stix2.RepeatQualifier(misp_lib_stix2.IntegerConstant(5))
    assert str(qual) == 'REPEATS 5 TIMES'


def test_invalid_repeat_qualifier():
    with pytest.raises(ValueError):
        misp_lib_stix2.RepeatQualifier('foo')


def test_invalid_within_qualifier():
    with pytest.raises(ValueError):
        misp_lib_stix2.WithinQualifier('foo')


def test_startstop_qualifier():
    qual = misp_lib_stix2.StartStopQualifier(
        misp_lib_stix2.StringConstant('2016-06-01T00:00:00Z'),
        misp_lib_stix2.StringConstant('2017-03-12T08:30:00Z'),
    )
    assert str(qual) == "START '2016-06-01T00:00:00Z' STOP '2017-03-12T08:30:00Z'"

    qual2 = misp_lib_stix2.StartStopQualifier(
        misp_lib_stix2.StringConstant("2016-06-01T00:00:00Z"),
        misp_lib_stix2.StringConstant('2016-07-01T00:00:00Z'),
    )
    assert str(qual2) == "START '2016-06-01T00:00:00Z' STOP '2016-07-01T00:00:00Z'"


def test_invalid_startstop_qualifier():
    with pytest.raises(ValueError):
        misp_lib_stix2.StartStopQualifier(
            'foo',
            misp_lib_stix2.StringConstant('2016-06-01T00:00:00Z'),
        )

    with pytest.raises(ValueError):
        misp_lib_stix2.StartStopQualifier(
            datetime.date(2016, 6, 1),
            'foo',
        )


@pytest.mark.parametrize(
    "input_, expected_class, expected_value", [
        (1, misp_lib_stix2.patterns.IntegerConstant, 1),
        (1.5, misp_lib_stix2.patterns.FloatConstant, 1.5),
        ("abc", misp_lib_stix2.patterns.StringConstant, "abc"),
        (True, misp_lib_stix2.patterns.BooleanConstant, True),
        (
            "2001-02-10T21:36:15Z", misp_lib_stix2.patterns.TimestampConstant,
            misp_lib_stix2.utils.STIXdatetime(2001, 2, 10, 21, 36, 15, tzinfo=pytz.utc),
        ),
        (
            datetime.datetime(2001, 2, 10, 21, 36, 15, tzinfo=pytz.utc),
            misp_lib_stix2.patterns.TimestampConstant,
            misp_lib_stix2.utils.STIXdatetime(2001, 2, 10, 21, 36, 15, tzinfo=pytz.utc),
        ),
    ],
)
def test_make_constant_simple(input_, expected_class, expected_value):
    const = misp_lib_stix2.patterns.make_constant(input_)

    assert isinstance(const, expected_class)
    assert const.value == expected_value


def test_make_constant_list():
    list_const = misp_lib_stix2.patterns.make_constant([1, 2, 3])

    assert isinstance(list_const, misp_lib_stix2.patterns.ListConstant)
    assert all(
        isinstance(elt, misp_lib_stix2.patterns.IntegerConstant)
        for elt in list_const.value
    )
    assert all(
        int_const.value == test_elt
        for int_const, test_elt in zip(list_const.value, [1, 2, 3])
    )


def test_make_constant_already_a_constant():
    str_const = misp_lib_stix2.StringConstant('Foo')
    result = misp_lib_stix2.patterns.make_constant(str_const)
    assert result is str_const


def test_parsing_comparison_expression():
    patt_obj = create_pattern_object("[file:hashes.'SHA-256' = 'aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f']", version="2.0")
    assert str(patt_obj) == "[file:hashes.'SHA-256' = 'aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f']"


def test_parsing_qualified_expression():
    patt_obj = create_pattern_object(
        "[network-traffic:dst_ref.type = 'domain-name' AND network-traffic:dst_ref.value = 'example.com'] REPEATS 5 TIMES WITHIN 1800 SECONDS",
        version="2.0",
    )
    assert str(
        patt_obj,
    ) == "[network-traffic:dst_ref.type = 'domain-name' AND network-traffic:dst_ref.value = 'example.com'] REPEATS 5 TIMES WITHIN 1800 SECONDS"


def test_parsing_start_stop_qualified_expression():
    patt_obj = create_pattern_object("[ipv4-addr:value = '1.2.3.4'] START '2016-06-01T00:00:00Z' STOP '2017-03-12T08:30:00Z'", version="2.0")

    assert str(
        patt_obj,
    ) == "[ipv4-addr:value = '1.2.3.4'] START '2016-06-01T00:00:00Z' STOP '2017-03-12T08:30:00Z'"


def test_parsing_mixed_boolean_expression_1():
    patt_obj = create_pattern_object("[a:b = 1 AND a:b = 2 OR a:b = 3]")
    assert str(patt_obj) == "[a:b = 1 AND a:b = 2 OR a:b = 3]"


def test_parsing_mixed_boolean_expression_2():
    patt_obj = create_pattern_object("[a:b = 1 OR a:b = 2 AND a:b = 3]")
    assert str(patt_obj) == "[a:b = 1 OR a:b = 2 AND a:b = 3]"


def test_parsing_integer_index():
    patt_obj = create_pattern_object("[a:b[1]=2]")
    assert str(patt_obj) == "[a:b[1] = 2]"


# This should never occur, because the first component will always be a property_name, and they should not be quoted.
def test_parsing_quoted_first_path_component():
    patt_obj = create_pattern_object("[a:'b'[1]=2]")
    assert str(patt_obj) == "[a:'b'[1] = 2]"


def test_parsing_quoted_second_path_component():
    patt_obj = create_pattern_object("[a:b.'b'[1]=2]")
    assert str(patt_obj) == "[a:b.'b'[1] = 2]"


def test_parsing_illegal_start_stop_qualified_expression():
    with pytest.raises(ValueError):
        create_pattern_object("[ipv4-addr:value = '1.2.3.4'] START '2016-06-01' STOP '2017-03-12T08:30:00Z'", version="2.0")


def test_list_constant():
    patt_obj = create_pattern_object("[network-traffic:src_ref.value IN ('10.0.0.0', '10.0.0.1', '10.0.0.2')]", version="2.0")
    assert str(patt_obj) == "[network-traffic:src_ref.value IN ('10.0.0.0', '10.0.0.1', '10.0.0.2')]"


def test_ast_class_override_comp_equals():
    patt_ast = create_pattern_object(
        "[a:b=1]", "Testing", "stix2.test.v20.pattern_ast_overrides",
        version="2.0",
    )

    assert isinstance(patt_ast, misp_lib_stix2.patterns.ObservationExpression)
    assert isinstance(patt_ast.operand, EqualityComparisonExpressionForTesting)
    assert str(patt_ast) == "[a:b = 1]"


def test_ast_class_override_string_constant():
    patt_ast = create_pattern_object(
        "[a:'b'[1].'c' < 'foo']", "Testing",
        "stix2.test.v20.pattern_ast_overrides",
        version="2.0",
    )

    assert isinstance(patt_ast, misp_lib_stix2.patterns.ObservationExpression)
    assert isinstance(
        patt_ast.operand, misp_lib_stix2.patterns.LessThanComparisonExpression,
    )
    assert isinstance(
        patt_ast.operand.lhs.property_path[0].property_name,
        str,
    )
    assert isinstance(
        patt_ast.operand.lhs.property_path[1].property_name,
        str,
    )
    assert isinstance(patt_ast.operand.rhs, StringConstantForTesting)

    assert str(patt_ast) == "[a:'b'[1].c < 'foo']"


def test_ast_class_override_startstop_qualifier():
    patt_ast = create_pattern_object(
        "[a:b=1] START '1993-01-20T01:33:52.592Z' STOP '2001-08-19T23:50:23.129Z'",
        "Testing", "stix2.test.v20.pattern_ast_overrides", version="2.0",
    )

    assert isinstance(patt_ast, misp_lib_stix2.patterns.QualifiedObservationExpression)
    assert isinstance(
        patt_ast.observation_expression, misp_lib_stix2.patterns.ObservationExpression,
    )
    assert isinstance(
        patt_ast.observation_expression.operand,
        EqualityComparisonExpressionForTesting,
    )
    assert isinstance(
        patt_ast.qualifier, StartStopQualifierForTesting,
    )
    assert str(patt_ast) == "[a:b = 1] START '1993-01-20T01:33:52.592Z' STOP '2001-08-19T23:50:23.129Z'"
