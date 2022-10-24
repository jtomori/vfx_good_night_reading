"""This script is used to generate README.md based on ``library.yml``.

Please do not edit directly ``README.md``, but modify entries in ``library.yml`` instead and then re-generate ``README.md`` by running ``$ python generate.py``. See bottom of ``README.md`` for more info.
"""

import re
import yaml
import textwrap


def main():
    """Script's entry point. This function does all of the work."""
    page_intro = """
    # VFX Good Night Reading

    Curated collection of good reading about VFX and CG. Mostly TD-level stuff, but not too hardcore.

    Links are pointing to PDFs when available for free, or to [acm digital library](https://dl.acm.org/). Note that ACM Digital Library content is sometimes available for **free**, more info [here](https://www.siggraph.org/learn/conference-content).

    :information_source: Note that some links might break after some time. You can still check if they are indexed in [Wayback Machine](https://archive.org/web/) though.

    :information_source: Bournemouth links are mostly dead. You should be able to find the content here though: [new website](https://nccastaff.bournemouth.ac.uk/jmacey/MastersProject/).

    Feel free to improve/extend this library and contribute with your findings. Pull requests are welcome.

    See [here](#adding-new-entries) for instructions about generating this page.

    Number of entries: {total_entries}, categories: {total_categories}
    """

    tags_links = {
        "spi": "http://library.imageworks.com/",
        "mpc": "http://www.moving-picture.com/film/content-pages/technology/",
        "dwa": "http://research.dreamworks.com/",
        "weta": "https://www.wetafx.co.nz/research-and-tech/publications/",
        "scad": "http://ecollections.scad.edu/iii/cpro/CollectionViewPage.external?lang=eng&sp=1000005&suite=def",
        "pixar": "https://graphics.pixar.com/library/",
        "disney": "https://studios.disneyresearch.com/",
        "tdforum": "http://tdforum.eu/pdf/",
        "clemson": "https://tigerprints.clemson.edu/theses/",
        "bournemouth": "https://nccastaff.bournemouth.ac.uk/jmacey/MastersProject/"
    }

    with open("library.yml", "r", encoding="utf-8") as file_data:
        lib_json = yaml.safe_load(file_data)

    # analyze library, create a dict holding entries organized by categories
    formats_set = set()
    tags_set = set()
    categories_set = set()
    categories_dict = {}
    tags_counter = {}
    format_counter = {}

    for title, entry in lib_json.items():
        formats_set = formats_set | set([entry["format"]])
        tags_set = tags_set | set(entry["tags"]) if entry["tags"] != [] else tags_set

        for cat in entry["categories"]:
            categories_set = categories_set | set([cat])

            if cat not in categories_dict:
                categories_dict[cat] = {title: entry}
            else:
                categories_dict[cat][title] = entry

        for tag in entry["tags"]:
            if tag not in tags_counter:
                tags_counter[tag] = 1
            else:
                tags_counter[tag] = tags_counter[tag] + 1

        if entry["format"] not in format_counter:
            format_counter[entry["format"]] = 1
        else:
            format_counter[entry["format"]] = format_counter[entry["format"]] + 1

    formats_list = list(formats_set)
    formats_list.sort()
    tags_list = list(tags_set)
    tags_list.sort()
    categories_list = list(categories_set)
    categories_list.sort()

    page_intro = textwrap.dedent(page_intro).format(total_entries=len(lib_json.keys()), total_categories=len(categories_list))

    # generate formats section
    page_format = "### Formats\n"

    for fmt in formats_list:
        page_format = page_format + f"* **{fmt}** ({format_counter[fmt]})\n"

    # generate tags section
    page_tags = "### Tags\n"

    for tag in tags_list:
        tag_orig = tag
        if tag in tags_links:
            tag = f"[{tag}]({tags_links[tag]})"
        page_tags = page_tags + f"* {tag} ({tags_counter[tag_orig]})\n"

    # generate categories section
    def filter_links(char):
        return char.isalpha() or char.isspace()

    page_categories = "### Categories\n"
    for cat in categories_list:
        link = str(cat.lower())
        link = ''.join(filter(filter_links, link))
        link = link.replace(" ", "-")

        page_categories = page_categories + f"* [{cat}](#{link}) ({len(categories_dict[cat].keys())})\n"

    # generate entries section
    page_entries = "# List\n<br>\n"

    for cat, entries in sorted(categories_dict.items()):
        page_entries = page_entries + f"\n\n### {cat}"

        for title, data in sorted(entries.items()):
            tags = data["tags"]
            tags.sort()
            tags_str = ""
            for tag in tags:
                tags_str = tags_str + f" `{tag}`"

            if "extra" in data:
                tags_str = tags_str + " " + data["extra"]

            entry = f'\n* [{title}]({data["link"]}) **{data["format"]}**{tags_str}'
            page_entries = page_entries + entry

    page_entries += "\n"

    page_contributing = """\
    ### Contributing
    Feel free to contribute to this project by creating pull requests.

    <br>

    ### Adding new entries
    * Create virtual environment
        ```
        $ python3 -m venv venv
        ```

    * Activate it
        ```
        $ source venv/bin/activate
        ```

    * Install dependencies
        ```
        $ pip install -r requirements.txt
        ```

    * Edit `library.yml` to add new entries

    * Run code quality checks and re-generate `README.md`
        ```
        $ make
        ```

        * You can run code checks only with
            ```
            $ make check
            ```

        * Or re-generate `README.md` only with
            ```
            $ make generate
            ```

        * Alternatively re-generate `README.md` without make
            ```
            $ python generate.py
            ```

    * Done!
    """
    page = "\n<br>\n\n".join([page_intro, page_format, page_tags, page_categories, page_entries, textwrap.dedent(page_contributing)])
    page = page + "\n"

    # Render into markdown
    with open("README.md", "w", encoding="utf-8") as out_file:
        out_file.write(page)

    html_header = """\
    <meta charset="utf-8" lang="en">
    <link href="styles.css" rel="stylesheet">
    """

    html_footer = """\
    <!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible");window.markdeepOptions = {tocStyle: 'none'};</script>
    """

    replaced_page = page.replace(
        "# VFX Good Night Reading", "**VFX Good Night Reading**"
    ).replace(
        "<br>", ""
    ).replace(
        ":information_source:", "!!!\n   "
    ).replace(
        "adding-new-entries", "addingnewentries"
    )

    # Fix ampersant in categories links
    pattern1 = re.compile(
        r'(\* \[.*\]\(#.*)(--)(.*\))',
    )
    replaced_page = pattern1.sub(r'\1&\3', replaced_page)

    # Fix space in categories links
    pattern2 = re.compile(
        r'(\* \[.*\]\(#.*)(-)(.*\))',
    )
    replaced_page = pattern2.sub(r'\1\3', replaced_page)

    html_page = textwrap.dedent(html_header) + replaced_page + textwrap.dedent(html_footer)

    # Render into html
    with open("index.html", "w", encoding="utf-8") as out_file:
        out_file.write(html_page)

    print("Generation finished!")


if __name__ == "__main__":
    main()
