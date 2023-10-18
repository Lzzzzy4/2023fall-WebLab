import requests
from bs4 import BeautifulSoup
import json
import os
import time

def get_html(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Host': 'movie.douban.com',
        'referer': 'https://movie.douban.com/explore',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }

    try:
        response = requests.get(url, headers = headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(e)
        return ""
    
def get_info(soup):
    info = soup.find('div', id = 'info')
    info = info.get_text().strip('\n').split('\n')
    info = [i.split(': ') for i in info]
    info_dict = {}
    for i in info:
        #check for i[i] exsit  盗梦空间bug
        if(len(i) == 1):
            continue
        info_dict[i[0]] = i[1].split(' / ')
        if(len(info_dict[i[0]]) == 1):
            info_dict[i[0]] = info_dict[i[0]][0]
    return info_dict

def get_rating(soup):
    rating = soup.find('div', class_ = 'rating_wrap clearbox')
    if rating == None:
        return None
    rating_dict = {}
    rating_dict['评分'] = rating.find('strong', class_ = 'll rating_num').get_text()
    rating_dict['评分人数'] = rating.find('a', class_ = 'rating_people').find('span').get_text()
    star = 5
    for i in rating.find('div', class_ = 'ratings-on-weight').find_all('div', class_ = 'item'):
        rating_dict[str(star) + '星'] = i.find('span', class_ = 'rating_per').get_text()
        star -= 1
    return rating_dict

def get_celebrities(url):
    html = get_html(url + 'celebrities')
    soup = BeautifulSoup(html, 'html.parser')
    celebrities_dict = {}
    for i in soup.find_all('div', class_ = 'list-wrapper'):
        celebrities_list = []
        for j in i.find_all('span', class_ = 'name'):
            celebrities_list.append(j.find('a').get_text())
        celebrities_dict[i.find('h2').get_text()] = celebrities_list
    return celebrities_dict

def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('span', property = 'v:itemreviewed').get_text()
    year = soup.find('span', class_ = 'year').get_text().strip('()')
    info = get_info(soup)
    rating = get_rating(soup)
    if soup.find('span', property = 'v:summary') != None:
        intro = "".join(soup.find('span', property = 'v:summary').get_text().split())
    else:
        intro = "".join(soup.find('span', class_ = "all hidden").get_text().split())
    celebrities  = get_celebrities(url)

    content = {}
    content['name'] = name
    content['year'] = year
    content['info'] = info
    content['rating'] = rating
    content['intro'] = intro
    content['celebrities'] = celebrities

    return content

if __name__ == '__main__':
    #获取当前文件路径
    path = os.path.dirname(__file__)
    id_path = path + "/../data/Movie_id.csv"
    info_path = path + "/../data/Movie_info.json"
    error_path = path + "/../data/error_id.txt"
    fread = open(id_path, "r")

    #check if file movie_info.json exisit
    try:
        fcomplete = open(info_path, "r",encoding='utf-8')
        id_map = json.load(fcomplete)
        fcomplete.close()
    except :
        id_map= {}
    
    try:
        with open(error_path, "r") as ferror:
            skip_set = set(ferror.read().splitlines())
    except:
        skip_set = set()


    for line in fread.readlines():
        id = line.strip('\n')

        #防止重爬 && 跳过下架电影的id
        if id in id_map or id in skip_set:
            continue

        print(id)

        url = 'https://movie.douban.com/subject/'+id+'/'
        try:
            content = get_content(url)
            id_map[id] = content
        except:
            with open(error_path, "a+") as ferror:
                ferror.write(id+"\n")


    
    with open(info_path, "w+", encoding='utf-8') as fwrite:
        fwrite.write(json.dumps(id_map, indent = 4, ensure_ascii = False)+"\n")

    fread.close()
    