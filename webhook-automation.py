
import pynetbox
from postman import *
from netaddr import *

requests.packages.urllib3.disable_warnings()

nb = pynetbox.api(
    '<netboxurlhere>',
    token='<tokenhere>'
)


#print("parsing json input")
f = open("automation.json",)
data = json.load(f)
actions = data["actions"]
triggers = data["triggers"]
stitches = data["stitches"]


devices = nb.dcim.devices.filter(manufacturer="fortinet")
for device in devices:
    #print(dict(device))
    fgt_device_id = device.id
    fgt_serial = device.serial

    print(device.name)
    print(fgt_serial)
    api_token = input("token for api user: ")

    if api_token:

        if device.primary_ip:
            device_primary_ip = IPNetwork(device.primary_ip.address)
        else: 
            print(f"no primary IP for {device.name}")
            device_primary_ip = IPNetwork(input("enter the primary wan IP in cidr notation (e.g. 192.168.1.99/24): "))

        baseurl = str(device_primary_ip.ip)
        https_port = "<porthere>"
    
        model = fgt_serial[:6]
        serial_15 = fgt_serial[-10:]
    
        print("getting custom log fields...")
        response = getCustomLogField(baseurl, https_port, api_token)
        print(response)
        response_json = response.json()
        logfields = []
        for result in response_json["results"]:
            logfields.append(result["name"])
    
        #print(logfields)
        print("setting checkpoint...")
        setConfigCheckpoint(baseurl, https_port, api_token, "before elastic logging")
    
        if "serial" in logfields :
            pass
        else: 
            try:
                print("setting custom field serial...")
                setCustomLogField(baseurl, https_port, api_token, "serial", serial_15)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            
        if "model" in logfields:
            pass
        else:
            try:
                print("setting custom field model...")
                setCustomLogField(baseurl, https_port, api_token, "model", model)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            
            
        payload = json.dumps({
            "custom-log-fields": [
                {
                    "field-id": "model"
                },
                {   
                    "field-id": "serial"
                }  
            ]
        })
    
        print("setting log settings...")
        r = setLogSettings(baseurl, https_port, api_token, payload)
        print(r)
    
        print("setting actions...")
        for action in actions:
            try:
                r = setAutomationAction(baseurl, https_port, api_token, action)
                print(r)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            
        print("setting triggers...")
        for trigger in triggers: 
            try:
                r = setAutomationTrigger(baseurl, https_port, api_token, trigger)
                print(r)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            
        print("setting stitches...")
        for stitch in stitches: 
            try:
                r = setAutomationStitch(baseurl, https_port, api_token, stitch)
                print(r)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            
        print("setting checkpoint...")
        setConfigCheckpoint(baseurl, https_port, api_token, "after elastic build")