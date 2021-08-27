import csv
import pynetbox
import requests
import json
import sys

# disable requests submodule warnings
requests.packages.urllib3.disable_warnings()

nb = pynetbox.api(
    '<netboxurlhere>',
    token='<tokenhere>'
)


with open('netbox-ips.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for x, row in enumerate(csv_reader):
        if x == 0:
            print(f'Column names are {", ".join(row)}')
        else:

            devices = nb.dcim.devices.filter(name=row[0])
            for device in devices:
                #print(dict(device))
                print(device.name)
                device_id = device.id
                tenant_name = device.tenant.name
                tenant_slug = device.tenant.slug


                interfaces = nb.dcim.interfaces.filter(device_id=device_id, name=row[2])
                if interfaces:
                    for interface in interfaces:
                        if row[2] in interface.name:
                            print(f"{row[2]} exists")
                            interface_id = interface.id

                            print("assigning ip address to existing interface")
                            rs = nb.ipam.ip_addresses.create([{
                              "address": row[1],
                              "assigned_object_type": "dcim.interface",
                              "assigned_object_id": interface_id,
                              "tenant": {
                                  "name": tenant_name,
                                  "slug": tenant_slug
                                }
                            }])
                            for r in rs:
                                print(f"successfully set {r.address}")

                else: 
                    print(f"creating {row[2]}")
                    rs = nb.dcim.interfaces.create([
                     {
                        "device": device_id,
                        "name": row[2],
                        "type": "virtual"
                     }
                    ])
                    for r in rs:
                     #print(dict(r)) 
                     interface_id = r.id
                     #sys.exit(f"created {r.name}")

                    print("assigning ip address to new interface")
                    rs = nb.ipam.ip_addresses.create([{
                      "address": row[1],
                      "assigned_object_type": "dcim.interface",
                      "assigned_object_id": interface_id,
                      "tenant": {
                          "name": tenant_name,
                          "slug": tenant_slug
                        }
                    }])
                    for r in rs:
                        print(f"successfully set {r.address} to {r.tenant} and {device.name}")

    print(f'Processed {x} lines.')
