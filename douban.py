import csv
import random

import requests
from bs4 import BeautifulSoup
import re

user_agent = [
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]
HEADER = {
    'User-Agent': user_agent[0],  # 浏览器头部
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # 客户端能够接收的内容类型
    'Accept-Language': 'en-US,en;q=0.5',  # 浏览器可接受的语言
    'Connection': 'keep-alive',  # 表示是否需要持久连接
}

def random_HEADER():
    index =  random.randint(0,len(user_agent)-1)
    HEADER = {
        'User-Agent': user_agent[index],  # 浏览器头部
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # 客户端能够接收的内容类型
        'Accept-Language': 'en-US,en;q=0.5',  # 浏览器可接受的语言
        'Connection': 'keep-alive',  # 表示是否需要持久连接
    }
    return HEADER
# 30482003
base_url = "https://movie.douban.com/subject/{}/comments?start={}&limit={}&sort=new_score&status=P"



def getHTMLText(url):
    '''

    :param url: 需要爬取数据的网址
    :return:
    '''
    r = requests.get(url, headers=random_HEADER())
    # print("status_code: ", r.status_code)
    #         r.raise_for_status()
    #         r.encoding = r.apparent_encoding
    r.encoding = "utf-8"
    return r.text, r.status_code


def get_userinfos(soup):
    peoples = soup.findAll(name="a", attrs={"href": re.compile(r"https://www.douban.com/people/(\s\w+)?")})
    for people in peoples:
        url = people.get("href")
        id = people.get("href").split('/')[-2]
        username = people.text
        # user_infos[id] = {"username": username, "url": url}
    return id, username, url

def get_comments(soup):
    comments = soup.findAll(name="span", attrs={"class": "short"})
    for comment in comments:
        _comment = comment.text
        # user_infos[id] = {"username": username, "url": url}
    return _comment

# <span class="allstar10 rating" title="很差"></span>
def get_rating(soup):
    rating = soup.find(name="span", attrs={"class": re.compile(r"allstar(\w+)?")})
    if(rating):
        rate = rating.get('title')
        return rate
    return ''



def parser(html,vedio_info,user_infos):
    '''

    :param html: html文本
    :param vedio_info: 视频信息
    :param user_infos: 用户评论list
    :return:
    '''
    # user_infos = []
    soup = BeautifulSoup(html, 'html.parser')
    comments = soup.findAll(name="div", attrs={"class": "comment"})
    if(len(comments)) < 1:
        return "over"
    # print(comments)
    for comment in comments:
        comment_tag = BeautifulSoup(str(comment),'html.parser')
        id, username, url = get_userinfos(comment_tag)
        _comment = get_comments(comment_tag)
        rate = get_rating(comment_tag)
        # user_infos[id] = {"username": username, "url": url}
        # user_infos.append({"id":id,"username": username, "url": url,"comment":_comment})
        user_infos.append((id, username, url,vedio_info[-1],rate,_comment))
    # return user_infos

def retry(url):
    for i in range(1,6):
        html, code = getHTMLText(url)
        # print("retry: ",code)
        if code == 200:
            return html, code
    return '',403

def spider(vedio_info):
    '''
    :param vedio_info: 视频信息
    :return:
    '''
    index = 0
    user_infos = []
    retry_time = 0
    while (True):
        url = base_url.format(vedio_info[1],index, 20)
        print(url)
        html, code = getHTMLText(url)
        if index == 400:
            print("debug")
        if code == 403:
            html, code = retry(url)
            if code != 200 and retry_time<5:
                print("Retry :", retry_time," code: ",code)
                retry_time += 1
                index += 20
                continue
            else:
                print("Retry over the limit , Over ")
                break
        if parser(html,vedio_info,user_infos) == "over":
            break
        index += 20
    print("get {} infos:".format(len(user_infos)))
    save2csv(user_infos,vedio_info)

def save2csv(list,vedio_info):
    out = open(vedio_info[-1]+".csv","w")
    csv_out = csv.writer(out)
    csv_out.writerow(['uid', 'name','url','movie_name','rating','comment'])
    for row in list:
        csv_out.writerow(row)


# <div class="cover-wp" data-isnew="false" data-id="30166972">
#                 <img src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2572166063.jpg" alt="少年的你" data-x="5906" data-y="8268">
#             </div>

def start():
    '''
    爬取豆瓣电影一周口碑榜的评论以及用户信息
    :return:
    '''
    html,code = getHTMLText("https://movie.douban.com/")
    soup = BeautifulSoup(html, 'html.parser')
    billboards = soup.findAll(name="div", attrs={"id":"billboard"})
    for billboard in billboards:
        # billboard = BeautifulSoup(str(billboard),'html.parser')
        table = billboard.find(name='div',attrs={'class':'billboard-bd'})
        table = BeautifulSoup(str(table),'html.parser')
        tables = table.findAll('table')
        tab = tables[0]
        # print(tab)
        for tr in tab.findAll('tr'):
            video_info = []
            for td in tr.findAll('td'):
                if td.get("class")[0] == "order":
                    video_info.append(td.getText())
                else:
                    a = td.find('a')
                    video_info.append(a.get("href").split('/')[-2])
                    video_info.append(a.text)
            print(video_info)
            spider(video_info)
            video_info.clear()
start()


