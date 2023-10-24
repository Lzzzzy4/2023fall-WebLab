from index import index
from path import pathpck
from part import part
def part_run(word:str) -> None:
    pck = pathpck(word)
    p = part(pck, word)
    p.run()

def index_run(word:str) -> None:
    pck = pathpck(word)
    i = index(pck, word)
    i.run()
    print("input Boolean Retrieval")
    i.query()

if __name__ == '__main__':
    print("input 'Book' or 'Movie':")
    index_run(input())   


