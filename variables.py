APIC_IP = "aci-k8tes-sandbox"

NAE_IP = "nae-sandbox.cisco.com"
NAE_USER = "developer"
NAE_PASS = "C!sco1234567890"
NAE_HEADER = {}

APIC_BASE_URL = "https://" + APIC_IP + "/api/"
NAE_BASE_URL = "https://" + NAE_IP + "/api/v1/"

WMI_URL = NAE_BASE_URL + "whoami"
LOGIN_URL = NAE_BASE_URL + "login"

RUNNING_FABRIC = None

FABRIC_URL = NAE_BASE_URL + "assured-networks/aci-fabric"

SEVERITY = dict()
CATEGORY = dict()
MNEMONIC = dict()


