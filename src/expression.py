from skip_list import SkipList


class expression:

    def insert(self, element):
        # print(self.top, self.stack.count)
        if self.top == len(self.stack):
            self.stack.append(element)
        else:
            self.stack[self.top] = element
        self.top += 1

    def calculate(self, word: str):
        while self.stack[self.top - 2] == word:
            if self.stack[self.top - 2] == 'and':
                self.stack[self.top - 3] = self.stack[self.top - 3].merge_and(
                    self.stack[self.top - 1])
            else:
                self.stack[self.top - 3] = self.stack[self.top - 3].merge_or(
                    self.stack[self.top - 1])
            self.top -= 2

    def __init__(self, s: str, lookup_table: map,
                 empty_element: SkipList) -> None:
        s = s.split(' ')
        self.stack = []
        self.top = 0
        for word in s:
            if word == '(':
                self.insert('(')
            elif word == ')':
                self.calculate('and')
                self.calculate('or')
                self.stack[self.top - 2] = self.stack[self.top - 1]
                self.top -= 1
            elif word == 'and' or word == 'or':
                if word == 'or':
                    self.calculate('and')
                self.insert(word)
            elif word in lookup_table:
                self.insert(lookup_table[word])
            else:
                self.insert(empty_element)

        self.calculate('and')
        self.calculate('or')

    def get_result(self) -> SkipList:
        return self.stack[0]
