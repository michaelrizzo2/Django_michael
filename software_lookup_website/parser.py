import json 
with open('software_lookup_website/json_small.json', 'r') as fcc_file:
    data=json.load(fcc_file)
    for entry in data:
        columns_needed=["Sws","Details","Domain Instance","Core Files","Applications"]
        
        print(entry['sws_info'])