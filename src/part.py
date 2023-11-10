import jieba
import thulac
import json
from config import config


class part:

    def __init__(self, pck: config) -> None:
        self.type = pck.type
        self.part_path = pck.part_path
        self.info_path = pck.info_path
        self.tag_path = pck.tag_path
        self.synonym_path = pck.synonym_path
        self.stop_word_path = pck.stop_word_path
        pass

    def run(self) -> None:
        finfo = open(self.info_path, 'r', encoding='utf-8')
        fpart = open(self.part_path, 'w', encoding='utf-8')
        fsynonym = open(self.synonym_path, 'r', encoding='utf-8')
        fstop = open(self.stop_word_path, 'r', encoding='utf-8')
        ftag = open(self.tag_path, 'r', encoding='utf-8')

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

        cuter = thulac.thulac(seg_only=True)

        for id in content:
            if self.type == "Movie":
                Type = content[id]['info']['类型']
            intro = content[id]['intro']
            seg_list = jieba.cut(intro)
            seg_set = set()
            # 合并同义词 && 去除停用词
            for seg in seg_list:
                if seg in synonym:
                    seg_set.add(synonym[seg])
                elif seg not in stop_word:
                    seg_set.add(seg)

            # seg_list = cuter.cut(intro)
            # for seg in seg_list:
            #     if seg[0] in synonym:
            #         seg_set.add(synonym[seg[0]])
            #     elif seg[0] not in stop_word:
            #         seg_set.add(seg[0])

            # merge seg_set and type
            if self.type == "Movie":
                for t in Type:
                    seg_set.add(t)

            if id in tag_map:
                for tag in tag_map[id]:
                    seg_set.add(tag)

            # output[id] = "/".join(seg_set)
            content[id]['tags'] = '/'.join(seg_set)

        json.dump(content, fpart, ensure_ascii=False, indent=4)
