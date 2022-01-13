import requests
from twilio.rest import Client
import time

prefered_sites = ['Santa Clara County Fairgrounds - Parking Lot A']

def SendSMS(details):
    account_sid = "******"
    auth_token = "******"
    msg = ""
    print(details)
    for center, slots in details.items():
        msg += "\n{0} slots in {1}".format(slots, center)
    client = Client(account_sid, auth_token)
    client.api.account.messages.create(
        to="+11234567890", 
        from_="+15554443333",
        body=msg)

def getAppointments():
    rsp = requests.get("https://scl.fulgentgenetics.com/api/sites/slot-sites")
    if rsp.status_code != 200:
        return
    info = dict()
    status = rsp.json()
    for s in status['sites']:
        if s['name'] in prefered_sites:
            info[s['name']] = s['slots_left']
    return info

while True:
    info = getAppointments()
    SendSMS(info)
    if len(info) > 0:
        time.sleep(3600)
    else:
        time.sleep(120)
