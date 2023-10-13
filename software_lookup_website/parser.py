import json 
with open('software_lookup_website/json_small.json', 'r') as fcc_file:
    data=json.load(fcc_file)
    for entry in data:
        dictionary_for_data={"Sws":"Fenix","Details":"description","Domain Instance":"domain","Core Files":"sws_info","Applications":"sws_info"}
        for key,value in dictionary_for_data.items():
            if key == "Core Files":
                print(entry[value]["Apps"])
            if key == "Applications":
                print(entry[value]["Core Files"])
            #This will call the entries without nested dictionaries
            else:
                print(entry[value])
        