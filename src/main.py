from index import index
from config import config
from part import part
import os
import psutil


def part_run(word: str) -> None:
    pck = config(word)
    p = part(pck)
    p.run()


def index_run(word: str) -> None:
    pck = config(word, "none")
    i = index(pck)
    i.run()
    i.query()

def get_mem() -> int:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss/1024

if __name__ == '__main__':
    start = get_mem()
    print("input 'Book' or 'Movie':")
    index_run(input())
    end = get_mem()
    print("memory usage: ", end - start, "KB")
