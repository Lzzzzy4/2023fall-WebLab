import os

path = os.path.dirname(__file__)


class config:

    def __init__(self, word: str, method="none") -> None:
        self.type = word
        self.part_path = path + '/../data/' + word + '_part.json'
        self.info_path = path + '/../data/' + word + '_info.json'
        self.tag_path = path + '/../data/' + word + '_tag.csv'
        self.synonym_path = path + '/../data/dict_synonym.txt'
        self.stop_word_path = path + '/../data/cn_stopwords.txt'
        self.compress_method = method
        pass
