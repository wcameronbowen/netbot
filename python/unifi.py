import requests
import json
import requests

def login(controllerIP, api_user, api_password):
    url = f"https://{controllerIP}:8443/api/login"

    payload = json.dumps({
        "username": api_user,
        "password": api_password
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)


def get_site_settings(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/setting"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def set_site_locale(controllerIP, site_ID, locale_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/setting/locale/{locale_ID}"

    payload = json.dumps({
      "timezone": "America/Chicago"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def get_site_connectivity(controllerIP, site_ID, connectivityID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/set/setting/connectivity/{connectivityID}"

    payload = json.dumps({
      "enabled": False
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def set_site_network_optimization(controllerIP, site_ID, network_opt_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/set/setting/network_optimization/{network_opt_ID}"

    payload = json.dumps({
      "enabled": False
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def set_controller_settings(controllerIP, site_ID, super_mgmtID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/set/setting/super_mgmt/{super_mgmtID}"

    payload = json.dumps({
      "override_inform_host": True,
      "discoverable": True,
      "data_retention_time_enabled": True,
      "data_retention_time_in_hours_for_5minutes_scale": 12,
      "data_retention_time_in_hours_for_hourly_scale": 720,
      "data_retention_time_in_hours_for_daily_scale": 744,
      "data_retention_time_in_hours_for_monthly_scale": 8760,
      "data_retention_time_in_hours_for_others": 720
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def set_controller_name(controllerIP, site_ID, super_ident_ID, client_ID, hostname):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/set/setting/super_identity/{super_ident_ID}"
    
    payload = json.dumps({
      "name": client_ID,
      "hostname": hostname
    })
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    #print(response.text)
    return(response)

def set_user_group(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/usergroup"

    payload = json.dumps({
      "qos_rate_max_down": 4000,
      "qos_rate_max_up": 2000,
      "name": "public_wifi"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def get_user_group(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/usergroup"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def create_vlan(controllerIP, site_ID, alias, vlan_id):
    url = f"{controllerIP}/api/s/{site_ID}/rest/networkconf"

    payload = json.dumps({
      "purpose": "vlan-only",
      "name": alias,
      "vlan": str(vlan_id),
      "enabled": True,
      "is_nat": True,
      "vlan_enabled": True
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def get_networks(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/networkconf"

    payload = ""
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def get_ap_group(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/v2/api/site/{site_ID}/apgroups"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def create_wlan(controllerIP, site_ID, apgroup_ID, ssid, password, network_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/wlanconf"

    payload = json.dumps({
      "enabled": True,
      "security": "wpapsk",
      "wpa_mode": "wpa2",
      "wpa_enc": "ccmp",
      "wlan_band": "both",
      "ap_group_ids": [
        apgroup_ID
      ],
      "name": ssid,
      "x_passphrase": password,
      "networkconf_id": network_ID
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def create_port_profile(controllerIP, site_ID, native_network_ID, voice_network_ID, profile_name, tagged_Networks_IDs):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/portconf"

    payload = json.dumps({
      "poe_mode": "auto",
      "dot1x_ctrl": "force_authorized",
      "native_networkconf_id": native_network_ID,
      "voice_networkconf_id": voice_network_ID,
      "autoneg": True,
      "lldpmed_enabled": True,
      "stp_port_mode": True,
      "egress_rate_limit_kbps_enabled": False,
      "name": profile_name,
      "forward": "customize",
      "tagged_networkconf_ids": tagged_Networks_IDs
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def logout(controllerIP):
    url = f"https://{controllerIP}:8443/api/logout"

    payload = ""
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def get_events(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/stat/event"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def get_wlans(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/wlanconf"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def get_site_stats(controllerIP):
    url = f"https://{controllerIP}:8443/api/stat/sites"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    return(response)

def get_devices(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/stat/device"
    
    payload = ""
    headers = {}
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    #print(response.text)
    return(response)

def delete_network(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/networkconf/60007156871ca403b387ac88"
    
    payload = ""
    headers = {}
    
    response = requests.request("DELETE", url, headers=headers, data=payload)
    
    print(response.text)

def get_networks(controllerIP, site_ID):
    url = f"https://{controllerIP}:8443/api/s/{site_ID}/rest/networkconf"

    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

