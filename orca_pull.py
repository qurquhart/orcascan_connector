import xml.etree.ElementTree as ET
import urllib.request
import csv
import os

def orca_connector(integration_url, netsuite_itemcsv_filepath, postman_collection, postman_environment):
    '''extract data from orcascan and compare it to NetSuite item CSV
    output data to json for PATCH request'''
    
    # pull xml data
    orca_url = urllib.request.urlopen(integration_url + '.xml')

    # initialize elementree
    root = ET.parse(orca_url).getroot()

    # for defining range() of loop
    postcount = len(root)

    # netsuite csv data containing inventory items - Required: Internal ID, Master SKU
    input_file = csv.DictReader(open(netsuite_itemcsv_filepath, encoding='utf-8'))

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


    # write CSV file, creating directory if not present
    os.makedirs(os.path.dirname('output/'), exist_ok=True)

    keys = output_list[0].keys()

    with open('output/orca_info.csv', 'w') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_list)

    print("File created.")

    os.system(f"newman run {postman_collection} -d .\\output\\orca_info.csv -e {postman_environment}")