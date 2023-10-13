import json 
with open('software_lookup_website/json_small.json', 'r') as fcc_file:
    data=json.load(fcc_file)
    for i in data:
        print(i['sws_info'])