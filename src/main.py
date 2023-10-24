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
    print("输入bool查询语句:")
    i.query()

if __name__ == '__main__':
    # part_run('Movie')
    # index_run('Movie')
    # part_run('Book')
    index_run('Book')   


