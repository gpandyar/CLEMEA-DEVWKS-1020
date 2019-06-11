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

def print_banner(message):
    """
    Print a banner
    """
    print ("\n\n*************************************")
    print (message)
    print ("*************************************")

if __name__ == '__main__':
    main()
