# to do
# clone unifi controller image #(docker maybe?)

import requests


oppor_mgmt_ips = ["<ipwmaskhere>","x.x.x.x"]


# variables

basenetboxURL = "<netboxurl>"
fortigate = <ip>
unifi = {{unifi_controller_ip}}
netbox_site_slug = "<slughere>"

input "client ID?"
clientID = input above



# netbox info



input "what is client name or ID in netbox?"
netbox_site_ID = <siteid>



get.netbox.site() {
        import requests

        url = "{{basenetboxURL}}/dcim/sites/?slug={{netbox-slug}}"

        payload={}
        headers = {
          'Accept': 'application/json',
          'Authorization': 'Token <tokenhere>'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

        class Site():
            def __init__(self):
                self.name = response.results.array.name
                self.id = response.results.array.id
}

get prefixes for site from netbox into array of # objects maybe?

get.site.prefixes() {
        import requests

        url = "{{basenetboxURL}}/ipam/prefixes/?site_id={{<siteidhere>}}"

        payload={}
        headers = {
          'Accept': 'application/json',
          'Authorization': 'Token <tokenhere>'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

}

get.site.fortigate.devices() {
        import requests

        url = "{{basenetboxURL}}/dcim/devices/?site_id={{nb_site_id}}&manufacturer={{fortinet}}"

        payload={}
        headers = {
          'Accept': 'application/json',
          'Authorization': 'Token <tokenhere>'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        return(response.results)


        class Fortigate():
            def __init__(self):
                self.name = response.results.array. name
                self.deviceID = response.results.array.id
                self.vlan1.ip = response.results.array.?
}




# fortigate pre-setup script

fortigate.prep () {

    generate fortigate-api-key
    fortigate-api-key = some way to randomly generate

        # setup api profile
        config system accprofile
            edit "api_admin"
                set secfabgrp read-write
                set ftviewgrp read-write
                set authgrp read-write
                set sysgrp read-write
                set netgrp read-write
                set loggrp read-write
                set fwgrp read-write
                set vpngrp read-write
                set utmgrp read-write
                set wanoptgrp read-write
                set wifi read-write
            next
        end

        # setup api user
        config system api-user
            edit "api_admin"
                set api-key ENC {{fortigate-api-key}}
                set accprofile "api_admin"
                set vdom "root"
                config trusthost
                    edit 1
                        set ipv4-trusthost <trustedhost>
                    next
                    edit 2
                        set ipv4-trusthost <trustedhost>
                    next
                    edit 3
                        set ipv4-trusthost <trustedhost>
                    next
                end
            next
        end

        # set web portal to 10443
        config system global
            set admin-port <adminport>
            set admin-sport <adminport>
        end

        config system dhcp server
            delete 1
        end

        # setup internal interface
        config system interface
            edit <interface>
                set alias <alias>
                set vdom root
                set ip {{fortigate_internal_ip}}
                set allowaccess ping https ssh http
                set type hard-switch
                set role lan
            next
        end

}















# fortigate pre-setup

run find/replace on fortigate template script and generate new script
run new script against fortigate #(figure out how to setup api keys with ssh script)






slug > prefixes > ip > device/interface