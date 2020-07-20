import xml.etree.ElementTree as ET
import urllib.request
import json
import csv
import time
import os

def orca_parse(integration_url):
    '''extract data from orcascan and compare it to NetSuite item CSV
    output data to json for PATCH request'''
    
    # pull xml data
    orca_url = urllib.request.urlopen(integration_url + '.xml')

    # initialize elementree
    root = ET.parse(orca_url).getroot()

    # for defining range() of loop
    postcount = len(root)

    # csv data containing inventory items - Required: Master SKU, Quantity
    input_file = csv.DictReader(open('items.csv', encoding='utf-8'))

    # to be written to json
    output_list = []



    for row in input_file:
        for i in range(postcount):

            # tree definitions
            quantity = root[i][6].text
            master_sku = root[i][11].text

            if master_sku:

                # to be added output_list
                temp_dict = {}

                # if the master sku matches a line, add the data to json
                if row["Master SKU"] == master_sku:

                    if quantity:
                        temp_dict.update({
                            "internal_id": row["Internal ID"],
                            "custitem_orcascan_qty": quantity
                        })
                        output_list.append(temp_dict)


    # write file, creating directory if not present
    os.makedirs(os.path.dirname('output/'), exist_ok=True)
    date = time.strftime("%m-%d-%Y_%H-%M-%S")
    f = open(f'output/{date}_orca_info.json', 'w')
    f.write(json.dumps(output_list))
    f.close()

    print("File created.")
