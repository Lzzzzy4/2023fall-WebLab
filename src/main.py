from index import index
from config import config
from part import part
def part_run(word:str) -> None:
    pck = config(word)
    p = part(pck, word)
    p.run()

def index_run(word:str) -> None:
    pck = config(word, "prefix")
    i = index(pck, word)
    i.run()
    print("input Boolean Retrieval")
    i.query()

if __name__ == '__main__':
    print("input 'Book' or 'Movie':")
    index_run(input())   


