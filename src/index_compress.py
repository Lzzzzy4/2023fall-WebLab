from pytrie import SortedStringTrie as Trie
class map_frefix_compress:
    def __init__(self) -> None:
        self.trie = Trie()

    def compress(self, content) -> None:
        self.len = len(content)
        for id in content:
            self.trie[str(id)] = content[id]
            words_trie = Trie()
            words = content[id]['tags'].split('/')
            cnt = 0
            for word in words:
                words_trie[word] = cnt
                cnt += 1
            self.trie[id]['tags'] = words_trie
    
    def get_tags(self, id:int) -> list:
        return self.trie[str(id)]['tags'].keys()
    
    def keys(self) ->list:
        return self.trie.keys()

    def __len__(self) -> int:
        return self.len
    
    def __getitem__(self, id:int) -> dict:
        return self.trie[str(id)]

class map_block_compress:
    def __init__(self, k:int) -> None:
        self.map = {}
        self.k = k
        self.idlist = []

    def compress(self, content) -> None:
        self.len = len(content)
        i = 0
        block = []
        firstid = 0
        for id in sorted(content.keys()):
            self.idlist.append(id)
            if i == 0:
                firstid = id
            content[id]['id'] = id
            block.append(content[id])
            if i == self.k-1:
                self.map[firstid] = block
                block = []
                i = 0
            else:
                i += 1
        if i != 0:
            self.map[firstid] = block

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
        return self[id]['tags'].split('/')
    
    def __getitem__(self, id:int) -> dict:
        block = self.map[self.bisearch(list(self.map.keys()), id)]
        if id == 5385852:
            print(block)
        for x in block:
            if x['id'] == id:
                return x
        print(id,'id not found')
        return None
    
    def keys(self) -> list:
        return self.idlist
    
    def __len__(self) -> int:
        return self.len