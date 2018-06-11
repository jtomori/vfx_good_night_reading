"""
This script is used to generate README.md based on library.json

Please do not edit directly README.md, but modify entries in library.json and then re-generate README.md by running `$ python generate.py`
"""

import json

page = ""
page_intro = """
# VFX Good Night Reading

Curated collection of good reading about VFX and CG. Mostly TD-level stuff, but not too hardcore.

Links are pointing to PDFs when available for free, or to [acm digital library](https://dl.acm.org/) if not. You can also find papers at [deepdyve](https://www.deepdyve.com/), where you can check free preview before buying them.

Feel free to improve/extend this library and contribute with your findings. Pull requests are welcome.

See [generate.py](./generate.py) for instructions about generating this page.

[![Total entries](https://img.shields.io/badge/total_entries-{total_entries}-green.svg?longCache=true&style=for-the-badge)](#list) [![GitHub stars](https://img.shields.io/github/stars/jtomori/vfx_good_night_reading.svg?style=for-the-badge&label=Stars)](https://github.com/jtomori/vfx_good_night_reading/stargazers)
"""

tags_links = {
    "spi":          "http://library.imageworks.com/",
    "mpc":          "http://www.moving-picture.com/film/content-pages/technology/",
    "dwa":          "http://research.dreamworks.com/",
    "scad":         "http://ecollections.scad.edu/iii/cpro/CollectionViewPage.external?lang=eng&sp=1000005&suite=def",
    "pixar":        "https://graphics.pixar.com/library/",
    "disney":       "https://www.disneyresearch.com/publication/",
    "tdforum":      "http://tdforum.eu/pdf/",
    "clemson":      "https://tigerprints.clemson.edu/theses/",
    "bournemouth":  "https://nccastaff.bournemouth.ac.uk/jmacey/MastersProjects/"
}

with open('library.json', 'r') as file_data:
    lib_json = json.load(file_data)

page_intro = page_intro.format( total_entries=len( lib_json.keys() ) )

# analyze library, create a dict holding entries organized by categories
formats_set = set()
tags_set = set()
categories_set = set()
categories_dict = {}
tags_counter = {}
format_counter = {}

for title, entry in lib_json.iteritems():
    formats_set = formats_set | set([ entry["format"] ])
    tags_set = tags_set | set( entry["tags"] ) if entry["tags"] != [] else tags_set

    for cat in entry["categories"]:
        categories_set = categories_set | set( [cat] )

        if cat not in categories_dict.keys():
            categories_dict[cat] = { title : entry }
        else:
            categories_dict[cat][title] = entry
    
    for tag in entry["tags"]:
        if tag not in tags_counter.keys():
            tags_counter[tag] = 1
        else:
            tags_counter[tag] = tags_counter[tag] + 1
    
    if entry["format"] not in format_counter.keys():
        format_counter[ entry["format"] ] = 1
    else:
        format_counter[ entry["format"] ] = format_counter[ entry["format"] ] + 1

formats_list = list(formats_set)
formats_list.sort()
tags_list = list(tags_set)
tags_list.sort()
tags_list = tags_list
categories_list = list(categories_set)
categories_list.sort()

#print json.dumps(categories_dict, indent=2)

# generate formats section
page_format = "### Formats\n"

for fmt in formats_list:
    page_format = page_format + "* **{}** ({})\n".format(fmt, format_counter[fmt])

# generate tags section
page_tags = "### Tags\n"

for tag in tags_list:
    tag_orig = tag
    if tag in tags_links:
        tag = "[{}]({})".format(tag, tags_links[tag])
    page_tags = page_tags + "* {} ({})\n".format(tag, tags_counter[tag_orig])

# generate categories section
def filter_links(char):
    return char.isalpha() or char.isspace()

page_categories = "### Categories\n"
for cat in categories_list:
    link = str(cat.lower())
    link = ''.join(filter(filter_links, link))
    link = link.replace(" ", "-")
    
    page_categories = page_categories + "* [{}](#{}) ({})\n".format(cat, link, len( categories_dict[cat].keys() ) )

# generate entries section
page_entries = "## List\n<br>\n"

for cat, entries in sorted(categories_dict.iteritems()):
    page_entries = page_entries + "\n\n### {}".format(cat)

    for title, data in sorted(entries.iteritems()):
        tags = data["tags"]
        tags.sort()
        tags_str = ""
        for tag in tags:
            tags_str = tags_str + " `{}`".format(tag)
        
        if data.has_key("extra"):
            tags_str = tags_str + " " + data["extra"]

        entry = "\n* [{}]({}) **{}**{}".format( title.encode('utf-8'), data["link"], data["format"], tags_str )
        page_entries = page_entries + entry

page = "\n<br>\n\n".join( [page_intro, page_format, page_tags, page_categories, page_entries] )
page = page + "\n"

with open("README.md", "w") as out_file:
    out_file.write(page) 