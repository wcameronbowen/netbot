import requests
import json
from postman import *
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

prep:
1. <infohere>

""")


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
input("You ran that script right?? ")

#static variables
print("setting static variables")
baseurl = "<fortigateiphere>"
https_port = "<fortigateporthere>"

#initialize netbox
nb = pynetbox.api(
    '<netboxurlhere>',
    token='<tokenhere>'
)


print("setting initial variables....")
#user input
api_token = input("Enter the API token from the above script: ")
#site_network_id = input("enter network id (3rd octet): ")
#clientID = input("enter client id: ")
tunnel_name = input("enter tunnel name: ")
peer_ip = input("enter peer ip: ")
psk = input("enter psk: ")
date = input("enter today's date: ")
comment = input("enter a description: ")
local_addresses = input("enter local ip addresses: ").split(", ")
remote_addresses = input("enter remote ip addresses: ").split(", ")
fgt_serial = getSerialNumber(baseurl, https_port, api_token)


#parse json
print("parsing json input")
f = open("tunnel_input.json",)
data = json.load(f)

data["phase1"]["name"] = tunnel_name
data["phase1"]["remote-gw"] = peer_ip
data["phase1"]["psksecret"] = psk 
data["phase1"]["comments"] = date + comment
phase1_config = data["phase1"]
phase2_config = data["phase2"]


#empty variables
print("initializing empty variables")


setConfigCheckpoint(baseurl, https_port, api_token, "fresh build")

#creating addres objects
local_members = setVpnLocalAddressObjects(baseurl, https_port, api_token, tunnel_name, local_addresses) 
remote_members = setVpnRemoteAddressObjects(baseurl, https_port, api_token, tunnel_name, remote_addresses) 

# creating address groups
local_group = setVpnLocalAddressGroups(baseurl, https_port, api_token, tunnel_name, local_members)
remote_group = setVpnRemoteAddressGroups(baseurl, https_port, api_token, tunnel_name, remote_members)

# creating phase1
createPhase1Interface(baseurl, https_port, api_token, phase1_config)

# creating phase2
for local_member in local_members:
    for y, remote_member in enumerate(remote_members):
        
        data["phase2"]["name"] = f"{tunnel_name}_{y}"
        data["phase2"]["phase1name"] = tunnel_name
        data["phase2"]["src-name"] = local_member["name"]
        data["phase2"]["dst-name"] = remote_member["name"]
        
        #print(data["phase2"])
        
        createPhase2Interface(baseurl, https_port, api_token, phase2_config)

# creating static routes
static_route_id = 100

for remote_member in remote_members:
    phase2_dst_addr = remote_member["name"]

    if phase2_dst_addr != "0.0.0.0" :
        createVpnStaticRoute(baseurl, https_port, api_token, tunnel_name, static_route_id, phase2_dst_addr)
        static_route_id =  static_route_id + 1


createVpnOutboundFirewallPolicies(baseurl, https_port, api_token, tunnel_name, local_group, remote_group)
createVpnInboundFirewallPolicies(baseurl, https_port, api_token, tunnel_name, remote_group, local_group)

setConfigCheckpoint(baseurl, https_port, api_token, "after initial config")


# create journal entry
objectType = "dcim.device" 
userID = input("enter your userID here: ")
kind = "info"

nb.extras.journal_entries.create([
     {
        "assigned_object_type" : objectType,
            "assigned_object_id": fgt_serial,
            "created_by": userID,
            "kind": kind,
            "comments": date + comment
     }])
