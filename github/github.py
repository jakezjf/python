# -*- coding: utf-8 -*-

import requests
import re

class git():
    def __init__(self):
        print "爬虫开始运行"

    def change(self,url,max_page):
        now_page = int(re.search('p=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,max_page):
            link = re.sub('p=(\d+)','p=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

    def get_html(self,url):
        html = requests.get(url)
        return html.text

    def get_all_repository(self,repository):
        all_repository = re.findall('<h3 class="repo-list-name">(.*?)</h3>',repository,re.S)
        return all_repository

    def get_repository_info(self,every):
        info = {}
        info['title'] = re.findall('">(.*?)<em>',every,re.S)
        info['url'] = re.findall('<a href="(.*?)">',every,re.S)
        return info

    def saveinfo(self,project_info):
        f = open('git.txt','w')
        for each in project_info:
            title = 'title: '+"".join(each['title'])
            url = '  url: https://github.com'+"".join(each['url']) + '\n'
            f.writelines(title)
            f.writelines(url)
        f.close()

    def find(self,url,max_page):
        project_info = []
        all_links = git.change(url,int(max_page)+1)
        for link in all_links:
            print "正在爬取 ：" + link
            html = git.get_html(link)
            all_repository = git.get_all_repository(html)
            for every in all_repository:
                info = git.get_repository_info(every)
                project_info.append(info)
        git.saveinfo(project_info)



if __name__ == '__main__':
    git = git()
    search = raw_input("请输入你要查找的相关内容：")
    max_page = raw_input("你要查找几页内容：")
    radio = raw_input("排序方式：" + "\n" + "1.Best match\n" + "2.Most stars\n" + "3.Fewest stars\n"
    + "4.Most forks\n" + "5.Fewest forks\n" + "6.Fewest forks\n" + "7.Least recently update\n")
    if int(radio)==1:
        url = "https://github.com/search?p=1&q=" + search + "&type=Repositories&utf8=%E2%9C%93"
    elif int(radio)==2:
        url = "https://github.com/search?o=desc&p=1&q=" + search + "&s=stars&type=Repositories&utf8=%E2%9C%93"
    elif int(radio)==3:
        url = " https://github.com/search?o=asc&p=1&q=" + search + "&s=stars&type=Repositories&utf8=%E2%9C%93"
    elif int(radio)==4:
        url = "https://github.com/search?o=desc&p=1&q=" + search + "&s=forks&type=Repositories&utf8=%E2%9C%93"
    elif int(radio)==5:
        url = "https://github.com/search?o=asc&p=1&q=" + search + "&s=forks&type=Repositories&utf8=%E2%9C%93"
    elif int(radio)==6:
        url = "https://github.com/search?o=desc&p=1&q=" + search + "&s=updated&type=Repositories&utf8=%E2%9C%93"
    git.find(url,max_page)

