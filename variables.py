#!/usr/bin/env python
# Task 1
APIC_IP = "candid2-apic3.cisco.com"

NAE_IP = "10.193.30.244"
NAE_USER = "devwks1020.user9"
NAE_PASS = "DEVWKS1020user9"
NAE_HEADER = dict()

APIC_BASE_URL = "https://" + APIC_IP + "/api/"
NAE_BASE_URL = "https://" + NAE_IP + "/api/v1/"

WMI_URL = NAE_BASE_URL + "whoami"
LOGIN_URL = NAE_BASE_URL + "login"

# Task 2
FABRIC_URL = NAE_BASE_URL + "assured-networks/aci-fabric"

# Task 3
RUNNING_FABRIC_ID = None

# Task 5
SEVERITY = dict()
CATEGORY = dict()
MNEMONIC = dict()
