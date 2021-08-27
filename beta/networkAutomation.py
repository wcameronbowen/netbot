# string together modules

from fortigate import *
from typing import Set
from netbox import *

# testing pynetbox
import pynetbox
nb = pynetbox.api(
    '<netboxurlhere>',
    token='<tokenhere>'
)


manufacturer = "fortinet"
slug = "<netboxslughere>"
fortigateUrl = "<fortigaturlhere>"
fortigateToken = ""
interfaceName = "<interfacename>"
#
#


devices = nb.dcim.devices.filter(role='firewall', manufacturer=manufacturer, site=slug)
for device in devices:
    #print(dict(device))
    fgt_device_id = device.id
    print(fgt_device_id)

    interfaces = nb.dcim.interfaces.filter(device_id=fgt_device_id)
    for interface in interfaces:
        if interface.tagged_vlans:
    #        if interface.parent['display'] == 'internal1':
    #            print("works")
    #            #print(interface.parent["id"])
    #            print(interface.parent['display'])
            if interface.parent:
                interface_parent = interface.parent['display']
                interface_id = interface.id
                name = interface.name
                for tagged in interface.tagged_vlans:
                    vlanid = tagged.vid
    
                ips = nb.ipam.ip_addresses.filter(device_id=fgt_device_id, interface_id=interface_id)
                for ip in ips:
                    print(dict(ip))
                    #print(ip.address)
                    ip = ip.address
    
    
                    print(name)
                    #print(type)
                    print(vlanid)
                    #print(role)
                    #print(alias)
                    print(interface_parent)
                    #print(mode)
                    print(ip)
                    #print(allowaccess)
                    #print(vdom)

#vlans = nb.ipam.prefixes.filter(role='<rolehere>')
#for vlan in vlans:
#    print(dict(vlan))


#interfaces = nb.dcim.interfaces.filter(device_id=fgt_device_id)
#for interface in interfaces:
#    if interface.parent:
#        if interface.parent['display'] == 'internal1':
#            print("works")
#            #print(interface.parent["id"])
#            print(interface.parent['display'])
#            interface_parent = interface.parent['display']
#            interface_id = interface.id
#        #print(interface.parent['display'])
#            print(dict(interface))
#            name = interface.name
#            for tagged in interface.tagged_vlans:
#                vlanid = tagged.vid



#interfaces = nb.dcim.interfaces.filter(device_id=fgt_device_id)
#for interface in interfaces:
#    if interface.parent:
##        if interface.parent['display'] == 'internal1':
##            print("works")
##            #print(interface.parent["id"])
##            print(interface.parent['display'])
#            interface_parent = interface.parent['display']
#            interface_id = interface.id
#
#            ips = nb.ipam.ip_addresses.filter(device_id=fgt_device_id, interface_id=interface_id)
#            for ip in ips:
#                print(dict(ip))
#                #print(ip.address)
#                ip = ip.address


#        #print(interface.parent['display'])
#            print(dict(interface))
#            name = interface.name
#            for tagged in interface.tagged_vlans:
#                vlanid = tagged.vid







#
#ips = nb.ipam.ip_addresses.filter(device_id=fgt_device_id, interface_id=interface_id)
#for ip in ips:
#        print(dict(ip))
#        #print(ip.address)
#        ip = ip.address


#
#       payload = json.dumps({
#          "name": f"{intname}",
#          "type": "vlan",
#          "vlanid": {vlanid},
#          "role": "lan",
#          "alias": f"{alias}",
#          "interface": "<interfacehere>",
#          "mode": "static",
#          "ip": f"{ip} {mask}",
#          "allowaccess": "ping",
#          "vdom": "root"
#        })
#print(dict(interfaces))



#
#vlaninterface = {
#        'name': "<nameofinterface>",  name of netbox interface
#        'vlanid': <vlanid>,  vlanid on prefix
#        'alias': '<role>', name of role on prefix
#        'interface': "<parentint>",  name of parent interface
#        'ip': f"{interfaceIP}",     interface ip
#        'allowaccess': 'PING',     statically set
#        }
#
#print(vlan["name"])
#print(vlan["ip"])
#setSystemInterfaceVlan(fortigateUrl, fortigateToken, vlan["name"], vlan["vlanid"], vlan["alias"], vlan["interface"], vlan["ip"], vlan["allowaccess"])

#for vlan in childinterfaces :
#    print(vlan)
#    print(vlan["name"])

#print(childinterfaces)
#
#
#def buildvlanobject(interfaceName) :
#
#    siteID = getSiteID(netboxUrl, netboxToken, slug)
#    deviceID = getdeviceid(netboxUrl, netboxToken, siteID, manufacturer)
#    interfaceID = getnamedinterface(netboxUrl, netboxToken, deviceID, interfaceName)
#    childinterfaces = getchildinterfaces(netboxUrl, netboxToken, deviceID, interfaceID)
#    vlanobjects = []
#
#
#    for childinterface in childinterfaces :
#        interfaceID = childinterface["id"]
#        #interfaceproperties = getinterfaceproperties(netboxUrl, netboxToken, interfaceID)
#        #print(interfaceproperties)
#        
#        #name
#        name = childinterface["name"]
#        
#        #vlanid
#        if (childinterface["untagged_vlan"] != None) :
#            vlanid = childinterface["untagged_vlan"]["vid"]
#        else :
#            vlanid = "1"
#
#        #alias
#        if (childinterface["untagged_vlan"] != None) :
#            vlanID = childinterface["untagged_vlan"]["id"]
#            vlanproperties = getvlanproperties(netboxUrl, netboxToken, vlanID)
#
#        if vlanproperties :
#            alias = vlanproperties["role"]["slug"]
#        else :
#            alias = "test"
#
#        #interface
#        interface = "test"
#
#        #ip
#        ip = getipofinterface(netboxUrl, netboxToken, interfaceID)
#
#        #allowaccess
#        allowaccess = "PING"
#
#        object = {"name": name, "vlanid": vlanid, "alias": alias, "interface": interface, "ip": ip, "allowaccess": allowaccess}
#        vlanobjects.append(object)
#
#    #print(vlanobjects)
#
#
#    #interfaceIP = getipofinterface(netboxUrl, netboxToken, interfaceID)
#    #interfaceproperties = getinterfaceproperties(netboxUrl, netboxToken, interfaceID)
#    #
#        
#    
#    #vlanobjects = []
#
#
#
#    return(vlanobjects)
#
#
#vlanobjects = buildvlanobject(interfaceName)
##print(vlanobjects)
#for vlanobject in vlanobjects :
#    print(setSystemInterfaceVlan(fortigateUrl, fortigateToken, vlanobject))
