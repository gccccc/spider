#!/usr/bin
#encoding:utf-8
import json,zlib,datetime,sys,urllib,urllib2,re,os,socket,time
from bs4 import BeautifulSoup

class Spider:
    __sleep_time = 0
    __wait_time = 0
    __dir_stack = []     #用堆栈管理目录
    __file_name = ''
    def getsleeptime(self):
        return self.__sleep_time
    def setsleeptime(self,stime):
        self.__sleep_time = stime
    def setfilename(self,name):
        self.__file_name = self.getworkdir() + name
    def getfilename(self):
        return self.__file_name
    def getwaittime(self):
        return self.__wait_time
    def setwaittime(self,stime):
        self.__wait_time = stime
    def w_sleep(self):
        time.sleep(self.getwaittime())
    def s_sleep(self):
        time.sleep(self.getsleeptime())
    def getworkdir(self):
        if len(self.__dir_stack) <= 0:
            return None
        else:
            return self.__dir_stack[len(self.__dir_stack)-1]
    def removeworkdir(self):
        if len(self.__dir_stack) <= 0:
            return None
        else:
            return self.__dir_stack.pop()
    def setworkdir(self,sdir):  #设置工作目录 
        self.__dir_stack.append(sdir)
        self.initDir(sdir)
    def saveJson(self,jsonInfo):
        f = open(self.getfilename(),'w+')
        f.write(jsonInfo)
        f.close()
    def initDir(self,nowdir):
        try:
            os.mkdir(nowdir)
        except:
            pass
    def outputLog(self,logText):
        pass
    def getResponse(self,url,data=None):#为1表示get请求 0表示post请求
        if data != None:
            data = urllib.urlencode(data)
        response = None
        errorText = ''
        now = datetime.datetime.now()
        now = now.strftime('%c')
        errorText = now + '\n'
        errorText = 'happen on ' + url + ':\n'
        html = ''
        try:
            req_header = {'user_agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)','Accept-encoding':'*'}
            req = urllib2.Request(url,None,req_header)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(req,data)
            gzipped = response.headers.get('Content-Encoding')
            html = response.read()
            if gzipped:
                 html = zlib.decompress(html, 16+zlib.MAX_WBITS)
            return html
        except urllib2.URLError, e:
              errorText = "urllib2.URLError\n"
              if hasattr(e,'code'):
                  try:
                      errorText = errorText + 'e.code:' + (str)(e.code) + '\n'
                  except:
                      errorText = errorText + 'e.code:unknow\n'
              if hasattr(e,'reason'):
                  try:
                      errorText = errorText + 'e.reason:' + (str)(e.reason) + '\n'
                  except:
                      errorText = errorText + 'e.reason:unknow' + '\n'
              self.outputLog(errorText)
        except socket.timeout as e:
              errorText = errorText + 'request timeout' + '\n'
              self.outputLog(errorText)
              return self.getResponse(url)
        return html

    def getSoup(self,url,data=None,response=None,uncode='utf-8',untype='html5lib'): #untype为解码器类型 默认为html5lib 还有lxml 和 html.parser
        if response == None:
             response = self.getResponse(url,data)
        if response == None:
             return None
        else:
             return BeautifulSoup(response,untype,from_encoding=uncode)

    def getTags(self,ssoup,tag,extra=None):#
        if isinstance(tag,list): #如果是findAll
            if extra == None:
                return ssoup.findAll(tag)
            else:
                return ssoup.findAll(tag,extra)
        else:                          #如果是search
            if extra == None:
                return ssoup.find(tag)
            else:
                return ssoup.find(tag,extra)

    def Reg(self,reg,text):
        re1 = re.compile(reg)
        match = re1.search(text)
        if match == None:
            return 'NULL'
        else:
            return match.group()

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')

    taglist = []

    def download(self,savetype,url,sign=''):
        content = self.getResponse(url)
        filename = sign + url[7:].replace('/','_')
        spider.setfilename(filename)
        if savetype:##非文本文件
            with open(self.getfilename(),'wb') as code:
                code.write(content)
        else:       ##文本文件
            with open(self.getfilename(),'w+') as code:
                code.write(content)

    def dfsTags(self,tags,depth=0):
        if depth == 0:
            self.taglist = []
        if tags == None:
            return 
        if tags.string == None:
              for tag in tags:
                   self.dfsTags(tag,depth+1)
        else:
            ss = (str)(tags.string).strip()
            ss = ss.replace('\n','')
            if cmp(ss,'') == 0:
                 pass
            else:
                 self.taglist.append(ss)
    def stringToDict(self,s):#s like "{a:'b',c:'d'}" or "{'a':'b',c:'d'}" or "{'a':b,c:d}"
        dic = {}
        s = s.strip()[1:-1]
        slist = s.split(',')
        for ss in slist:
            i = 0
            for i in range(0,len(ss)):
                if ss[i] == ':':
                    break
            s1 = ss[:i].strip()
            s2 = ss[i+1:].strip()
            if (s1[0] == "'" and s1[-1] == "'") or (s1[0] == '"' and s1[-1] == '"'): #如果key 已经是"a" or 'a'的形式 则去掉已配对的"" or '' 然后加入dict
                k = s1[1:-1]
            else:
                k = s1
            if (s2[0] == "'" and s2[-1] == "'") or (s2[0] == '"' and s2[-1] == '"'):
                v = s2[1:-1]
            else:
                v = s2
            dic[k] = v
        return dic
