import datetime

import pytz

import misp_lib_stix2

FAKE_TIME = datetime.datetime(2017, 1, 1, 12, 34, 56, tzinfo=pytz.utc)

ATTACK_PATTERN_ID = "attack-pattern--168b3330-fc69-11e8-b98e-0800279d6dc6"
BUNDLE_ID = "bundle--2acecf31-5262-3981-8eff-db8a1de5945b"
CAMPAIGN_ID = "campaign--f22d70fa-871d-5155-9812-89b3a48f6e50"
COURSE_OF_ACTION_ID = "course-of-action--f9ae0d21-f4c9-360e-8743-b064b2ad2a2e"
IDENTITY_ID = "identity--035a5348-2485-3bca-99ce-62da0f14c37a"
INDICATOR_ID = "indicator--412aba5b-75b4-5827-99f1-c62d91504e97"
INTRUSION_SET_ID = "intrusion-set--2d1db502-fc6c-11e8-8b3f-00216af611cf"
MALWARE_ID = "malware--64ee70a4-8cc1-5d25-8bf2-dea6c79a09c8"
MARKING_DEFINITION_ID = "marking-definition--f8427579-bd0f-3550-8eef-c3f2cb33cd0f"
OBSERVED_DATA_ID = "observed-data--9a74c83e-2c09-3513-874b-91d679be82b8"
RELATIONSHIP_ID = "relationship--ee36ba22-c954-5d25-89c8-5a435eaebeb3"
REPORT_ID = "report--dbfe2a52-fc6c-11e8-8b3f-00216af611cf"
SIGHTING_ID = "sighting--9ae1145d-b1b2-57b6-83f1-36a173a24112"
THREAT_ACTOR_ID = "threat-actor--e5313ad6-6b11-3c07-8ace-7dc52824e063"
TOOL_ID = "tool--bf0895d6-7626-361f-89dd-d404aa340bc2"
VULNERABILITY_ID = "vulnerability--20296e55-98b9-5988-851a-51eddd5022c8"

OBJECT_REFS = [
    ATTACK_PATTERN_ID, CAMPAIGN_ID, COURSE_OF_ACTION_ID, INDICATOR_ID, INTRUSION_SET_ID,
    MALWARE_ID, MARKING_DEFINITION_ID, OBSERVED_DATA_ID, RELATIONSHIP_ID, SIGHTING_ID,
    THREAT_ACTOR_ID, TOOL_ID, VULNERABILITY_ID,
]

ATTACK_PATTERN_KWARGS = dict(
    type='attack-pattern',
    id=ATTACK_PATTERN_ID,
    name="Phishing",
    created_by_ref=IDENTITY_ID,
)

BUNDLE_KWARGS = dict(
    type='bundle',
    id=BUNDLE_ID,
)

CAMPAIGN_KWARGS = dict(
    type='campaign',
    id=CAMPAIGN_ID,
    created_by_ref=IDENTITY_ID,
    created="2016-04-06T20:03:00.000Z",
    modified="2016-04-06T20:03:00.000Z",
    name="Green Group Attacks Against Finance",
    description="Campaign by Green Group against a series of targets in the financial services sector.",
)

COURSE_OF_ACTION_KWARGS = dict(
    type='course-of-action',
    id=COURSE_OF_ACTION_ID,
    name="Block",
    created_by_ref=IDENTITY_ID,
)

IDENTITY_KWARGS = dict(
    type='identity',
    id=IDENTITY_ID,
    name="John Smith",
    identity_class="individual",
)

INDICATOR_KWARGS = dict(
    type='indicator',
    id=INDICATOR_ID,
    labels=['malicious-activity'],
    pattern="[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
    pattern_type="stix",
    created_by_ref=IDENTITY_ID,
    indicator_types=["malicious-activity"],
    valid_from="2016-04-06T20:03:00.000Z",
)

INTRUSION_SET_KWARGS = dict(
    type='intrusion-set',
    id=INTRUSION_SET_ID,
    name="Bobcat Breakin",
    created_by_ref=IDENTITY_ID,
)

MALWARE_KWARGS = dict(
    type='malware',
    id=MALWARE_ID,
    created="2016-04-06T20:03:00.000Z",
    modified="2016-04-06T20:03:00.000Z",
    labels=['ransomware'],
    name="Cryptolocker",
    description="A ransomware related to ...",
    created_by_ref=IDENTITY_ID,
    malware_types=["malicious-activity"],
    is_family=False,
)

MARKING_DEFINITION_KWARGS = dict(
    type='marking-definition',
    id=MARKING_DEFINITION_ID,
    definition_type='statement',
    definition={'statement': "Copyright 2016, Example Corp"},
    created_by_ref=IDENTITY_ID,
)

OBSERVED_DATA_KWARGS = dict(
    type='observed-data',
    id=OBSERVED_DATA_ID,
    first_observed=FAKE_TIME,
    last_observed=FAKE_TIME,
    number_observed=1,
    objects={
        "0": {
            "type": "windows-registry-key",
            "key": "HKEY_LOCAL_MACHINE\\System\\Foo\\Bar",
        },
    },
    created_by_ref=IDENTITY_ID,
)

REPORT_KWARGS = dict(
    type='report',
    id=REPORT_ID,
    labels=["campaign"],
    name="Bad Cybercrime",
    published=FAKE_TIME,
    object_refs=OBJECT_REFS,
    created_by_ref=IDENTITY_ID,
    report_types=["malicious-activity"],
)

RELATIONSHIP_KWARGS = dict(
    type='relationship',
    id=RELATIONSHIP_ID,
    relationship_type="indicates",
    source_ref=INDICATOR_ID,
    target_ref=MALWARE_ID,
    created_by_ref=IDENTITY_ID,
)

SIGHTING_KWARGS = dict(
    type='sighting',
    id=SIGHTING_ID,
    sighting_of_ref=INDICATOR_ID,
    created_by_ref=IDENTITY_ID,
    observed_data_refs=[OBSERVED_DATA_ID],
    where_sighted_refs=[IDENTITY_ID],
)

THREAT_ACTOR_KWARGS = dict(
    type='threat-actor',
    id=THREAT_ACTOR_ID,
    labels=["crime-syndicate"],
    name="Evil Org",
    created_by_ref=IDENTITY_ID,
    threat_actor_types=["malicious-activity"],
)

TOOL_KWARGS = dict(
    type='tool',
    id=TOOL_ID,
    labels=["remote-access"],
    name="VNC",
    created_by_ref=IDENTITY_ID,
    interoperability=True,
    tool_types=["malicious-activity"],
)

VULNERABILITY_KWARGS = dict(
    type='vulnerability',
    id=VULNERABILITY_ID,
    name="Heartbleed",
    created_by_ref=IDENTITY_ID,
)


if __name__ == '__main__':
    attack_pattern = misp_lib_stix2.v21.AttackPattern(**ATTACK_PATTERN_KWARGS, interoperability=True)
    campaign = misp_lib_stix2.v21.Campaign(**CAMPAIGN_KWARGS, interoperability=True)
    course_of_action = misp_lib_stix2.v21.CourseOfAction(**COURSE_OF_ACTION_KWARGS, interoperability=True)
    identity = misp_lib_stix2.v21.Identity(**IDENTITY_KWARGS, interoperability=True)
    indicator = misp_lib_stix2.v21.Indicator(**INDICATOR_KWARGS, interoperability=True)
    intrusion_set = misp_lib_stix2.v21.IntrusionSet(**INTRUSION_SET_KWARGS, interoperability=True)
    malware = misp_lib_stix2.v21.Malware(**MALWARE_KWARGS, interoperability=True)
    marking_definition = misp_lib_stix2.v21.MarkingDefinition(**MARKING_DEFINITION_KWARGS, interoperability=True)
    observed_data = misp_lib_stix2.v21.ObservedData(**OBSERVED_DATA_KWARGS, interoperability=True)
    relationship = misp_lib_stix2.v21.Relationship(**RELATIONSHIP_KWARGS, interoperability=True)
    sighting = misp_lib_stix2.v21.Sighting(**SIGHTING_KWARGS, interoperability=True)
    threat_actor = misp_lib_stix2.v21.ThreatActor(**THREAT_ACTOR_KWARGS, interoperability=True)
    tool = misp_lib_stix2.v21.Tool(**TOOL_KWARGS)
    vulnerability = misp_lib_stix2.v21.Vulnerability(**VULNERABILITY_KWARGS, interoperability=True)
    report = misp_lib_stix2.v21.Report(**REPORT_KWARGS, interoperability=True)
    bundle = misp_lib_stix2.v21.Bundle(
        **BUNDLE_KWARGS, interoperability=True,
        objects=[
            attack_pattern, campaign, course_of_action, identity, indicator,
            intrusion_set, malware, marking_definition, observed_data, tool,
            relationship, sighting, threat_actor, vulnerability, report,
        ]
    )
    misp_lib_stix2.parse(dict(bundle), interoperability=True)
    print("All interoperability tests passed !")
