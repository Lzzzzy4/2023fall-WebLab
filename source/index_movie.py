import os
import json
import math
from skip_list import SkipList
from expression import expression

path = os.path.dirname(__file__)
part_path = path + '/../data/Movie_part.json'
synonym_path = path + '/../data/dict_synonym.txt'

fpart = open(part_path, 'r', encoding='utf-8')
fsynonym = open(synonym_path, 'r', encoding='utf-8')

synonym = {}
for line in fsynonym:
    line = line.strip()
    if line == '':
        continue
    words = line.split(' ')
    for word in words[2:]:
        synonym[word] = words[1]

content = json.load(fpart)

lookup_table = {}

level = int(math.ceil(math.log2(len(content))))

for id in content:
    words = content[id]['tags'].split('/')
    for word in words:
        if word not in lookup_table:
            lookup_table[word] = SkipList(level)
        lookup_table[word].insert(id)

result = expression(input(), lookup_table, SkipList(level)).get_result()

for i in result.get_all():
    print(i, content[i]['name'], content[i]['info']['类型'])