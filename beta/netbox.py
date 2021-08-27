import requests
import json


def getSiteID(netboxUrl, netboxToken, slug) :


    url = netboxUrl + "/api/dcim/sites/" + "?slug=" + slug

    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)
    siteID = object["results"][0]["id"]

    #print(siteID)
    return(siteID)


def getprefixes(netboxUrl, netboxToken, siteID) :

    url = netboxUrl + "/api/ipam/prefixes/" + "?site_id=" + str(siteID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    prefixes = object["results"]
    return(prefixes)
    #for prefix in prefixes :
        #prefix = object["results"][prefix]["id"]
        #print(prefix)
        #print(prefix["id"])
        #return(prefix["id"])

def getprefixfromip(netboxUrl, netboxToken, ipID) :

    url = netboxUrl + "/api/ipam/prefixes/" + "?site_id=" + str(siteID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    prefixes = object["results"]
    return(prefixes)
    #for prefix in prefixes :
        #prefix = object["results"][prefix]["id"]
        #print(prefix)
        #print(prefix["id"])
        #return(prefix["id"])


def getipsfromprefix(netboxUrl, netboxToken, prefixID) :

    url = netboxUrl + "/api/ipam/ip-addresses/" + "?interface_id=" + str(prefixID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    ips = object["results"]
    return(ips)
    #for ip in ips :
        #prefix = object["results"][prefix]["id"]
        #print(ip)
        #print(ip["id"])
        #print(ip["address"])
        #return(ip["address"])


def getipofinterface(netboxUrl, netboxToken, interfaceID) :

    url = netboxUrl + "/api/ipam/ip-addresses/" + "?interface_id=" + str(interfaceID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    ips = object["results"]
    #return(ips)
    for ip in ips :
        return(ip["address"])


def getinterfacesfromip(netboxUrl, netboxToken, ipID) :

    url = netboxUrl + "/api/dcim/interfaces/" + "?ip=" + str(ipID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    interfaces = object["results"]
    return(interfaces)
    #for interface in interfaces :
        #prefix = object["results"][prefix]["id"]
        #print(interface)
        #print(interface["id"])
      #if interface
        #return(interface["id"])
        

def getinterfaces(netboxUrl, netboxToken, deviceID) :

    url = netboxUrl + "/api/dcim/interfaces/" + "?device_id=" + str(deviceID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    interfaces = object["results"]
    return(interfaces)
    #for interface in interfaces :
        #prefix = object["results"][prefix]["id"]
        #print(interface)
        #print(interface["id"])
    #    if (interface["name"] == "internal1") :
    #      return(interface["id"])

def getnamedinterface(netboxUrl, netboxToken, deviceID, interfaceName) :

    url = netboxUrl + "/api/dcim/interfaces/" + "?device_id=" + str(deviceID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    interfaces = object["results"]

    for interface in interfaces :
        #prefix = object["results"][prefix]["id"]
        #print(interface)
        #print(interface["id"])
        if (interface["name"] == interfaceName ) :
          return(interface["id"])
        

def getdevices(netboxUrl, netboxToken, siteID, manufacturer) :

    url = netboxUrl + "/api/dcim/devices/" + "?manufacturer=" + manufacturer + "&site_id=" + str(siteID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    devices = object["results"]
    return(devices)


def getdeviceid(netboxUrl, netboxToken, siteID, manufacturer) :

    url = netboxUrl + "/api/dcim/devices/" + "?manufacturer=" + manufacturer + "&site_id=" + str(siteID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    devices = object["results"]
    for device in devices :
        return(device["id"])


def getinterfaceproperties(netboxUrl, netboxToken, interfaceID) :

    url = netboxUrl + "/api/dcim/interfaces/" + str(interfaceID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)
    interfaces = object
    return(interfaces)
    #for interface in interfaces :
        #prefix = object["results"][prefix]["id"]
        #print(interface)
        #print(interface["id"])
    #    if (interface["name"] == "internal1") :
    #      return(interface["id"])


def getchildinterfaces(netboxUrl, netboxToken, deviceID, interfaceID) :

    url = netboxUrl + "/api/dcim/interfaces/" + "?device_id=" + str(deviceID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)

    interfaces = object["results"]
    #print(interfaces)
    childinterfaces = []
    for interface in interfaces :
        #print(interface)
        if interface["parent"] :
          if (interface["parent"]["id"] == interfaceID) :
            #name = interface["name"]
            #id = interface["id"]
            #type = interface["type"]["value"]
            #object = {"name": name, "id": id, "type": type}
            #childinterfaces.append(object)
            
            childinterfaces.append(interface)
            
            #childinterfaces[f'{name}']= {
            #                              "id": id,
            #                              "type": type
            #                            }
           #return(interface["id"])
    #print(childinterfaces)
    return(childinterfaces)

def getvlanproperties(netboxUrl, netboxToken, vlanID) :
    url = netboxUrl + "/api/ipam/vlans/" + str(vlanID)


    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Token {netboxToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    object = json.loads(response.text)
    return(object)
