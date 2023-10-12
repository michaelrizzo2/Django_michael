import json 
with open('software_lookup_website/json_small.json', 'r') as fcc_file:
    for file in fcc_file.readlines():
        print (type(file))