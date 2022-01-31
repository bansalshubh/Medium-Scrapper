from django.shortcuts import render,HttpResponse
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree
from selenium.webdriver.chrome.options import Options
import requests
import time

path = "chromedriver"

#Custom Functions Here
def get_Data(tag):
    URL = "https://medium.com/tag/{}/latest".format(tag)
    data = dict()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
    driver.get(URL)
    time.sleep(4)
    page = driver.page_source
    err = driver.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/section[1]/div[1]/div/div[2]/div/div[2]/div[1]')
    if(len(err) > 0 and err[0].get_attribute('textContent') == '404'):
        return None
    # for i in range(1,10):
    #     related = driver.find_elements_by_xpath('//*[@id="root"]/div/div[4]/div/div/div[3]/div/div/div/div/div[2]/div/div[2]/div[{}]/a/div'.format(i))
    #     if(len(related) > 0):
    #         print(related[0].get_attribute('textContent'))
    #         related_tags.append(related[0].get_attribute('textContent'))
    # if(len(related_tags) > 0):
    #     data['related_tags'] = related_tags    
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser')
    titles = []
    related_tags = []
    authors = []
    texts = []
    times_ago = []
    mins_read = []
    links = []
    
    # Getting the title
    title = soup.select("div>div>a>div>h2")
    for t in title:
        titles.append(t.text)
    print(data.keys())
    if(len(titles) > 0):
        data['titles'] = titles

    # Getting the author
    author = soup.select("span>div>a>p")
    for t in author:
        authors.append(t.text)
    print(data.keys())
    if(len(authors) > 0):
        data['authors'] = authors

    # Getting the text
    texty = soup.select("a>div>p")
    for t in texty:
        texts.append(t.text)
    print(data.keys())
    if(len(texts) > 0):
        data['texts'] = texts

    # Getting the mins_read
    minutes = soup.select("div>a>p>span")
    for t in minutes:
        mins_read.append(t.text)
    print(data.keys())
    if(len(mins_read) > 0):
        data['mins_read'] = mins_read

    # Getting the mins_read
    times = soup.select("span>a>p")
    for t in times:
        times_ago.append(t.text)
    print(data.keys())
    if(len(times_ago) > 0):
        data['times_ago'] = times_ago

    # Getting the article Links
    link = soup.find_all('a',{"aria-label":"Post Preview Title"})
    for t in link:
        links.append("https://medium.com"+t['href'])
    if(len(links) > 0):
        data['links'] = links

    #Get the Related Topics
    dom = etree.HTML(str(soup))
    for i in range(1,10):
        l = dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div/div[1]/div[2]/div[3]/div/div[2]/div[{}]/a/div'.format(i))
        if(len(l) > 0):
            related_tags.append(l[0].text)
    if(len(related_tags) > 0):
        data['related_tags'] = related_tags

    return data



# Create your views here.
def index(request):
    data = get_Data("cooking")
    if(data == None):
        return HttpResponse("404")
    while('titles' not in data):
        data = get_Data("cooking")
        if(data == None):
            return HttpResponse("404")
    # print(data.keys())
    for datas in data:
        print(data[datas])
        print()
    # print(data['related_tags'])
    return HttpResponse("Home Page of Medium Scrapper")
