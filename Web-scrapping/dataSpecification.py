import json

file_paths = [
    'JsonParts/Species_data1.json', 'JsonParts/Species_data2.json', 'JsonParts/Species_data3.json', 
    'JsonParts/Species_data4.json', 'JsonParts/Species_data5.json'
]


json_global = {}

for fileJ in file_paths:
    with open(fileJ,"r") as file:
        data = json.load(file)
        json_global.update(data)


sections_null = 0
entries = 0
goodIntroduction = 0 #Bigger than 300 chars

#for entry in json_global.values():
#    print(entry.get('introduction'))
#    print("\n")
#    print(len(entry.get('introduction')))
#    break


for entry in json_global.values():
    entries +=1
    if (entry.get('sections') == {}):
        sections_null +=1
    if (len(entry.get('introduction')) > 300):
        goodIntroduction += 1

print(f"Number of entries: {entries}\n")
print(f"Number of entries with null sections: {sections_null}\n")
print(f"Number of entries introductions bigger than 300 chars: {goodIntroduction}\n")



#### Creates a json global file
#with open('json_global.json', "w") as global_file:
#    json.dump(json_global, global_file, indent=4)