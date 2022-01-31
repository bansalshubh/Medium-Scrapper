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
    related_tags = []
    for i in range(1,10):
        related = driver.find_elements_by_xpath('//*[@id="root"]/div/div[4]/div/div/div[3]/div/div/div/div/div[2]/div/div[2]/div[{}]/a/div'.format(i))
        if(len(related) > 0):
            print(related[0].get_attribute('textContent'))
            related_tags.append(related[0].get_attribute('textContent'))
    if(len(related_tags) > 0):
        data['related_tags'] = related_tags    
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser')
    titles = []
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
    # print(data.keys())


    return data




# Create your views here.
def index(request):
    data = get_Data("cooking")
    if(data == None):
        return HttpResponse("404")
    while('titles' not in data):
        data = get_Data("cooking")
    # print(data.keys())
    for datas in data:
        print(data[datas])
        print()
    # print(data['related_tags'])
    return HttpResponse("Home Page of Medium Scrapper")
