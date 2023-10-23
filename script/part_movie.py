import jieba
import json
import os

path = os.path.dirname(__file__)

info_path = path + '/../data/Movie_info.json'
part_path = path + '/../data/Movie_part.json'
synonym_path = path + '/../data/dict_synonym.txt'
stop_word_path = path + '/../data/cn_stopwords.txt'

finfo = open(info_path, 'r', encoding='utf-8')
fpart = open(part_path, 'w', encoding='utf-8')
fsynonym = open(synonym_path, 'r', encoding='utf-8')
fstop = open(stop_word_path, 'r', encoding='utf-8')

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

content = json.load(finfo)

for id in content:
    type = content[id]['info']['类型']
    intro = content[id]['intro']
    seg_list =jieba.cut(intro)

    # 合并同义词 && 去除停用词

    seg_list_new = []
    for seg in seg_list:
        if seg in synonym:
            seg_list_new.append(synonym[seg])
        elif seg not in stop_word:
            seg_list_new.append(seg)
    
    # merge seg_list and type
    seg_list_new.extend(type)
    content[id]['part'] = "/".join(seg_list_new)

json.dump(content, fpart, ensure_ascii=False, indent=4)