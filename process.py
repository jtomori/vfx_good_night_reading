"""
This script was used for conversion of my initial approach (writing everything by hand) into more programmable one.

This script should not be needed after one-time conversion.
"""

import re
import json


with open('initial_entries', 'r') as f:
    file_data = f.read()

file_data_categories = file_data.split("### ")[1:]

input_entries = 0

cat_dict = {}
for cat in file_data_categories:
    cat = cat.split("\n")
    cat_dict[ cat[0] ] = cat[1:-1]
    input_entries = input_entries + len(cat[1:-1])

#print json.dumps(cat_dict, indent=4, sort_keys=True)

dict_lib = {}

unique_counter = 0
duplicate_counter = 0

for cat, entries in cat_dict.iteritems():
    for line in entries:
        parts = re.split('\[|\]\(|\) \[|\] \[|\]', line)[1:-1]

        title = parts[0]

        dict_entry = {}
        dict_entry["link"] = parts[1]
        dict_entry["format"] = parts[2]
        dict_entry["tags"] = parts[3:]
        dict_entry["categories"] = [cat]

        if title not in dict_lib:
            dict_lib[ title ] = dict_entry
            unique_counter = unique_counter + 1
        else:
            duplicate_counter = duplicate_counter + 1
            if dict_lib[title]["tags"] != dict_entry["tags"]:
                print "\ncorrupted duplicates found:"
                print title
                print dict_lib[title]
                print dict_entry
            dict_lib[title]["categories"].append(cat)

print "number of input file categories: {}".format( len(file_data_categories) )
print "number of input entries (with duplicates): {}".format( input_entries )
print "number of output unique entries: {}".format( len(dict_lib.keys()) )
print "unique_counter = {}, duplicate_counter = {}, sum = {}".format(unique_counter, duplicate_counter, unique_counter + duplicate_counter)

with open('library.json', 'w') as out_file:
    json.dump(dict_lib, out_file, indent=4, sort_keys=True, ensure_ascii=False)