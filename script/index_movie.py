import os
import json
import math
from skip_list import SkipList

path = os.path.dirname(__file__)

part_path = path + '/../data/Movie_part.json'

fpart = open(part_path, 'r', encoding='utf-8')

content = json.load(fpart)

lookup_table = {}

level = int(math.ceil(math.log2(len(content))))

for id in content:
    words = content[id].split('/')
    for word in words:
        if word not in lookup_table:
            lookup_table[word] = SkipList(level)
        lookup_table[word].insert(id)
    break