import json
import math
import time
from skip_list import SkipList
from expression import expression
from index_compress import map_frefix_compress, map_block_compress
from config import config


class index:

    def __init__(self, pck: config) -> None:
        self.type = pck.type
        self.part_path = pck.part_path
        self.synonym_path = pck.synonym_path
        self.compress_method = pck.compress_method
        pass

    def run(self) -> None:
        start = time.time()

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
            map.compress(self.content)
            self.content = map
        elif self.compress_method == "block":
            map = map_block_compress(5)
            map.compress(self.content)
            self.content = map

        self.lookup_table = {}

        self.level = int(math.ceil(math.log2(len(self.content))))

        for id in self.content.keys():
            words = self.get_tags(id)
            for word in words:
                if word in synonym:
                    word = synonym[word]
                if word not in self.lookup_table:
                    self.lookup_table[word] = SkipList(self.level)
                self.lookup_table[word].insert(id)

        end = time.time()
        print('totally run time is ', end - start)

    def query(self) -> None:
        print("input Boolean Retrieval")
        word = input()
        start = time.time()
        result = expression(word, self.lookup_table,
                            SkipList(self.level)).get_result()

        for i in result.get_all():
            if self.type == 'Movie':
                print(i, self.content[i]['name'],
                      self.content[i]['info']['类型'])
            else:
                print(i, self.content[i]['name'])

        end = time.time()
        print('totally query time is ', end - start)


    def get_tags(self, id) -> dict:
        if self.compress_method == "prefix" or self.compress_method == "block":
            return self.content.get_tags(id)
        else:
            return self.content[id]['tags'].split('/')
