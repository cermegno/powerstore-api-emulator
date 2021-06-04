host_template = {
    "id": "19894d22-87e1-4fef-9a040000000000001",
    "name": "a01",
    "os_type": "Linux",
    "os_type_l10n": "Linux",
    "description": "k8s node 2",
    "host_group_id": None,
    "host_initiators": [
        {
            "port_name": "21:00:00:24:ff:12:e9:aa",
            "port_type": "FC"
        },
        {
            "port_name": "21:00:00:24:ff:12:e9:bb",
            "port_type": "FC"
        }
    ]
}

hosts = [host_template]

volume_template = {
    "id": "557fb1e2-fe5a-450a-8cc9-837400000001",
    "name": "Powerstore-Demo-0003",
    "description": "",
    "type": "Primary",
    "appliance_id": "A1",
    "state": "Ready",
    "size": 107374182400,
    "wwn": "naa.68ccf09800214791c8e202dd7a95ada8",
    "performance_policy_id": None,
    "protection_policy_id": None,
    "host": [],
    "host_group": [],
    "volume_groups": []
}

volumes = [volume_template]

host_mapping_template = {
    "id": "2d1bcdc7-1288-4beb-bbce-8707c9469f68",
    "host_id": "19894d22-87e1-4fef-9a040000000000001",
    "volume_id": "557fb1e2-fe5a-450a-8cc9-837400000001",
    "host_group_id": None,
    "logical_unit_number": 1
}

mappings = [host_mapping_template]

cluster = [
    {
        "id": "0",
        "name": "PowerStore-1000X",
        "master_appliance_id": "A1",
        "state": "Configured"
    }
]


events = [
    {
        "id": "b6b9884a-d7a5-4b81-11c1-267937436f16",
        "severity": "Info",
        "resource_type": "system",
        "generated_timestamp": "2020-10-20T13:49:56.869+00:00",
        "description_l10n": "Clear alerts for object csi-0e87a32d9c of type volume."
    },
    {
        "id": "c5133266-8cb0-05ea-05d1-1a80459175f9",
        "severity": "Info",
        "resource_type": "volume",
        "generated_timestamp": "2020-10-20T13:30:41.104+00:00",
        "description_l10n": "A replication session associated with resource demo-vol00001 has been deleted."
    },
    {
        "id": "1b4bbbca-801b-c52a-3180-820ce2d41559",
        "severity": "Minor",
        "resource_type": "appliance",
        "generated_timestamp": "2020-10-20T21:48:02.241+00:00",
        "description_l10n": "Unable to get information about the vCenter API version."
    },
    {
        "id": "185dcd4e-7d6c-a737-7897-6f517460a1a8",
        "severity": "Major",
        "resource_type": "appliance",
        "generated_timestamp": "2020-10-20T21:48:02.241+00:00",
        "description_l10n": "Failed to connect to the vCenter 172.24.185.100."
    }
]
