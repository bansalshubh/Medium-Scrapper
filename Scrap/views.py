from django.shortcuts import render,HttpResponse
from bs4 import BeautifulSoup
from selenium import webdriver
from django import template
from lxml import etree
from selenium.webdriver.chrome.options import Options
from .models import SearchHistory
import requests
import datetime
from dateutil.relativedelta import relativedelta
import time
path = "chromedriver"
related_tags = []
#Custom Functions Here

def takeSleep(tak):
    time.sleep(2)
    return True

def get_Data(tag):
    URL = "https://medium.com/tag/{}/latest".format(tag)
    data = []
    #Getting the results of page
    result = requests.get(URL)

    #passing into soup to get html page content
    soup = BeautifulSoup(result.content, 'html.parser')

    #finding page exists or not
    err = soup.select("#root > div > div.l.c > div > div > div.dd.de.df.dg.dh.di.l.dj > section.ev.ew.dq.dl.l.ex.ey.ez.fa.fb.fc.fd.fe.ff.fg.fh.fi.fj.fk.fl > div.l.h.g > div > div:nth-child(2) > div > div.fy.b > div.fz.ga.gb.gc.gd.ge.gf.gg.gh.gi.gj.gk.fx.b.gl.gm.gn")
    if(len(err) > 0 and err[0].text == "404"):
        return None

    #finding the details
    title = soup.select("div>div>a>div>h2")
    author = soup.select("span>div>a>p")
    texty = soup.select("a>div>p")
    minutes = soup.select("div>a>p>span")
    times = soup.select("span>a>p")
    link = soup.find_all('a',{"aria-label":"Post Preview Title"})
    if(len(texty) > 0 and len(title) > 0):
        leng = len(texty)-len(title)
        for i in range(leng):
            texty.pop()

    #Fetching the details for every article
    for t,tex,a,times,mins,links in zip(title,texty,author,times,minutes,link):
        detail = []
        detail.append(t.text)
        detail.append(tex.text)
        detail.append(a.text)
        l = times.text
        detail.append(l[1:])
        detail.append(mins.text)
        detail.append("https://medium.com"+links['href'])
        data.append(detail)

    # Get the Related Topics
    # dom = etree.HTML(str(soup))
    # for i in range(1,10):
    #     l = dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div/div[1]/div[2]/div[3]/div/div[2]/div[{}]/a/div'.format(i))
    #     if(len(l) > 0):
    #         related_tags.append(l[0].text)
    # print(related_tags)
    # if(len(related_tags) > 0):
    #     data.append(related_tags)
    if(len(related_tags) == 0):
        for i in range(1,10):
            l = soup.select("#root > div > div.l.c > div > div > div.dk.dl.c.dm.h.k.j.i.bl.dn.do.dp > div > div > div > div.l.gz > div.eh.l > div.ie.gi.l > div > div.o.gk.iu > div:nth-child({}) > a > div".format(i))
            if(len(l) > 0):
                s = l[0].text
                s = s.replace(" ","-")
                related_tags.append(s)

    return data

#//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/a/div


# Create your views here.
def index(request):
    return render(request,'index.html')

def history(request):
    his = SearchHistory.objects.all()
    hist = []
    for h in his:
        myhist = {
            "id":h.SearchId,
            "tag" : h.SearchTagName,
            "date":h.SearchDate
        }
        hist.append(myhist)
    params = {"results":hist}
    print(hist)
    return render(request,'History.html',params)

def scrapper(request):
    tag = request.POST['tag']
    related_tags.clear()
    if(tag == ""):
        return HttpResponse("Invalid Tag")
    tag = tag.strip(" ")
    tag = tag.lower()
    tag = str(tag.replace(" ","-"))
    one_year_from_now = datetime.datetime.now() + relativedelta(years=0)
    date_formated = one_year_from_now.strftime("%Y-%m-%d")
    print(date_formated)
    myhistory = SearchHistory.objects.create(SearchTagName=tag,SearchDate=date_formated)
    myhistory.save()
    start=time.time()
    data = get_Data(tag)
    if(data == None):
        return HttpResponse("404")
    while(len(data) == 0):
        data = get_Data(tag)
        if(data == None):
            return HttpResponse("404")
    end = int(time.time()-start)
    params = {"results" : data,"tag":tag,"related":related_tags}
    return render(request,"data.html",params)
