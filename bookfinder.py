import requests
from bs4 import BeautifulSoup
from random import randint

def booksearch():
    print("Searching Books...")
    linklist = []
    global booklink

    url = "https://alwaysjudgeabookbyitscover.com/"

    page = requests.get(url).text

    soup = BeautifulSoup(page, 'html.parser')
    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        if link:
            linklist.append(link)
        starti = 77
    try:
        booklink = linklist[randint(1, starti)]
    except:
        starti = starti - 1
        booklink = linklist[randint(1, starti)]
    print("Found " + booklink)
    return booklink


