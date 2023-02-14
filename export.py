# format is: [ [ "鼻まじろき", "はなまじろき", "", "", 0, [ "description" ], 47942, "" ] ]
import json
import pathlib
import re
import os

with open("entries.jsonl", "r") as f:
    entries = map(json.loads, f.readlines())

terms = []
for i, e in enumerate(entries):
    m = re.match("ピンイン(.*)", e["text"])
    assert m != None
    pinyin = re.sub("・| ", "", m.group(1))
    if "⇒" in pinyin:
        pinyin = pinyin[:pinyin.index("⇒")]

    text = e['midashigo'] +  re.sub("ピンイン", " ", e["text"], count=1)
    terms.append([e["title"], pinyin, "", "", 0, [text], i, ""])

pathlib.Path("term_bank_1.json").write_text(json.dumps(terms))
os.popen("zip hakusuisha.zip index.json term_bank_1.json ; rm term_bank_1.json").read()
