import requests
import json
from variables import *

#Disable warnings
requests.packages.urllib3.disable_warnings()

def main():
    """
    Main body for DevNet Create 19. In this, we will
        1. Create a session to the NAE instance
        2. Access all fabrics
        3. Fetch fabric
            a. All fabrics
            b. Running fabric
        4. Fetch epochs
            a. Last 20 epochs 
            b. Latest epoch
        5. Fetch event summary for the latest epoch
        6. Fetch events by
            a. category
            b. severity
        7. Find all the epochs in which an event exists


    """
    print_banner("Let's learn NAE APIs!")

    print_banner("Create a session to the NAE instance")
    # Logon to the NAE instance and print credentials
    if nae_login(NAE_IP, NAE_USER, NAE_PASS):
        header = NAE_HEADER
    else:
        print ("Login failed to: " + NAE_IP + " with username: " + NAE_USER + " and password: " + NAE_PASS)

    print_banner("Get all fabric ids")
    # Get all fabric Ids
    fabric_ids = get_fabric_ids()
    print (json.dumps(fabric_ids, indent=4, sort_keys=True))

    print_banner("Fetch running fabric")
    # Get running fabric
    for fabric in fabric_ids:
        if fabric['status'] == 'RUNNING':
            RUNNING_FABRIC_ID = fabric['id']
            print (RUNNING_FABRIC_ID)
        else:
            RUNNING_FABRIC_ID = None

    # If no running fabric is found, we will use the first fabric
    if not RUNNING_FABRIC_ID:
        print ("No running fabric found. Using the first fabric from the list")
        RUNNING_FABRIC_ID = fabric_ids[0]['id']


def print_banner(message):
    """
    Print a banner
    """
    print ("\n\n*************************************")
    print (message)
    print ("*************************************")

def nae_login(nae_ip, nae_user, nae_pass):
    """
    Logon to NAE
        :parameter:
            nae_ip (required): IP address of Cisco NAE instance to connect to
            nae_user (required): User name to log on to device specified by nae_ip
            nae_pass (required): Password for nae_user
    """
    data = dict() 
    data['username'] = nae_user
    data['password'] = nae_pass 
    data = json.dumps(data)

    header = dict()
    header["Content-Type"] = "application/json"
    header["Accept"] = "application/json"

    '''
        Executes whoami request first to get the one time password and retireves session id, which will be used to login and 
        get the actual token and session id that will be used in all subsequent REST Call.
        URL - "https://nae_ip/api/v1/whoami"
    '''
    wmi_req = requests.get(url=WMI_URL, headers=header, verify=False)
    
    if wmi_req.status_code is 200 or wmi_req.status_code is 201:
        otp = wmi_req.headers['X-NAE-LOGIN-OTP']
        sid = wmi_req.headers['Set-Cookie']
        sid = str(sid).split(';')[0]

        '''
            Taking one time password and session id as inputs, this generates a token after authenticating 
            (Username and Password sent in the body).
            URL - URL - "https://nae_ip/api/v1/login"
        '''
        header['X-NAE-LOGIN-OTP'] = otp
        header['Cookie'] = sid
        req = requests.post(url=LOGIN_URL, data=data, headers=header, verify=False)

        if req.status_code is 200 or req.status_code is 201:
            nae_token = req.headers['X-NAE-CSRF-TOKEN']
            cookie = req.headers['Set-Cookie']
            nae_session = str(cookie).split(';')[0]

            NAE_HEADER["Content-Type"] = "application/json" 
            NAE_HEADER["Accept"] = "application/json" 
            NAE_HEADER['X-NAE-CSRF-TOKEN'] = nae_token 
            NAE_HEADER['Cookie'] = nae_session
            return True
        else:
            return False

def get_fabric_ids():
    """
    Get a list of all Fabrics, along with APICs
        :return:
            fabric_ids: All fabrics, along with APIC IPs
            Type: List
    """
    fabric_ids = dict()
    fabric_ids = []

    '''
        Build URL and send the request. URL - "https://{nae_ip}/api/v1/assured-networks/aci-fabric"
    '''
    req = requests.get(url=FABRIC_URL, headers=NAE_HEADER, verify=False)
    if req.status_code is 200:
        resp = json.dumps(req.json())
        res = json.loads(resp)
        data_no = len(res['value']['data'])
        '''
            Write all fabric UUIDs to an array and return the array
        '''
        for f in range(0, data_no):
            fab = dict()
            fab['id'] = res['value']['data'][f]['uuid']
            fab['status'] = res['value']['data'][f]['status']
            if fab['status'] == 'RUNNING':
                fab['apic_hosts'] = res['value']['data'][f]['apic_hostnames']
            fabric_ids.append(fab)
    return fabric_ids

if __name__ == '__main__':
    main()
