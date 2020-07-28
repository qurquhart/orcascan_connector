from orca_pull import orca_connector


# orcascan integration URL
integration_url = 'https://api.orcascan.com/sheets/xxxxxxxxxxxxxx'

# netsuite csv data containing inventory items - Required: Internal ID, Master SKU
netsuite_itemcsv_filepath = 'items.csv'

# postman collection and environment variables
postman_collection = '.\\postman\\postman_collection.json'
postman_environment = '.\\postman\\postman_environment.json'
postman_data = '.\\output\\postman_data.csv'

# REQUIRES NEWMAN - https://github.com/postmanlabs/newman
orca_connector(integration_url,
               netsuite_itemcsv_filepath,
               postman_collection,
               postman_environment,
               postman_data
               )
