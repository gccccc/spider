#!/usr/bin/env python
# coding=utf-8
from spider import Spider
spider = Spider()
spider.setworkdir('/data/work/ys/oriinfo/ownerinfo/')
spider.setfilename('owneridlist.txt')
f = open(spider.getfilename(),'r+')
while True:
    dic = {}
    dic['diary'] = dic['information'] = dic['allComments'] = dic['order'] = {}
    line = f.readline()
    if not line:
        break
    line = line[:-1]
    print line
    soup = spider.getSoup('http://www.xiaozhu.com/fangdong/' + line + '/pinglun.html')
    ul = soup.find('ul',{'class':'comment_right'})
    dic['allComments']['rate'] = {}
    item = ['sanitationRate','descriptionRate','performanceRate','securityRate','locationRate']
    if ul == None:
        dic['nohtml'] = True
        for i in item:
            dic['allComments']['rate'][i] = 'NULL'
        dic['allComments']['rate']['allcommentRate'] = 'NULL'
    else:
        dic['nohtml'] = False
        liAll = ul.findAll('li')
        cot = 0
        for li in liAll:
            print li
            grade = li.find('span').find('em').get('value')
            dic['allComments']['rate'][item[cot]] = grade
            cot+=1
        value = soup.find('div',{'class':'comment_left'}).find('span').get('value')
        dic['allComments']['rate']['allcommentRate'] = value
    print dic
    if not dic['nohtml']:
        soup = spider.getSoup('http://www.xiaozhu.com/fangdong/' + line + '/yuding.html')
        hd = soup.find('ul',{'class':'fd_navUl'})
        aAll = hd.findAll('a')
        mp = {u'短租日记':u'diaryNum',u'房源信息':u'informationNum',u'房客点评':u'allcommentsNum',u'预订历史':u'orderNum'}
        for a in aAll:
            li = a.find('li')
            strong = li.find('strong')
            strongstr = u'' + strong.string
            num = li.find('span').string
            print num
            num = spider.Reg(u'\d+',(str)(num) + 'u')
            dic[mp[strongstr]] = (int)(num)
        soup.find('table',{'class':'table_fd'})
        trAll = soup.findAll('tr')
        print trAll
        for tr in trAll:
            tdAll = tr.findAll('td')
            num = (int)(tdAll[0].string)
            a = tdAll[1].find('a')
            href = a.get('href')
            name = a.string()
            spanAll = tdAll[2].findAll('span')
            day = spanAll[0].string
            period = spanAll[1].contents[0].contents
            ab = tdAll[3].string
    else:
        pass
    
f.close()

