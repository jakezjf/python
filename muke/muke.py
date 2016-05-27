#-*_coding:utf8-*-
import requests
import re


class muke():
    def __init__(self):
        print "开始运行"

    def changepage(self,url,maxpage):
        now_page = int(re.search('page=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,maxpage + 1):
            link = re.sub('page=(\d+)','page=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

    def getsource(self,url):
        html = requests.get(url)
        return html.text

    def geteveryclass(self,source):
        everyclass = re.findall('<h5>(.*?)</h5>',source,re.S);
        return everyclass

    def getinfo(self,eachclass):
        info = {}
        info['title'] = re.search('.*?',eachclass,re.S)
        return info

    def saveinfo(self,classinfo):
        f = open('info.txt','a')
        for each in classinfo:
            f.writelines('title:' + '\n')
        f.close()

if __name__ == '__main__':
    muke = muke()
    classinfo = []
    url = "http://www.imooc.com/course/list?page=1"
    all_links = muke.changepage(url,10)
    for link in all_links:
        print u'正在处理页面：' + link
        html = muke.getsource(link)
        everyclass = muke.geteveryclass(html)
        for each in everyclass:
            info = muke.getinfo(each)
            classinfo.append(info)
    muke.saveinfo(classinfo)







