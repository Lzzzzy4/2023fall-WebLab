import jieba
import json
import os

path = os.path.dirname(__file__)

info_path = path + '/../data/Movie_info.json'
part_path = path + '/../data/Movie_part.json'
synonym_path = path + '/../data/dict_synonym.txt'
stop_word_path = path + '/../data/cn_stopwords.txt'
tag_path = path + '/../data/Movie_tag.csv'

finfo = open(info_path, 'r', encoding='utf-8')
fpart = open(part_path, 'w', encoding='utf-8')
fsynonym = open(synonym_path, 'r', encoding='utf-8')
fstop = open(stop_word_path, 'r', encoding='utf-8')
ftag = open(tag_path, 'r', encoding='utf-8')

synonym = {}
for line in fsynonym:
    line = line.strip()
    if line == '':
        continue
    words = line.split(' ')
    for word in words[2:]:
        synonym[word] = words[1]

stop_word = set()
for line in fstop:
    line = line.strip()
    if line == '':
        continue
    stop_word.add(line)

tag_map = {}
for line in ftag.readlines()[1:]:
    line = line.strip()
    if line == '':
        continue
    words = line.split(',')
    id = words[0]
    tag = words[1:]

    if len(tag[0]) == 0:
        continue

    for i in range(len(tag)):
        if tag[i][0] == '\"':
            tag[i] = tag[i][1:]
        if tag[i][-1] == '\"':
            tag[i] = tag[i][:-1]

    tag_map[id] = tag

content = json.load(finfo)
output = {}
total_tag = set()

for id in content:
    Type = content[id]['info']['类型']
    intro = content[id]['intro']
    seg_list =jieba.cut(intro)

    # 合并同义词 && 去除停用词

    seg_set = set()
    for seg in seg_list:
        if seg in synonym:
            seg_set.add(synonym[seg])
        elif seg not in stop_word:
            seg_set.add(seg)
    
    # merge seg_set and type
    for t in Type:
        seg_set.add(t)

    if id in tag_map:
        for tag in tag_map[id]:
            seg_set.add(tag)

    output[id] = "/".join(seg_set)

    for seg in seg_set:
        total_tag.add(seg)

json.dump(output, fpart, ensure_ascii=False, indent=4)
print("There are %d tags in total." % len(total_tag))