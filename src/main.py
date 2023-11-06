from index import index
from config import config
from part import part


def part_run(word: str) -> None:
    pck = config(word)
    p = part(pck)
    p.run()


def index_run(word: str) -> None:
    pck = config(word, "block")
    i = index(pck)
    i.run()
    print("input Boolean Retrieval")
    i.query()


if __name__ == '__main__':
    print("input 'Book' or 'Movie':")
    index_run(input())
