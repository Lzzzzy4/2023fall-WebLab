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

class SkipList:
    def __init__(self, level) -> None:
        self.level = level
        self.lists = [LinkedList() for i in range(level)]
        self.p = 0.5

    def insert(self, val):
        for llist in self.lists:
            if random.random() > self.p:
                llist.insert(val)
            else :
                break