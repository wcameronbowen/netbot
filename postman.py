import requests
import json
#import time
import sys
from netaddr import *



def getModelNumber(baseurl, https_port, api_token) :
    """
    uses the fortigate's serial number to "create" a model number

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    :return str: return the first 6 characters of the serial number
    """

    print("getting fortigate model number...")
    url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/global/?access_token={api_token}"

    payload = {}
    headers = {
      'Content-Type': 'application/json',
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        print(response)
    except requests.exceptions.SSLError as err:
        print("Looks like there is a self-signed cert", err)
        input("Hit enter to try without verification...")
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        print(response)
    except requests.exceptions.ConnectionError as err:
        print("failed to authenticate, verify token and url are correct", err)
    except NameError as err: 
        print("no response created, verify token and url are correct", err)

    try:
        print()
        #print(response.json())
    except NameError: 
        print("no response received, verify token is correct and url is correct")

    if (len(response.json()["serial"]) > 6):
        # Accessing out of range element causes error
        ftg_model = response.json()["serial"][0:6].lower()
    else:
        print('Hm, this seems too short to be the serial number')

    #print(ftg_model)
    return(ftg_model)

def getSerialNumber(baseurl, https_port, api_token) :
    """
    gets the serial number of a given fortigate

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    :return str: return the full serial number
    """

    print("getting fortigate model number...")
    url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/global/?access_token={api_token}"

    payload = {}
    headers = {
      'Content-Type': 'application/json',
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        print(response)
    except requests.exceptions.SSLError as err:
        print("Looks like there is a self-signed cert", err)
        input("Hit enter to try without verification...")
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        print(response)
    except requests.exceptions.ConnectionError as err:
        print("failed to authenticate, verify token and url are correct", err)
    except NameError as err: 
        print("no response created, verify token and url are correct", err)

    try:
        print()
        #print(response.json())
    except NameError: 
        print("no response received, verify token is correct and url is correct")

    if (len(response.json()["serial"]) > 6):
        # Accessing out of range element causes error
        ftg_serial = response.json()["serial"]
    else:
        print('Hm, this seems too short to be the serial number')

    #print(ftg_model)
    return(ftg_serial)

def setConfigCheckpoint(baseurl, https_port, api_token, comments=None) :
    """
    sets a config revision checkpoing

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    :param str,optional comments: comment for checkpoint creation
    """

    try:
        print("setting config checkpoint...")
        url = f"https://{baseurl}:{https_port}/api/v2/monitor/system/config-revision/save?access_token={api_token}"

        payload = json.dumps({
          "comments": f"{comments}"
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
      print("Unexpected error:", sys.exc_info()[0])
      raise


def setPasswordPolicy(baseurl, https_port, api_token):
    """
    sets the fortigates global password policy for admins

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    """

    try:
        print("setting password policy...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/password-policy/?access_token={api_token}"

        payload = json.dumps({
          "status": "enable",
          "apply-to": "admin-password",
          "minimum-length": 8,
          "min-lower-case-letter": 0,
          "min-upper-case-letter": 0,
          "min-non-alphanumeric": 0,
          "min-number": 0,
          "change-4-characters": "enable",
          "expire-status": "enable",
          "expire-day": 999,
          "reuse-password": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    

def setAdminUser(baseurl, https_port, api_token) :
    """
    sets the default admin

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    """

    try:
        print("creating new admin user...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/admin/?access_token={api_token}"

        payload = json.dumps({
          "name": "<someusername>",
          "password": "<somepassword>",
          "accprofile": "super_admin",
          "vdom": [
            {
              "name": "root"
            }
          ],
          "force-password-change": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def editAdminUser(baseurl, https_port, api_token) :

    try:
        print("future feature here...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/admin/<someusername>?access_token={api_token}"

        payload = json.dumps({
          "password-expire": "2021-04-16 10:00:00",
          "force-password-change": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setAdminPassword(baseurl, https_port, api_token, old_password, new_password): 

    try:
        url = f"https://{baseurl}:{https_port}/api/v2/monitor/system/change-password/?access_token={api_token}"

        payload = json.dumps({
          "mkey": "admin",
          "old_password": old_password,
          "new_password": new_password
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def getLoggedInAdmins(baseurl, https_port, api_token):
    """
    gets a list of logged in admins

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    """

    try:
        print("getting list of logged in users...")
        url = f"https://{baseurl}:{https_port}/api/v2/monitor/system/current-admins?access_token={api_token}"

        payload = ""
        headers = {
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

        admins = response.json()["results"]

        for admin in admins:
            if admin["admin"] == "admin":
              print("default admin logged in")
              return(admin)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def kickLoggedInAdmins(baseurl, https_port, api_token, admin_id, admin_method):
    """
    kicks logged in admin given admin id and login method

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    :param int admin_id: id of admin to kick
    :param str method
    """
    try:
        print("kicking logged in default admin...")
        url = f"https://{baseurl}:{https_port}/api/v2/monitor/system/disconnect-admins/select?access_token={api_token}"

        #admin_id = str(admin_id)
        payload = json.dumps({ 
          "id": admin_id, 
          "method": admin_method,
          "admins": [
            {
              "id": admin_id, 
              "method": admin_method 
            }
          ] 
        })

        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def deleteAdminUser(baseurl, https_port,  api_token):

    try:
        print("deleting default admin user...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/admin/admin?access_token={api_token}"

        payload = ""
        headers = {}

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setSysSettings(baseurl, https_port, api_token):

    try:
        print("setting feature visibility...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/settings/?access_token={api_token}"

        payload = json.dumps({
          "gui-dos-policy": "enable",
          "gui-local-in-policy": "enable",
          "gui-dynamic-routing": "enable",
          "gui-multiple-utm-profiles": "enable",
          "gui-ips": "enable",
          "gui-allow-unnamed-policy": "disable",
          "gui-domain-ip-reputation": "enable",
          "gui-multiple-interface-policy": "enable",
          "gui-dns-database": "enable",
          "central-nat": "disable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setSysGlobal(baseurl, https_port, api_token, hostname) :

    try:
        print("setting global settings...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/global/?access_token={api_token}"

        payload = json.dumps({
          "hostname": hostname,
          "timezone": "80",
          "admintimeout": "60",
          "admin-port": 80,
          "admin-sport": 443,
          "gui-certificates": "enable",
          "dst": "enable",
          "revision-backup-on-logout": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setAutoupdatePush(baseurl, https_port, api_token):

    try:
        print("setting autoupdate push...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system.autoupdate/push-update/?access_token={api_token}"

        payload = json.dumps({
          "status": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def disableSipAlg(baseurl, https_port, api_token):

    try:
        print("disabling sip alg...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/settings?access_token={api_token}"

        payload = json.dumps({
          "sip-nat-trace": "disable",
          "sip-helper": "disable",
          "default-voip-alg-mode": "kernel-helper-based"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)


    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def getSipHelperID(baseurl, https_port, api_token):

    try: 
        print("getting sip helper id...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/session-helper?access_token={api_token}"

        payload = ""
        headers = {
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

        helpers = response.json()["results"]

        for helper in helpers :
            if helper["name"] == "sip":
                sipHelperID = helper["id"]
                return(sipHelperID)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def deleteSipHelper(baseurl, https_port, api_token, sipHelperID):

    try:
        print("deleting sip alg helper...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/session-helper/{sipHelperID}?access_token={api_token}"

        payload = ""
        headers = {
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)


    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def getInternalVirtualSwitch(baseurl, https_port, api_token): 

    try:
        print("getting list of ports associated with hardware switches")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-switch/?access_token={api_token}"

        payload = {}
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

        switches = response.json()["results"]

        list = []

        for switch in switches:
            ports = switch["port"]
            for port in ports:
                if "internal" in port["name"]:
                    list.append(port["name"])

        return(list)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def getInterface(baseurl, https_port, api_token) : 

    try:
        print("getting list of internal ports not associated with hardware switches")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/interface/?access_token={api_token}"

        payload = {}
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

        interfaces = response.json()["results"]
        list = []

        for interface in interfaces :
            if "internal" in interface["name"] and interface["name"] != "internal":
                list.append(interface["name"])

        return(list)


    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def editInternalVirtualSwitch(baseurl, https_port, api_token): 

    try:
        print("removing all but port 1 from system default internal hardware switch")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-switch/internal?access_token={api_token}"

        payload = json.dumps({
          "port": [
            {
              "name": "internal1"
            }
          ]
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def createVirtualSwitch(baseurl, https_port, api_token) :

    try:
        print("creating **new_switch** hardware switch")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-switch/?access_token={api_token}"

        payload = json.dumps({
          "name": "new_switch",
          "physical-switch": "sw0",
          "port": [
            {
              "name": "internal2"
            },
            {
              "name": "internal3"
            },
            {
              "name": "internal4"
            }
          ]
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setNetworkInterfacesVlan1(baseurl, https_port, api_token, site_network_id) :

    try:
        print("edit hardware switch interface")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/interface/default_switch?access_token={api_token}"

        payload = json.dumps({
          "ip": "<iphere>",
          "allowaccess": "<allowedservices>",
          "alias": ""
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setNetworkInterfaceVlan(baseurl, https_port, api_token, intname, vlanid, alias, ip):

    try: 
        print(f"create vlan{vlanid}")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/interface/?access_token={api_token}"

        payload = json.dumps({
          "name": intname,
          "type": "vlan",
          "vlanid": vlanid,
          "role": "lan",
          "alias": alias,
          "interface": "internal",
          "mode": "static",
          "ip": ip,
          "allowaccess": "<allowedservices>",
          "vdom": "root"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        print(response)
        ##print(response.text)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setWan1Interface(baseurl, https_port, api_token, wan1_ip) :

    try:
        print("setting wan1 ip")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/interface/wan1?access_token={api_token}"

        payload = json.dumps({
          "name": "wan1",
          "type": "physical",
          "role": "wan",
          "alias": "primary_isp",
          "mode": "static",
          "ip": f"{wan1_ip}",
          "allowaccess": "<allowedservices>",
          "vdom": "root"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setWan2Interface(baseurl, https_port, api_token, wan2_ip) : 

    try:
        print("setting wan2 ip")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/interface/wan2?access_token={api_token}"

        payload = json.dumps({
          "name": "wan2",
          "type": "physical",
          "role": "wan",
          "alias": "secondary_isp",
          "mode": "static",
          "ip": f"{wan2_ip}",
          "allowaccess": "<allowedservices>",
          "vdom": "root"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def deleteDefaultHealthChecks(baseurl, https_port, api_token) : 

    try:
        print("delete default health checks")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-wan-link/health-check/Default_Office_365?access_token={api_token}"

        payload = ""
        headers = {
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)



        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-wan-link/health-check/Default_FortiGuard?access_token={api_token}"

        payload = ""
        headers = {
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)



        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-wan-link/health-check/Default_Google%20Search?access_token={api_token}"

        payload = ""
        headers = {
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)



        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-wan-link/health-check/Default_Gmail?access_token={api_token}"

        payload = ""
        headers = {
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)



        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-wan-link/health-check/Default_AWS?access_token={api_token}"

        payload = ""
        headers = {
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setSDwanSettings(baseurl, https_port, api_token, wan1_gateway, wan2_gateway) :

    try:
        print("setting up sd-wan")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/virtual-wan-link/?access_token={api_token}"

        payload = json.dumps({
          "status": "enable",
          "load-balance-mode": "source-ip-based",
          "fail-detect": "disable",
          "fail-alert-interfaces": [],
          "members": [
            {
              "seq-num": 1,
              "interface": "wan1",
              "gateway": f"{wan1_gateway}",
              "source": "0.0.0.0",
              "cost": 0,
              "weight": 1,
              "priority": 0,
              "spillover-threshold": 0,
              "ingress-spillover-threshold": 0,
              "volume-ratio": 1,
              "status": "enable",
              "comment": ""
            },
            {
              "seq-num": 2,
              "interface": "wan2",
              "gateway": f"{wan2_gateway}",
              "source": "0.0.0.0",
              "cost": 0,
              "weight": 1,
              "priority": 0,
              "spillover-threshold": 0,
              "ingress-spillover-threshold": 0,
              "volume-ratio": 1,
              "status": "disable",
              "comment": ""
            }
          ],
          "health-check": [
            {
              "name": "internet",
              "probe-packets": "enable",
              "addr-mode": "ipv4",
              "server": "\"8.8.8.8\" \"1.1.1.1\"",
              "protocol": "ping",
              "port": 80,
              "security-mode": "none",
              "password": "",
              "packet-size": 64,
              "ha-priority": 1,
              "interval": 60000,
              "probe-timeout": 500,
              "failtime": 10,
              "recoverytime": 10,
              "update-cascade-interface": "enable",
              "update-static-route": "enable",
              "members": [
                {
                  "seq-num": 1
                }
              ],
              "sla": []
            }
          ],
          "neighbor": [],
          "service": [
            {
              "id": 1,
              "name": "default_to_internet",
              "addr-mode": "ipv4",
              "input-device": [],
              "input-device-negate": "disable",
              "mode": "manual",
              "role": "standalone",
              "standalone-action": "disable",
              "quality-link": 0,
              "protocol": 0,
              "start-port": 1,
              "end-port": 65535,
              "route-tag": 0,
              "dst": [
                {
                  "name": "all"
                }
              ],
              "dst-negate": "disable",
              "src": [
                {
                  "name": "all"
                }
              ],
              "dst6": [],
              "src6": [],
              "src-negate": "disable",
              "users": [],
              "groups": [],
              "internet-service": "disable",
              "health-check": "",
              "link-cost-factor": "latency",
              "packet-loss-weight": 0,
              "latency-weight": 0,
              "jitter-weight": 0,
              "bandwidth-weight": 0,
              "link-cost-threshold": 10,
              "hold-down-time": 0,
              "sla": [],
              "priority-members": [
                {
                  "seq-num": 1
                }
              ],
              "status": "enable",
              "gateway": "disable",
              "default": "disable",
              "sla-compare-method": "order"
            }
          ]
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setSDwanRoute(baseurl, https_port, api_token) : 

    try:
        print("settings default sd-wan route")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/router/static/?access_token={api_token}"

        payload = json.dumps({
          "status": "enable",
          "dst": "0.0.0.0 0.0.0.0",
          "gateway": "0.0.0.0",
          "distance": 1,
          "weight": 0,
          "priority": 0,
          "virtual-wan-link": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setBlackholeRoutes(baseurl, https_port, api_token) : 

    try:
        print("setting standard blackhole routes")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/router/static/?access_token={api_token}"

        payload = json.dumps({
          "status": "enable",
          "dst": "10.0.0.0 255.0.0.0",
          "distance": 254,
          "blackhole": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)



        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/router/static/?access_token={api_token}"

        payload = json.dumps({
          "status": "enable",
          "dst": "172.16.0.0 255.240.0.0",
          "distance": 254,
          "blackhole": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)



        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/router/static/?access_token={api_token}"

        payload = json.dumps({
          "status": "enable",
          "dst": "192.168.0.0 255.255.0.0",
          "distance": 254,
          "blackhole": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setDhcpServers(baseurl, https_port, api_token, clientID, ipNetwork, intname, start_ip, end_ip) :

    try:
        print("setting dhcp servers")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system.dhcp/server/?access_token={api_token}"

        payload = json.dumps({
          "status": "enable",
          "dns-service": "specify",
          "dns-server1": "8.8.8.8",
          "dns-server2": "8.8.4.4",
          "domain": f"{clientID}.local",
          "default-gateway": str(ipNetwork.ip),
          "netmask": str(ipNetwork.netmask),
          "interface": intname,
          "ip-range": [
            {
              "id": 1,
              "start-ip": str(start_ip),
              "end-ip": str(end_ip)
            }
          ],
          "timezone-option": "default",
          "lease-time": 86400
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setFirewallAddressObjects(baseurl, https_port, api_token, name, subnet) : 
    
    try:
        print("setting standard address objects")
        #static obj
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/address/?access_token={api_token}"

        payload = json.dumps({
          "name": name,
          "subnet": subnet
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        ##print(response.text)
        print(response)


    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setFirewallAddressObjectsLegacy(baseurl, https_port, api_token, site_network_id) : 
    
    try:
        #phone pbx obj
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/address/?access_token={api_token}"

        payload = json.dumps({
          "name": "ob_addr_hst_phone_server",
          "subnet": "<iphere>"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setFirewallAddressGroups(baseurl, https_port, api_token) :

    try:
        print("setting standard address groups")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/addrgrp/?access_token={api_token}"

        payload = json.dumps({
          "name": "gr_addr_things",
          "member": [
            {
              "name": "ob_addr_thing"
            }
          ],
          "visibility": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setFirewallServiceObjects(baseurl, https_port, api_token) : 

    try:
        print("setting standard service objects")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall.service/custom/?access_token={api_token}"

        payload = json.dumps({
          "name": "ob_svc_udp_port",
          "protocol": "TCP/UDP/SCTP",
          "udp-portrange": "<porthere>"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setFirewallServiceGroups(baseurl, https_port, api_token) : 

    try:
        print("setting standard service object groups")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall.service/group/?access_token={api_token}"

        payload = json.dumps(
          {
            "name": "gr_svc_things",
            "member": [
                    {
                        "name": "ob_svc_udp_port",
                    }
                ]
            })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    

def createFilterProfiles(baseurl, https_port, api_token) : 

    try:
        print("setting standard filter profiles")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/ssl-ssh-profile/?access_token={api_token}"

        payload = json.dumps({
          "name": "default",
          "comment": "Read-only SSL handshake inspection profile",
          "ssl": {
            "inspect-all": "disable",
            "client-cert-request": "bypass",
            "unsupported-ssl": "bypass",
            "allow-invalid-server-cert": "disable",
            "untrusted-cert": "allow"
          },
          "https": {
            "ports": [
              443
            ],
            "status": "certificate-inspection",
            "client-cert-request": "bypass",
            "unsupported-ssl": "bypass",
            "allow-invalid-server-cert": "disable",
            "untrusted-cert": "allow"
          },
          "ftps": {
            "ports": [
              990
            ],
            "status": "disable",
            "client-cert-request": "bypass",
            "unsupported-ssl": "bypass",
            "allow-invalid-server-cert": "disable",
            "untrusted-cert": "allow"
          },
          "imaps": {
            "ports": [
              993
            ],
            "status": "disable",
            "client-cert-request": "inspect",
            "unsupported-ssl": "bypass",
            "allow-invalid-server-cert": "disable",
            "untrusted-cert": "allow"
          },
          "pop3s": {
            "ports": [
              995
            ],
            "status": "disable",
            "client-cert-request": "inspect",
            "unsupported-ssl": "bypass",
            "allow-invalid-server-cert": "disable",
            "untrusted-cert": "allow"
          },
          "smtps": {
            "ports": [
              465
            ],
            "status": "disable",
            "client-cert-request": "inspect",
            "unsupported-ssl": "bypass",
            "allow-invalid-server-cert": "disable",
            "untrusted-cert": "allow"
          },
          "ssh": {
            "ports": [
              22
            ],
            "status": "disable",
            "inspect-all": "disable",
            "unsupported-version": "bypass",
            "ssh-policy-check": "disable",
            "ssh-tun-policy-check": "disable",
            "ssh-algorithm": "compatible"
          },
          "whitelist": "disable",
          "ssl-exempt": [],
          "server-cert-mode": "re-sign",
          "use-ssl-server": "disable",
          "caname": "Fortinet_CA_SSL",
          "untrusted-caname": "",
          "server-cert": "",
          "ssl-server": [],
          "ssl-anomalies-log": "enable",
          "ssl-exemptions-log": "disable",
          "rpc-over-https": "disable",
          "mapi-over-https": "disable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)



        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/antivirus/profile/?access_token={api_token}"

        payload = json.dumps({
          "name": "default",
          "comment": "Scan files and block viruses.",
          "replacemsg-group": "",
          "inspection-mode": "flow-based",
          "ftgd-analytics": "disable",
          "analytics-max-upload": 10,
          "analytics-wl-filetype": 0,
          "analytics-bl-filetype": 0,
          "analytics-db": "disable",
          "mobile-malware-db": "enable",
          "http": {
            "options": "scan",
            "archive-block": "",
            "archive-log": "",
            "emulator": "enable",
            "outbreak-prevention": "disabled",
            "content-disarm": "disable"
          },
          "ftp": {
            "options": "scan",
            "archive-block": "",
            "archive-log": "",
            "emulator": "enable",
            "outbreak-prevention": "disabled"
          },
          "imap": {
            "options": "scan",
            "archive-block": "",
            "archive-log": "",
            "emulator": "enable",
            "executables": "virus",
            "outbreak-prevention": "disabled",
            "content-disarm": "disable"
          },
          "pop3": {
            "options": "scan",
            "archive-block": "",
            "archive-log": "",
            "emulator": "enable",
            "executables": "virus",
            "outbreak-prevention": "disabled",
            "content-disarm": "disable"
          },
          "smtp": {
            "options": "scan",
            "archive-block": "",
            "archive-log": "",
            "emulator": "enable",
            "executables": "virus",
            "outbreak-prevention": "disabled",
            "content-disarm": "disable"
          },
          "mapi": {
            "options": "",
            "archive-block": "",
            "archive-log": "",
            "emulator": "enable",
            "executables": "default",
            "outbreak-prevention": "disabled"
          },
          "nntp": {
            "options": "",
            "archive-block": "",
            "archive-log": "",
            "emulator": "enable",
            "outbreak-prevention": "disabled"
          },
          "smb": {
            "options": "",
            "archive-block": "",
            "archive-log": "",
            "emulator": "enable",
            "outbreak-prevention": "disabled"
          },
          "nac-quar": {
            "infected": "none",
            "expiry": "5m",
            "log": "disable"
          },
          "content-disarm": {
            "original-file-destination": "discard",
            "office-macro": "enable",
            "office-hylink": "enable",
            "office-linked": "enable",
            "office-embed": "enable",
            "pdf-javacode": "enable",
            "pdf-embedfile": "enable",
            "pdf-hyperlink": "enable",
            "pdf-act-gotor": "enable",
            "pdf-act-launch": "enable",
            "pdf-act-sound": "enable",
            "pdf-act-movie": "enable",
            "pdf-act-java": "enable",
            "pdf-act-form": "enable",
            "cover-page": "enable",
            "detect-only": "disable"
          },
          "av-virus-log": "enable",
          "av-block-log": "enable",
          "extended-log": "disable",
          "scan-mode": "full"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)




        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/ips/sensor/?access_token={api_token}"

        payload = json.dumps({
          "name": "default",
          "comment": "Prevent critical attacks",
          "replacemsg-group": "",
          "block-malicious-url": "disable",
          "extended-log": "disable",
          "entries": [
            {
              "id": 1,
              "rule": [],
              "location": "all",
              "severity": "medium high critical ",
              "protocol": "all",
              "os": "all",
              "application": "all",
              "status": "default",
              "log": "enable",
              "log-packet": "disable",
              "log-attack-context": "disable",
              "action": "default",
              "rate-count": 0,
              "rate-duration": 60,
              "rate-mode": "continuous",
              "rate-track": "none",
              "exempt-ip": [],
              "quarantine": "none",
              "quarantine-expiry": "5m",
              "quarantine-log": "enable"
            }
          ],
          "filter": [],
          "override": []
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)




        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/dnsfilter/profile/?access_token={api_token}"

        payload = json.dumps({
          "name": "default",
          "domain-filter": {
            "domain-filter-table": 0
          },
          "ftgd-dns": {
            "options": "error-allow ftgd-disable",
            "filters": [
              {
                "id": 1,
                "q_origin_key": 1,
                "category": 2,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 2,
                "q_origin_key": 2,
                "category": 7,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 3,
                "q_origin_key": 3,
                "category": 8,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 4,
                "q_origin_key": 4,
                "category": 9,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 5,
                "q_origin_key": 5,
                "category": 11,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 6,
                "q_origin_key": 6,
                "category": 12,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 7,
                "q_origin_key": 7,
                "category": 13,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 8,
                "q_origin_key": 8,
                "category": 14,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 9,
                "q_origin_key": 9,
                "category": 15,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 10,
                "q_origin_key": 10,
                "category": 16,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 11,
                "q_origin_key": 11,
                "category": 0,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 12,
                "q_origin_key": 12,
                "category": 57,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 13,
                "q_origin_key": 13,
                "category": 63,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 14,
                "q_origin_key": 14,
                "category": 64,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 15,
                "q_origin_key": 15,
                "category": 65,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 16,
                "q_origin_key": 16,
                "category": 66,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 17,
                "q_origin_key": 17,
                "category": 67,
                "action": "monitor",
                "log": "enable"
              },
              {
                "id": 18,
                "q_origin_key": 18,
                "category": 26,
                "action": "block",
                "log": "enable"
              },
              {
                "id": 19,
                "q_origin_key": 19,
                "category": 61,
                "action": "block",
                "log": "enable"
              },
              {
                "id": 20,
                "q_origin_key": 20,
                "category": 86,
                "action": "block",
                "log": "enable"
              },
              {
                "id": 21,
                "q_origin_key": 21,
                "category": 88,
                "action": "block",
                "log": "enable"
              },
              {
                "id": 22,
                "q_origin_key": 22,
                "category": 90,
                "action": "block",
                "log": "enable"
              },
              {
                "id": 23,
                "q_origin_key": 23,
                "category": 91,
                "action": "block",
                "log": "enable"
              }
            ]
          },
          "log-all-domain": "enable",
          "sdns-ftgd-err-log": "enable",
          "sdns-domain-log": "enable",
          "block-action": "redirect",
          "redirect-portal": "0.0.0.0",
          "block-botnet": "enable",
          "safe-search": "disable",
          "youtube-restrict": "strict",
          "external-ip-blocklist": []
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)


    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def getVips(baseurl, https_port, api_token) :

    try:
        print("getting vips")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/vip/?access_token={api_token}"

        payload = ""
        headers = {
          'Content-Type': 'application/json',
        }


        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setVips(baseurl, https_port, api_token, site_network_id) :

    try:
        print("setting standard vips")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/vip/?access_token={api_token}"

        payload = json.dumps({
          "name": "ob_vip_thing",
          "extip": "<someip>",
          "mappedip": [
            {
              "range": "<someip>"
            }
          ],
          "extintf": "any",
          "portforward": "enable",
          "protocol": "udp",
          "extport": "<someport>",
          "mappedport": "<someport>"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setVipGroup(baseurl, https_port, api_token) :

    try:
        print("setting standard vip groups")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/vipgrp/?access_token={api_token}"

        payload = json.dumps({
          "name": "gr_vip_pritunl",
          "interface": "any",
          "member": [
            {
              "name": "ob_vip_pritunl"
            }
          ]
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def deleteFirewallPolicy(baseurl, https_port, api_token, policy_id="1") :

    try:
        print("deleting default firewall policy")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/policy/{policy_id}?access_token={api_token}"

        payload = {}
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def setFirewallPolicies(baseurl, https_port, api_token) :

    try:
        print("setting standard firewall policies")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/policy/?access_token={api_token}"

        payload = json.dumps({
          "name": "default_to_internet",
          "srcintf": [
            {
              "name": "internal"
            }
          ],
          "dstintf": [
            {
              "name": "virtual-wan-link"
            }
          ],
          "srcaddr": [
            {
              "name": "all"
            }
          ],
          "dstaddr": [
            {
              "name": "all"
            }
          ],
          "action": "accept",
          "status": "enable",
          "schedule": "always",
          "service": [
            {
              "name": "ALL"
            }
          ],
          "av-profile": "default",
          "dnsfilter-profile": "default",
          "ips-sensor": "default",
          "ssl-ssh-profile": "default",
          "nat": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setFirewallLocalInPolicies(baseurl, https_port, api_token) :

    try:
        print("setting local in policies")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/local-in-policy/?access_token={api_token}"

        payload = json.dumps({
          "policyid": 10,
          "intf": "wan1",
          "srcaddr": [
            {
              "name": "all"
            }
          ],
          "dstaddr": [
            {
              "name": "all"
            }
          ],
          "action": "accept",
          "service": [
            {
              "name": "<servicehere"
            }
          ],
          "schedule": "always",
          "status": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setVpnLocalAddressObjects(baseurl, https_port, api_token, tunnel_name, local_addresses) : 
    
    try:
        print("setting tunnel local address objects")
        members = []

        for x, address in enumerate(local_addresses):
          #static obj

          url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/address/?access_token={api_token}"
          name = f"vpn_{tunnel_name}_local_{x}"

          payload = json.dumps({
            "name": f"{name}",
            "subnet": f"{address}",
            "allow-routing": "enable"
          })
          headers = {
            'Content-Type': 'application/json',
          }

          response = requests.request("POST", url, headers=headers, data=payload, verify=False)

          toAppend = {"name": f"{name}"}
          members.append(toAppend)
          ##print(response.text)

        return(members)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def setVpnRemoteAddressObjects(baseurl, https_port, api_token, tunnel_name, remote_addresses) : 
    
    try:
        print("setting tunnel remote address objects")
        members = []

        for x, address in enumerate(remote_addresses):
          #static obj

          url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/address/?access_token={api_token}"
          name = f"vpn_{tunnel_name}_remote_{x}"

          payload = json.dumps({
            "name": f"{name}",
            "subnet": f"{address}",
            "allow-routing": "enable"
          })
          headers = {
            'Content-Type': 'application/json',
          }

          response = requests.request("POST", url, headers=headers, data=payload, verify=False)

          toAppend = {"name": f"{name}"}
          members.append(toAppend)
          ##print(response.text)

        return(members)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def setVpnLocalAddressGroups(baseurl, https_port, api_token, tunnel_name, local_members) :

    try:
        print("setting tunnel local groups")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/addrgrp/?access_token={api_token}"

        payload = json.dumps({
          "name": f"vpn_{tunnel_name}_local",
          "member": local_members,
          "visibility": "enable",
          "allow-routing": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        print(response)
        return(response.json())

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setVpnRemoteAddressGroups(baseurl, https_port, api_token, tunnel_name, remote_members) :

    try:
        print("setting tunnel remote groups")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/addrgrp/?access_token={api_token}"

        payload = json.dumps({
          "name": f"vpn_{tunnel_name}_remote",
          "member": remote_members,
          "visibility": "enable",
          "allow-routing": "enable"
        })
        headers = {
          'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        print(response)
        return(response.json())

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def createPhase1Interface(baseurl, https_port, api_token, phase1_config):

    try:
        print("creating phase1 interface")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/vpn.ipsec/phase1-interface?access_token={api_token}"

        payload = json.dumps(phase1_config)
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def createPhase2Interface(baseurl, https_port, api_token, phase2_config):

    try:
        print("creating phase2 interfaces")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/vpn.ipsec/phase2-interface?access_token={api_token}"

        payload = json.dumps(phase2_config)
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        print(response)
        #print(response.text)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def createVpnStaticRoute(baseurl, https_port, api_token, tunnel_name, static_route_id, phase2_dst_addr):

    try:
        print("creating static routes")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/router/static?access_token={api_token}"

        payload = json.dumps({
          "seq-num": static_route_id,
          "status": "disable",
          "dst": "0.0.0.0 0.0.0.0",
          "src": "0.0.0.0 0.0.0.0",
          #"dst": f"{phase2_dst_addr}",
          "dstaddr": f"{phase2_dst_addr}",
          "gateway": "0.0.0.0",
          "distance": 10,
          "weight": 0,
          "priority": 0,
          "device": f"{tunnel_name}"
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        print(response)
        #print(response.text)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def createVpnOutboundFirewallPolicies(baseurl, https_port, api_token, tunnel_name, local_group, remote_group):

    try:
        print("creating outbound firewall policy")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/policy?access_token={api_token}"

        payload = json.dumps({
          "name": f"vpn_{tunnel_name}_outbound",
          "srcintf": [
            {
              "name": "any"
            }
          ],
          "dstintf": [
            {
              "name": tunnel_name
            }
          ],
          "srcaddr": [
            {
              "name": local_group["mkey"]
            }
          ],
          "dstaddr": [
            {
              "name": remote_group["mkey"]      
            }
          ],
          "action": "accept",
          "status": "disable",
          "schedule": "always",
          "service": [
            {
                "name": "ALL"
            }
          ],
          "nat": "disable"
        })

        headers = {
          'Content-Type': 'application/json'
        }

        #print(payload)
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def createVpnInboundFirewallPolicies(baseurl, https_port, api_token, tunnel_name, remote_group, local_group): 

    try:
        print("creating inbound firewall policy")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/firewall/policy?access_token={api_token}"

        payload = json.dumps({
          "name": f"vpn_{tunnel_name}_inbound",
          "srcintf": [
              {
                  "name": f"{tunnel_name}"
              }
          ],
          "dstintf": [
              {
                  "name": "any"
              }
          ],
          "srcaddr": [
              {
                  "name": remote_group["mkey"]
              }
          ],
          "dstaddr": [
              {
                  "name": local_group["mkey"]
              }
          ],
          "action": "accept",
          "status": "disable",
          "schedule": "always",
          "service": [
              {
                  "name": "ALL"
              }
          ],
          "nat": "disable"
        })

        headers = {
          'Content-Type': 'application/json'
        }

        #print(payload)
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        print(response)
        #print(response.text)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setLogDiskFilter(baseurl, https_port, api_token):

    try:
        print("setting disk log filter...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/log.disk/filter?access_token={api_token}"

        payload = json.dumps({
          "severity": "information"
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def setLogDiskSetting(baseurl, https_port, api_token):

    try:
        print("setting disk log settings...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/log.disk/setting?access_token={api_token}"

        payload = json.dumps({
          "status": "enable",
          "maximum-log-age": 30
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        #print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def setLogMemoryFilter(baseurl, https_port, api_token):

    try:
        print("setting memory log filter...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/log.memory/filter?access_token={api_token}"
    
        payload = json.dumps({
          "severity": "information"
        })
        headers = {
          'Content-Type': 'application/json'
        }
    
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
    
        #print(response.text)
        print(response)
    
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def setLogMemorySetting(baseurl, https_port, api_token):

    try:
        print("setting memory log settings...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/log.memory/setting?access_token={api_token}"

        payload = json.dumps({
          "status": "enable"
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



def deleteApiUser(baseurl, https_port, api_token):

    try:
        print("cleaning up api access...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/api-user/api_admin?access_token={api_token}"

        payload = ""
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def createApiUser(baseurl, https_port, api_token):

    try:
        print("creating backup user...")
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/api-user/?access_token={api_token}"

        payload = json.dumps({
          "name": "backup_admin",
          "comments": "used to grab backups",
          "accprofile": "super_admin_readonly",
          "trusthost": [
            {
              "type": "ipv4-trusthost",
              "ipv4-trusthost": "<somehost>"
            },
            {
              "type": "ipv4-trusthost",
              "ipv4-trusthost": "<sonehost>"
            },
            {
              "type": "ipv4-trusthost",
              "ipv4-trusthost": "<somehost>"
            }
          ]
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)
        return(response)
        

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def generateApiUserKey(baseurl, https_port, api_token, username):

    try:
        print("resetting backup user key...")
        url = f"https://{baseurl}:{https_port}/api/v2/monitor/system/api-user/generate-key?access_token={api_token}"

        payload = json.dumps({
          "api-user": username
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        print(response)
        #print(response.results["access_token"])
        return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def getCustomLogField(baseurl, https_port, api_token):
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
    

def setCustomLogField(baseurl, https_port, api_token, log_name, log_value):
    """
    sets a custom log field

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    :param str id: id associated with custom log field (can be any integer)
    :param str log_name: name of the custom field
    :param str log_value: value that will be put into that custom field 
       note, cannot be more than 15 characters
    """
    
    try:
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/log/custom-field?access_token={api_token}" 

        payload = json.dumps({   
          "id" : log_name,
          "name": log_name,  
          "value": log_value
          })
        headers = {
          'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise




def setAutomationAction(baseurl, https_port, api_token, payload):

    try:
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/automation-action?access_token={api_token}"

        payload = json.dumps(payload)

        headers = {
          'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setAutomationTrigger(baseurl, https_port, api_token, payload):

    try:
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/automation-trigger?access_token={api_token}"

        payload = json.dumps(payload)

        headers = {
          'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def setAutomationStitch(baseurl, https_port, api_token, payload):

    try:
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/system/automation-stitch?access_token={api_token}"

        payload = json.dumps(payload)

        headers = {
          'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def setLogSettings(baseurl, https_port, api_token, payload):
    """
    sets custom log fields in general log settings

    :param str baseurl: The base URL to the fortigate you wish to connect to.
    :param str api_token: api user token.
    :param str id: id associated with custom log field (can be any integer)
    :param str log_name: name of the custom field
    :param str (json) payload: payload for api request
    """
    
    try:
        url = f"https://{baseurl}:{https_port}/api/v2/cmdb/log/setting?access_token={api_token}" 

        headers = {
          'Content-Type': 'application/json',
        }
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        #print(response.text)
        return(response)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise