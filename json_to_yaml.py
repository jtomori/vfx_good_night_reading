"""
Converts the previous JSON library into more easily editable and readable YAML format
"""

import json
import yaml

class MyDumper(yaml.Dumper):
    """
    Improves YAML indenting behavior
    src: https://stackoverflow.com/a/39681672
    """
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

def convert():
    """
    Does the actual conversion
    """
    with open('library.json', 'r') as file_data:
        lib_json = json.load(file_data)

    with open('library.yml', 'w') as yaml_file:
        yaml.dump(lib_json, yaml_file, Dumper=MyDumper, default_flow_style=False, indent=4)

if __name__ == "__main__":
    convert()