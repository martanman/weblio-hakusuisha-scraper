import json
import sys

with open("entries.jsonl", "r") as f:
    args = sys.argv[1:]
    if "num" in args:
        print(f.readlines().__len__())
    for x in map(json.loads, f.readlines()):
        for arg in args:
            if arg in x.keys():
                print(x[arg])
        print("----------------------")
