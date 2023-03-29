import requests
import json
from postman import *
#from typing import Set
# testing pynetbox
import pynetbox


# disable requests submodule warnings
requests.packages.urllib3.disable_warnings()


# intro
print("""



                       /\ \__/\ \            /\ \__     
            ___      __\ \ ,_\ \ \____    ___\ \ ,_\    
          /' _ `\  /'__`\ \ \/\ \ '__`\  / __`\ \ \/    
          /\ \/\ \/\  __/\ \ \_\ \ \L\ \/\ \L\ \ \ \_   
          \ \_\ \_\ \____\\\\ \__\\\\ \_,__/\ \____/\ \__\ 
           \/_/\/_/\/____/ \/__/ \/___/  \/___/  \/__/  


caution: use at your own risk, please read all prompts and pay attention to examples/suggestions

prep fortigate:
1. info here

setup netbox:
1. info here

""")

# fortigate prep script
input("Press Enter to generate script")

print("""
********************************************************************
********************************************************************
************************ SCRIPT STARTS HERE ************************
********************************************************************
********************************************************************

# set web portal to unique port
config system global
    set admin-port <someport>
    set admin-sport <someport>
end

# setup api user
config system api-user
    edit "api_admin"
        set accprofile "super_admin"
        set vdom "root"
        config trusthost
            edit 1
                set ipv4-trusthost <someip>
            next
            edit 2
                set ipv4-trusthost <someip>
            next
            edit 3
                set ipv4-trusthost <someip>
            next
            edit 4
                set ipv4-trusthost <someip>
            next
        end
    next
end

# generate api token/key for new api user
execute api-user generate-key api_admin

********************************************************************
********************************************************************
************************ SCRIPT ENDS HERE **************************
********************************************************************
********************************************************************

""")

input("Press Enter to continue...")

#static variables
print("setting static variables")
baseurl = "<fortigateiphere>"
https_port = "<fortigateporthere>"


#initialize netbox

nb = pynetbox.api(
    '<netboxurlhere>',
    token='<tokenhere>'
)

#manufacturer = input("Enter the manufacturer of the firewall (probably fortinet): ")
#slug = input("Enter the site slug from netbox: ")


print("setting initial variables....")
#user input
api_token = input("Enter the API token from the above script: ")
site_network_id = input("enter network id (3rd octet): ")
clientID = input("enter client id: ")

#parse json
print("parsing json input")
f = open("input.json",)
data = json.load(f)
wan1_gateway = data["wan1_gateway"]
wan2_gateway = data["wan2_gateway"]

j = open("automation.json",)
data = json.load(j)
actions = data["actions"]
triggers = data["triggers"]
stitches = data["stitches"]



#calculated variables
print("calculating variables")
ftg_model = getModelNumber(baseurl, https_port, api_token)
fgt_serial = getSerialNumber(baseurl, https_port, api_token)
hostname = clientID + "-" + ftg_model
sipHelperID = getSipHelperID(baseurl, https_port, api_token)
switchports = getInternalVirtualSwitch(baseurl, https_port, api_token)
admin_obj = getLoggedInAdmins(baseurl, https_port, api_token)
model = fgt_serial[:6]
serial_15 = fgt_serial[-10:]

if admin_obj:
    admin_id = admin_obj["id"]
    admin_method = admin_obj["method"]


#running functions
setConfigCheckpoint(baseurl, https_port, api_token, "fresh build")
setPasswordPolicy(baseurl, https_port, api_token)
setAdminUser(baseurl, https_port, api_token)

# checking if user exists before trying to execute
if admin_obj:
    kickLoggedInAdmins(baseurl, https_port, api_token, admin_id, admin_method)

#deleteAdminUser(baseurl, https_port, api_token)
setSysSettings(baseurl, https_port, api_token)
setSysGlobal(baseurl, https_port, api_token, hostname)
setAutoupdatePush(baseurl, https_port, api_token)
disableSipAlg(baseurl, https_port, api_token)
deleteSipHelper(baseurl, https_port, api_token, sipHelperID)
editInternalVirtualSwitch(baseurl, https_port, api_token)
createVirtualSwitch(baseurl, https_port, api_token)
setNetworkInterfacesVlan1(baseurl, https_port, api_token, site_network_id)

#setting vlan interfaces from netbox
#getting all devices with given serial number
devices = nb.dcim.devices.filter(serial=fgt_serial)
for device in devices:
    #print(dict(device))
    device_id = device.id
    #print(fgt_device_id)

    interfaces = nb.dcim.interfaces.filter(device_id=device_id)
    for interface in interfaces:
        #checking if any interfaces have vlans tagged on them
        if interface.tagged_vlans:
            #if so and they are a subinterface then continue
            if interface.parent:
                interface_parent = interface.parent['display']
                interface_id = interface.id
                interface_name = interface.name


                for tagged_vlan in interface.tagged_vlans:
                    vlan_id = tagged_vlan.id

                    vlans = nb.ipam.vlans.filter(id=vlan_id)
                    for vlan in vlans:
                        vlan_alias = vlan.role["name"]
                        vlan_vid = vlan.vid

                    prefixes = nb.ipam.prefixes.filter(vlan_id=vlan_id)
                    for prefix in prefixes:
                        prefix_prefix = prefix.prefix
                        prefix_id = prefix.id

                        if prefix.vrf:
                            vrf_id = prefix.vrf.id


    
                    interface_ips = nb.ipam.ip_addresses.filter(device_id=device_id, interface_id=interface_id, vrf_id=vrf_id)
                    for interface_ip in interface_ips:
                        ip = interface_ip.address
                        ipNetwork = IPNetwork(interface_ip.address)

                        setNetworkInterfaceVlan(baseurl, https_port, api_token, interface_name, vlan_vid, vlan_alias, ip)
                        setFirewallAddressObjects(baseurl, https_port, api_token, vlan_alias, prefix_prefix)
                        

                    #counter = 0
                    start_ip = ""
                    end_ip = ""    
                    dhcp_ips = nb.ipam.ip_addresses.filter(parent=prefix_prefix, status="dhcp", vrf_id=vrf_id)
                    # look into doing 
                    # length = len(dhcp_ips) - 1 
                    # dhcp_ips[length]
                    for x, dhcp_ip in enumerate(dhcp_ips):
                        ipNetworkDhcp = IPNetwork(dhcp_ip.address)
                        if x == 0 :
                            #print(ip.address)
                            start_ip = ipNetworkDhcp.ip
                            #print(start_ip)
                        end_ip = ipNetworkDhcp.ip

                    if start_ip and end_ip :
                        setDhcpServers(baseurl, https_port, api_token, clientID, ipNetwork, interface_name, start_ip, end_ip)




        if interface.name == "wan1":
            interface_id = interface.id
            ips = nb.ipam.ip_addresses.filter(device_id=device_id, interface_id=interface_id)
            for ip in ips:
                wan1_ip = ip.address
                setWan1Interface(baseurl, https_port, api_token, wan1_ip)

        if interface.name == "wan2":
            interface_id = interface.id
            ips = nb.ipam.ip_addresses.filter(device_id=device_id, interface_id=interface_id)
            for ip in ips:
                wan2_ip = ip.address
                setWan2Interface(baseurl, https_port, api_token, wan2_ip)


deleteDefaultHealthChecks(baseurl, https_port, api_token)
setSDwanSettings(baseurl, https_port, api_token, wan1_gateway, wan2_gateway)
setSDwanRoute(baseurl, https_port, api_token)
setBlackholeRoutes(baseurl, https_port, api_token)
setDhcpServersLegacy(baseurl, https_port, api_token, site_network_id, clientID)
setFirewallAddressObjectsLegacy(baseurl, https_port, api_token, site_network_id)
setFirewallAddressGroups(baseurl, https_port, api_token)
setFirewallServiceObjects(baseurl, https_port, api_token)
setFirewallServiceGroups(baseurl, https_port, api_token)
createFilterProfiles(baseurl, https_port, api_token)
setVips(baseurl, https_port, api_token, site_network_id)
setVipGroup(baseurl, https_port, api_token)
deleteFirewallPolicy(baseurl, https_port, api_token)
setFirewallPolicies(baseurl, https_port, api_token)
setFirewallLocalInPolicies(baseurl, https_port, api_token)
apiUserResponse = createApiUser(baseurl, https_port, api_token)
username = apiUserResponse.json()["mkey"]

apikey = generateApiUserKey(baseurl, https_port, api_token, username)
print(apikey.json()["results"]["access_token"])

setCustomLogField(baseurl, https_port, api_token, "serial", serial_15)
setCustomLogField(baseurl, https_port, api_token, "model", model)

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

setLogSettings(baseurl, https_port, api_token, payload)


for action in actions:
    setAutomationAction(baseurl, https_port, api_token, action)

for trigger in triggers: 
    setAutomationTrigger(baseurl, https_port, api_token, trigger)

for stitch in stitches: 
    setAutomationStitch(baseurl, https_port, api_token, stitch)


setConfigCheckpoint(baseurl, https_port, api_token, "after initial config")
#deleteApiUser(baseurl, https_port, api_token)
