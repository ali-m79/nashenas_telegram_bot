import json


def read_json(json_file):
    with open(json_file) as f:
        return json.load(f)


def write_json(data, json_file, ident=4):
    with open(json_file, "w") as f:
        json.dump(data, f)
