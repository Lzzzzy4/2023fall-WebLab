import random

class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None
    
class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, val):
        if self.head is None:
            self.head = ListNode(val)
            return
        node = ListNode(val)
        cur = self.head
        while cur.next is not None and cur.next.val < val:
            cur = cur.next

        node.next = cur.next
        cur.next = node
    
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

    def insert(self, val):
        for lst in self.lists:
            if random.random() > self.p:
                lst.insert(val)
            else :
                break
    
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