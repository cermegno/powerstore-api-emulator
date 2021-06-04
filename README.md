# powerstore-api-emulator
Basic emulator of DellEMC PowerStore REST API provisioning functions

## Description
It allows you to get familiar with the basics programming with the DellEMC PowerStore REST API. It implements the following API calls that cover some basic information gathering and the fundamentals of block provisioning:

- GET /cluster
- GET /event
- GET /host
- GET /host/<host_id>
- POST /host
- DELETE /host/<host_id>
- GET /volume
- GET /volume/<vol_id>
- POST /volume
- PATCH /volume/<vol_id>
- POST /volume/<vol_id>/attach
- DELETE /volume/<vol_id>
- GET /host_volume_mapping

Information for the cluster and the event calls is static but the information about hosts, volumes and mappings can be edited through the API calls. It lives in memory and it will last until you stop the emulator

In order to help you interact with the emulator the following resources have been provided:
 - Sample collection in the Postman folder
 - Sample playbooks in the Ansible folder. The playbooks successfully behave idempotently like the real array. As playbooks run you can see all the different API calls the Ansible modules perform in order to ensure idempotency

## Requirements
It has been developed with Python 3.9.2. It has also been tested with Python 3.6.8
Python package requirements are mostly Flask and PyOpenSSL. You can install the specific versions with the attached requirements.txt

## Known limitations
- Only a single field will be used for matching
- Only "eq." rules for matching
- Not checking if the new volume size is larger than current size during a PATCH
- Not checking whether a host has volume mappings during a DELETE /volume
- Not enforcing mandatory parameters when creating resources
- ... and a few more

