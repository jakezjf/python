#-*_coding:utf8-*-
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class DouBan(object):
    def __init__(self):
        print u'开始爬取内容。。。'

    def getsource(self,url):
        html = requests.get(url)
        return html.text

    def changepage(self, url, total_page):
        now_page = int(re.search('start=(\d+)', url, re.S).group(1))
        page_group = []
        count = 0
        for i in range(now_page, total_page):
            count = count + 50
            link = re.sub('start=\d+', 'start=%s'%count, url, re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self, source):
        everyclass = re.findall('">.*?</dd>', source, re.S)
        return everyclass

    def getinfo(self, eachhouse):
        info = {}
        info['url'] = re.search(r'<a href="(.*?)"', eachhouse, re.S).group(1)
        info['title'] = re.search(r'title="(.*?)" class', eachhouse, re.S).group(1)
        return info

    def saveinfo(self, classinfo):
        f = open('3.txt', 'a')
        for each in classinfo:
            f.writelines(each['url'] + '\n')
            f.writelines(each['title'] + '\n' + '\n')
        f.close()

    def find_text(self, source):
        everyhose = re.findall('<td class="title">(.*?)</td>', source, re.S)
        return everyhose

if __name__ == '__main__':

    pages = []
    file = []
    url = 'https://www.douban.com/group/zhufang/discussion?start=0'
    dou = DouBan()
    pages = dou.changepage(url, 300)
    for page in pages:
        print ("正在爬取" + page)
        page_info = dou.find_text(dou.getsource(page))
        for info in page_info:
            infos = {}
            infos = dou.getinfo(info)
            file.append(infos)
        dou.saveinfo(file)
