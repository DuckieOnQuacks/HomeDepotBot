import requests
from bs4 import BeautifulSoup
from random import randint
import re



async def getmakelink(search_query):
  global link
  if " " in search_query:
    search_query = search_query.replace(" ", "+")
  else:
      search_query = search_query
  url_int = "https://www.allrecipes.com/search/results/?search=" + search_query
  page = requests.get(url_int).text
  soup = BeautifulSoup(page, 'html.parser')
  link = soup.find("a", class_="card__titleLink manual-link-behavior")['href']
  return link


async def getimage(link):
    global image
    url_int = link
    page = requests.get(url_int).text
    soup = BeautifulSoup(page, 'html.parser')
    soup = soup.find_all("img")
    imagelist = []
    for image in soup:
        if "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fimages.media-allrecipes.com%2Fuserphotos%" in (image['src']):
            imagelist.append(image['src'])
    image = imagelist[1]
    return image
        



async def getingredients(link):
    global ingredients
    url_int = link
    page = requests.get(url_int).text
    soup = BeautifulSoup(page, 'html.parser')
    soup = soup.find_all("span", class_="ingredients-item-name")
    ingredientlist = ["___***Ingredients***___ \n"]

    for span in soup:
        
        ingredient = span.text + "\n"
        ingredientlist.append(ingredient)

    ingredients = "".join(ingredientlist)
    return ingredients

async def getdirections(link):
    global directions
    url_int = link
    page = requests.get(url_int).text
    soup = BeautifulSoup(page, 'html.parser')
    soup = soup.find_all("div", class_="paragraph")
    directionlist = ["___***Directions***___ \n"]
    startnum = 1
    for span in soup:
        
        direction = str(startnum) + ". " + span.text + "\n"
        directionlist.append(direction)
        startnum += 1
    directions = "".join(directionlist)
    return directions   

  
