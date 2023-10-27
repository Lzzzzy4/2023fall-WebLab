from pytrie import SortedStringTrie as Trie
class map_frefix_compress:
    def __init__(self) -> None:
        self.trie = Trie()

    def compress(self, content) -> None:
        for id in content:
            self.trie[id] = content[id]
            words_trie = Trie()
            words = content[id]['tags'].split('/')
            cnt = 0
            for word in words:
                words_trie[word] = cnt
                cnt += 1
            self.trie[id]['tags'] = words_trie
    
    def getwords(self) -> list:
        return self.trie.keys()
        
        