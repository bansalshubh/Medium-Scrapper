from django.shortcuts import render,HttpResponse
from bs4 import BeautifulSoup
from selenium import webdriver
from django import template
from lxml import etree
from selenium.webdriver.chrome.options import Options
import requests
import time

path = "chromedriver"

#Custom Functions Here

def takeSleep(tak):
    time.sleep(2)
    return True

def get_Data(tag):
    URL = "https://medium.com/tag/{}/latest".format(tag)
    data = []
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
    # driver.get(URL)
    # time.sleep(3)
    # page = driver.page_source
    # err = driver.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/div[2]/div[1]')
    # if(len(err) > 0 and err[0].get_attribute('textContent') == '404'):
    #     return None  
    # driver.quit()
    result = requests.get(URL)
    soup = BeautifulSoup(result.content, 'html.parser')
    # titles = []
    # related_tags = []
    # authors = []
    # texts = []
    # times_ago = []
    # mins_read = []
    # links = []
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

    for t,tex,a,times,mins,links in zip(title,texty,author,times,minutes,link):
        detail = []
        detail.append(t.text)
        detail.append(tex.text)
        detail.append(a.text)
        detail.append(times.text)
        detail.append(mins.text)
        detail.append("https://medium.com"+links['href'])
        data.append(detail)





    
    # # Getting the title
    # for t in title:
    #     titles.append(t.text)
    # # print(data.keys();
    # if(len(titles) > 0):
    #     data['titles'] = titles

    # # Getting the author
    # for t in author:
    #     authors.append(t.text)
    # # print(data.keys())
    # if(len(authors) > 0):
    #     data['authors'] = authors

    # # Getting the text
    # for t in texty:
    #     texts.append(t.text)
    # # print(data.keys())
    # if(len(texts) > 0 and len(titles) > 0):
    #     leng = len(texts)-len(titles)
    #     for i in range(leng):
    #         texts.pop()
    # if(len(texts) > 0):
    #     data['texts'] = texts

    # # Getting the mins_read
    # for t in minutes:
    #     mins_read.append(t.text)
    # # print(data.keys())
    # if(len(mins_read) > 0):
    #     data['mins_read'] = mins_read

    # # Getting the mins_read
    # for t in times:
    #     times_ago.append(t.text)
    # # print(data.keys())
    # if(len(times_ago) > 0):
    #     data['times_ago'] = times_ago

    # Getting the article Links
    # for t in link:
    #     links.append("https://medium.com"+t['href'])
    # if(len(links) > 0):
    #     data['links'] = links

    #Get the Related Topics
    # dom = etree.HTML(str(soup))
    # for i in range(1,10):
    #     l = dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div/div[1]/div[2]/div[3]/div/div[2]/div[{}]/a/div'.format(i))
    #     if(len(l) > 0):
    #         related_tags.append(l[0].text)
    # if(len(related_tags) > 0):
    #     data['related_tags'] = related_tags

    return data



# Create your views here.
def index(request):
    return render(request,'index.html')

def scrapper(request):
    tag = request.POST['tag']
    if(tag == ""):
        return HttpResponse("Invalid Tag")
    tag = str(tag.replace(" ","-"))
    start=time.time()
    data = get_Data(tag)
    if(data == None):
        return HttpResponse("404")
    
    while(len(data) == 0):
        data = get_Data(tag)
        if(data == None):
            return HttpResponse("404")
    end = int(time.time()-start)
    print(end)
    
    print(data)
    params = {"results" : data,"tag":tag,"sleep":takeSleep}
    return render(request,"data.html",params)
