import json
import xmltodict
import pandas as pd
import pandas_read_xml as pdx

with open("JMdict_e_examp.xml", 'r', encoding='utf-8') as xml_file:
    data_dict = xmltodict.parse(xml_file.read(), disable_entities=False)
    xml_file.close()
# print(type(data_dict))

# count = 0
# for key, value in data_dict.items():
#     print(value)
#     count+=1
#     if count>5:
#         break

    # generate the object using json.dumps()
    # corresponding to json data

# import xml.etree.ElementTree as E
# tree = E.parse('JMdict_e_examp')
# root = tree.getroot()
# data_dict={}
# for child in root:
#     if child.tag not in data_dict:
#         data_dict[child.tag]=[]
#     dic={}
#     for child2 in child:
#         if child2.tag not in dic:
#             dic[child2.tag]=child2.text
#     data_dict[child.tag].append(dic)
# df = pdx.read_xml("JMdict_e_examp.xml",encoding='utf-8')
# print(df)
# count=0
# for d in df:
#     print (d)
#     count+=1
#     if count > 5:
#         break
json_data = json.dumps(data_dict, indent=2, ensure_ascii=False)
# # json_data = df.to_json()

# # # Write the json data to output
# # # json file
with open("data.json", "w") as json_file:
    json_file.write(json_data)
