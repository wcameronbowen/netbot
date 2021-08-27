
import pynetbox
from postman import *
from netaddr import *

nb = pynetbox.api(
    '<netboxurlhere>',
    token='<tokenhere>'
)

baseurl = "<fortigateiphere>"
api_token = "<apitokenhere>"
https_port = "<httpsporthere>"


def getCustomLogFieldTest(baseurl, https_port, api_token):
    """
    gets custom log fields

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    :param str log_name: name of the custom field
    :param str log_value: value that will be put into that custom field 
       note, cannot be more than 15 characters
    """
    
    try:
      url = f"https://{baseurl}:{https_port}/api/v2/cmdb/log/custom-field?access_token={api_token}" 

      payload = ""
      headers = {
        'Content-Type': 'application/json',
      }
      response = requests.request("GET", url, headers=headers, data=payload, verify=False)
      #print(response.text)

      return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise




def getIpInfo(ip):
    """
    gets custom log fields

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    :param str log_name: name of the custom field
    :param str log_value: value that will be put into that custom field 
       note, cannot be more than 15 characters
    """
    
    try:
      url = f"http://ipwhois.app/json/{ip}" 

      payload = ""
      headers = {
        'Content-Type': 'application/json',
      }
      response = requests.request("GET", url, headers=headers, data=payload, verify=False)

      return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


#r = getCustomLogFieldTest(baseurl, https_port, api_token)
r = getIpInfo("8.8.8.8")

#print(r.status_code)
#print(r.text)
#print(r.json())
#print(r.history)
#print(r.content)

for attr in dir(r):
    print("obj.%s = %r" % (attr, getattr(r, attr)))

#devices = nb.dcim.devices.filter(serial="<serialhere")
#for device in devices:
#    for attr in dir(device):
#        print("obj.%s = %r" % (attr, getattr(device, attr)))
#
#
#    interfaces = nb.dcim.interfaces.filter(device_id=fgt_device_id)
#    for interface in interfaces:
#        #print(dict(interface))
#        #checking if any interfaces have vlans tagged on them
#        if interface.tagged_vlans:
#            #if so and they are a subinterface then continue
#            if interface.parent:
#                #checking if interface has a parent interface and continuing if so
#                interface_parent = interface.parent['display']
#                interface_id = interface.id
#                interface_name = interface.name
#
#
#                for tagged in interface.tagged_vlans:
#                    #vlanid = tagged.vid
#                    netboxvlanid = tagged.id
#
#                    taggedvlan = nb.ipam.vlans.filter(id=netboxvlanid)
#                    for info in taggedvlan:
#                        print(dict(info))
#                        alias = info.role["name"]
#                        vlan_id = info.id
#
#                    prefixes = nb.ipam.prefixes.filter(vlan_id=netboxvlanid)
#                    for prefix in prefixes:
#                        #print(dict(prefix))
#                        prefix_prefix = prefix.prefix
#                        prefix_id = prefix.id
#                        #print(prefix_prefix)
#                        #print(dict(prefix))
#                        if prefix.vrf:
#                            print(prefix.vrf)
#                            vrf_id = prefix.vrf.id
#                            print(vrf_id)
#
#
#



















########################################################################
#print("parsing json input")
#f = open("automation.json",)
#data = json.load(f)
#actions = data["actions"]
#triggers = data["triggers"]
#stitches = data["stitches"]
#
#
#devices = nb.dcim.devices.filter(manufacturer="fortinet", serial="<serialhere>")
#for device in devices:
#    #print(dict(device))
#    fgt_device_id = device.id
#    fgt_serial = device.serial
#    #print(fgt_device_id)
#
#    print(fgt_serial)
#    print(device.name)
#
#
#    baseurl = input("external IP of fortigate: ")
#    api_token = input("token for api user: ")
#    https_port = input("https port: ")
#    #baseurl = "<fortigateiphere>"
#    #api_token = "<tokenhere>"
#    #https_port = "<porthere>"
#
#
#    model = fgt_serial[:6]
#    serial_15 = fgt_serial[-10:]
#
#    print(model)
#    print(serial_15)
#    #setCustomLogField(baseurl, https_port, api_token, "model", model)
#    #setCustomLogField(baseurl, https_port, api_token, "serial", serial_15)
#
#setCustomLogField(baseurl, https_port, api_token, fgt_serial)
#
#for action in actions:
#    setAutomationAction(baseurl, https_port, api_token, action)
#
#for trigger in triggers: 
#    setAutomationTrigger(baseurl, https_port, api_token, trigger)
#
#for stitch in stitches: 
#    setAutomationStitch(baseurl, https_port, api_token, stitch)


