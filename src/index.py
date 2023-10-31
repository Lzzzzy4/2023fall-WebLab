import json
import math
from skip_list import SkipList
from expression import expression
from index_compress import map_frefix_compress, map_block_compress
from config import config

class index:
    def __init__(self, pck:config, type:str) -> None:
        self.type = type
        self.part_path = pck.part_path
        self.synonym_path = pck.synonym_path
        self.compress_method = pck.compress_method
        pass

    def run(self) -> None:

        fpart = open(self.part_path, 'r', encoding='utf-8')
        fsynonym = open(self.synonym_path, 'r', encoding='utf-8')

        synonym = {}
        for line in fsynonym:
            line = line.strip()
            if line == '':
                continue
            words = line.split(' ')
            for word in words[2:]:
                synonym[word] = words[1]

        self.content = json.load(fpart)
        if self.compress_method == "prefix":
            map = map_frefix_compress()
            self.content = map.compress(self.content)
        elif self.compress_method == "block":
            map = map_block_compress(5)
            self.content = map.compress(self.content)

        self.lookup_table = {}

        self.level = int(math.ceil(math.log2(len(self.content))))

        for id in self.content:
            words = self.content[id]['tags'].split('/')
            for word in words:
                if word in synonym:
                    word = synonym[word]
                if word not in self.lookup_table:
                    self.lookup_table[word] = SkipList(self.level)
                self.lookup_table[word].insert(id)

    def query(self) -> None:
        result = expression(input(), self.lookup_table, SkipList(self.level)).get_result()

        for i in result.get_all():
            if self.type == 'Movie':
                print(i, self.content[i]['name'], self.content[i]['info']['类型'])
            else :
                print(i, self.content[i]['name'])