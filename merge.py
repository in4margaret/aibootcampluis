import json
import glob

files = glob.glob("generated_json_files_for_intent/*.json")
utterances = []
for file in files:
    with open(file) as f:
        json_file = json.load(f)
        for entry in json_file:
            for entity in entry['entities']:
                if entity['entity'] == 'datetimeV2'or entity['entity'] == 'days'or entity['entity'] == 'time':
                    entity['entity'] = 'builtin.datetimeV2.datetime'
                if entity['entity'] == 'number':
                    entity['entity'] == 'builtin.number'
        utterances.extend(json_file)

with open(r"./model/merged.json", 'w') as json_file:
    json.dump(utterances, json_file, indent=2)
