import json
import xmltodict

with open("JMdict_e") as xml_file:
    data_dict = xmltodict.parse(xml_file.read(), encoding='utf-8', disable_entities=False)
    # xml_file.close()

    # generate the object using json.dumps()
    # corresponding to json data

    json_data = json.dumps(data_dict, indent=2, ensure_ascii=False)

    # Write the json data to output
    # json file
    with open("data.json", "w") as json_file:
        json_file.write(json_data)
