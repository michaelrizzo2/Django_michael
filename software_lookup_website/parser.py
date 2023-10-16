import json 
with open('software_lookup_website/json_small.json', 'r') as fcc_file:
    data=json.load(fcc_file)
    print(len(data))
    for entry in data:
        dictionary_for_data={"Sws":"Fenix","Details":"description","Domain Instance":"domain","Core Files":"sws_info","Applications":"sws_info"}
        for key,value in dictionary_for_data.items():
            if key in ["Core Files","Applications"]:
                if key == "Core Files":
                    print(entry[value]["Core Files"])
                if key == "Applications":
                    print(entry[value]["Apps"])
            else:
                print(entry[value])
    print("===================================") 