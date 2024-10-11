import json

file_paths = [
    'JsonParts/Species_data1.json', 'JsonParts/Species_data2.json', 'JsonParts/Species_data3.json', 
    'JsonParts/Species_data4.json', 'JsonParts/Species_data5.json', 'JsonParts/Species_data6.json',
    'JsonParts/Species_data7.json', 'JsonParts/Species_data8.json'
]


json_global = {}

for fileJ in file_paths:
    with open(fileJ,"r") as file:
        data = json.load(file)
        json_global.update(data)


sections_null = 0
entries = 0
goodIntroduction = 0 #Bigger than 300 chars
onlySmallIntro = 0
totalIntroChar = 0
totalIntroCharNull = 0
totalIntroCharNotNull = 0
sections_notNull = 0
taxonavigation_null = 0
seen_introductions = set()
duplicate_keys = [] 

for entry in json_global.values():
    entries +=1
    totalIntroChar += len(entry.get('introduction'))

    if (entry.get('sections') == {}):
        sections_null +=1
        totalIntroCharNull += len(entry.get('introduction'))

    if(entry.get('sections') != {}):
        sections_notNull += 1
        totalIntroCharNotNull += len(entry.get('introduction'))

    if (len(entry.get('introduction')) > 300):
        goodIntroduction += 1

    if ((entry.get('sections') == {}) &(len(entry.get('introduction')) < 100)):
        onlySmallIntro += 1

    if((entry.get('scientific_classification') == {})): # DROP THESE VALUES, Miliarium example 
        taxonavigation_null += 1


for key, entry in json_global.items():
    intro = entry.get('introduction')
    if intro in seen_introductions:
        duplicate_keys.append(key)
    else:
        seen_introductions.add(intro)

keys = [key for key, entry in json_global.items() if (((entry.get('sections') == {}) and (len(entry.get('introduction')) < 100))
        or (entry.get('scientific_classification') == {}))]
 
for key in keys:
    del json_global[key]

print(f"Number of entries that are duplicated: {len(duplicate_keys)}\n") 
print(f"Number of entries to be removed: {len(keys)}\n")
print(f"Number of entries: {entries}\n")
print(f"Number of entries with null sections: {sections_null}\n")
print(f"Number of entries introductions bigger than 300 chars: {goodIntroduction}\n")
print(f"Number of entries with null sections and small introductions: {onlySmallIntro}\n")
print(f"Average char length in the introduction: {round(totalIntroChar/entries,2)}\n")
print(f"Number of entries with null taxonavigation: {taxonavigation_null}\n")
print(f"Average char length in the introduction when sections are null: {round(totalIntroCharNull/sections_null,2)}\n")
print(f"Average char length in the introduction when sections are not null: {round(totalIntroCharNotNull/sections_notNull,2)}\n")



#### Creates a json global file
#with open('json_global.json', "w") as global_file:
#    json.dump(json_global, global_file, indent=4)