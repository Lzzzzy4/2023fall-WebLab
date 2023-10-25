import random

class ListNode:
    def __init__(self, val, next = None, down = None):
        self.val = val
        self.next = next
        self.down = down 
class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, val, cur = None):
        if self.head is None:
            node = ListNode(val)
            self.head = node
            return (None, node)

        if cur == None:
            cur = self.head

        while cur.next is not None and cur.next.val < val:
            cur = cur.next

        node = ListNode(val, cur.next)
        cur.next = node
        return (cur, node)

    def merge_and(self, lst):
        i = self.head
        j = lst.head
        new_lst = LinkedList()
        while i != None and j != None:
            if i.val == j.val:
                new_lst.insert(i.val)
                i = i.next
                j = j.next
            elif i.val < j.val:
                i = i.next
            else:
                j = j.next
        return new_lst
    
    def merge_or(self, lst):
        i = self.head
        j = lst.head
        new_lst = LinkedList()
        while i != None and j != None:
            if i.val == j.val:
                new_lst.insert(i.val)
                i = i.next
                j = j.next
            elif i.val < j.val:
                new_lst.insert(i.val)
                i = i.next
            else:
                new_lst.insert(j.val)
                j = j.next

        while i != None:
            new_lst.insert(i.val)
            i = i.next
        while j != None:
            new_lst.insert(j.val)
            j = j.next
        return new_lst
    
    def gel_all(self):
        i = self.head
        while i != None:
            yield i.val
            i = i.next


class SkipList:
    def __init__(self, level) -> None:
        self.level = level
        self.lists = [LinkedList() for i in range(level)]
        self.p = 0.5

    def rand_level(self):
        level = 0
        while random.random() < self.p and level + 1 < self.level:
            level += 1
        return level

    def insert(self, val):
        rlevel = self.rand_level()
        pre = None
        cur = None
        for i in range(rlevel, -1, -1):
            (nxtpre, nxtcur) = self.lists[i].insert(val, pre)
            if cur != None:
                cur.down = nxtcur

            if nxtpre != None:
                nxtpre = nxtpre.down
            
            (pre, cur) = (nxtpre, nxtcur)
    
    #merge with and method
    def merge_and(self, lst):
        new_lst = SkipList(self.level)
        for i in range(self.level):
            new_lst.lists[i] = self.lists[i].merge_and(lst.lists[i])
        return new_lst

    def merge_or(self, lst):
        new_lst = SkipList(self.level)
        for i in range(self.level):
            new_lst.lists[i] = self.lists[i].merge_or(lst.lists[i])
        return new_lst
    
    def get_all(self):
        return self.lists[0].gel_all()