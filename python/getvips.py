
import pynetbox
from postman import *
from netaddr import *

nb = pynetbox.api(
    '<netboxurlhere>',
    token='<tokenhere>'
)


devices = nb.dcim.devices.filter(manufacturer="fortinet", tenant="<sometenant>")

for device in devices:
    #print(dict(device))
    fgt_device_id = device.id
    fgt_serial = device.serial
    
    #for attr in dir(device.primary_ip):
    #    print("obj.%s = %r" % (attr, getattr(device.primary_ip, attr)))
    
    device_primary_ip = IPNetwork(device.primary_ip.address)

    print(device.name)
    print(fgt_serial)

    baseurl = str(device_primary_ip.ip)
    https_port = "10443"
    api_token = input("token for api user: ")

    try:
        r = getVips(baseurl, https_port, api_token)
        print(r.json())

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise