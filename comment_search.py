import requests
from bs4 import BeautifulSoup
from random import randint
import re


async def givecomment():
    global retcomment
    retcomment = ""
    
    #Pornhub link list
    linklist = ["https://www.pornhub.com/view_video.php?viewkey=ph5e4155ef4a5a4",
    "https://www.pornhub.com/view_video.php?viewkey=ph6139e73643c7c",
    "https://www.pornhub.com/view_video.php?viewkey=ph5e9fceedb9cc9",
    "https://www.pornhub.com/view_video.php?viewkey=ph613100f2ca3bd",
    "https://www.pornhub.com/view_video.php?viewkey=ph608c32718faf1",
    "https://www.pornhub.com/view_video.php?viewkey=ph5f8d74e228b27",
    "https://www.pornhub.com/view_video.php?viewkey=ph5f59585a9808f"]
    
    #Picks random link to search through.
    page = requests.get(linklist[randint(0,len(linklist)-1)]).text
    soup = BeautifulSoup(page, 'html.parser')

    #Finds all items with commentMessage in it
    soup = soup.find_all("div", class_="commentMessage")
    commentlist = []
    try:
        for lines in soup:
            #Searches for certain pattern
            pattern = "<span>(.*?)</span>"
            try:
                stringiwant = re.search(pattern, str(lines)).group(1)
            except:
                print("failure to split comment")
                return

            #appends all the comments into the comment list.
            commentlist.append(stringiwant)
            retcomment = commentlist[randint(0,len(commentlist)-1)]
    except:
        print("failure to find comment")
        retcomment = ""
    return retcomment



