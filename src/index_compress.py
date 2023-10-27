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
    
    def get_tags(self, id:int) -> list:
        return self.trie[id]['tags'].keys()
    
    def get_content(self, id:int) -> dict:
        return self.trie[id]

class map_block_compress:
    def __init__(self, k:int) -> None:
        self.map = {}
        self.k = k

    def compress(self, content) -> None:
        i = 0
        block = []
        firstid = 0
        for id in content:
            if i == 0:
                firstid = id
            block[i] = content[id]
            if i == self.k-1:
                self.map[firstid] = block
                block = {}
                i = 0

    def bisearch(self, nums:list, val:int) -> int:
        # 返回第一个小于等于val的值
        left = 0
        right = len(nums)-1
        while left <= right:
            mid = (left+right)//2
            if nums[mid] > val:
                right = mid - 1
            else:
                left = mid + 1
        return nums[right]

    def get_tags(self, id:int) -> list:
        block = self.map[self.bisearch(self.map.keys(), id)]
        for x in block:
            if x['id'] == id:
                return x['tags'].split('/')
        print('id not found')
        return None
    
    def get_content(self, id:int) -> dict:
        block = self.map[self.bisearch(self.map.keys(), id)]
        for x in block:
            if x['id'] == id:
                return x
        print('id not found')
        return None