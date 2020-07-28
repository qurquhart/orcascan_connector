import xml.etree.ElementTree as ET
import urllib.request
import csv
import os
from logger import Logger

def orca_connector(integration_url, netsuite_itemcsv_filepath, postman_collection, postman_environment):
    '''extract data from orcascan and compare it to NetSuite item CSV
    output data to json for PATCH request'''

    # logging
    log = Logger("activity_log.txt", "orca_connector")
    emails = ["quinn@portableblowout.com"]
    error = Logger("error_log.txt", "orca_connector", True, "pbautomated@gmail.com", "jkl1432l", emails, "Error log: orca_connector()")

    try:
        # pull xml data
        orca_url = urllib.request.urlopen(integration_url + '.xml')

        # initialize elementree
        root = ET.parse(orca_url).getroot()

        # for defining range() of loop
        postcount = len(root)

        log.text('Parsed orcascan URL successfully.')

    except Exception as ex:
        error.text(f"Cannot parse orcascan URL: {ex}")
        raise

    try:
        # netsuite csv data containing inventory items - Required: Internal ID, Master SKU
        input_file = csv.DictReader(open(netsuite_itemcsv_filepath, encoding='utf-8'))
        log.text('NetSuite item data loaded successfully.')

    except Exception as ex:
        error.text(f"Cannot load NetSuite item data: {ex}")
        raise


    # to be written to json
    output_list = []

    for row in input_file:
        for i in range(postcount):

            # tree definitions
            quantity = root[i].find("Quantity").text
            master_sku = root[i].find("Sku").text

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

    try:
        os.makedirs(os.path.dirname('output/'), exist_ok=True)

    except Exception as ex:
        error.text('Unable to create "output/" directory.')
        raise

    try:
        keys = output_list[0].keys()

        with open('output/orca_info.csv', 'w', newline='') as output:
            dict_writer = csv.DictWriter(output, keys)
            dict_writer.writeheader()
            dict_writer.writerows(output_list)

    except Exception as ex:
        error.text(f'Unable to write to CSV: {ex}')
        raise

 
    log.text("Created JSON PATCH data.")

    try:
        os.system(f"newman run {postman_collection} -d .\\output\\orca_info.csv -e {postman_environment}")
        log.text(f"Successfully PATCHed {len(output_list)} entries to NetSuite.")
    except Exception as ex:
        error.text(f'Newman could not run, unable to PATCH NetSuite: {ex}')
        raise