import requests
from bs4 import BeautifulSoup
from random import randint
import re

def get_song_url(search_query):
  url_int = "http://www.google.com/search?q="+ search_query +"+song+youtube&tbm=vid"
  page = requests.get(url_int).text
  soup = BeautifulSoup(page, 'html.parser')
  soup = soup.find("div", class_="kCrYT")
  #print(soup)
  strings = str(soup)
  link = []
  for x in range (35,82):
    link.append(strings[x])
  linkSF = ' '.join(link)

  linkF = linkSF.replace(" ","")
  linkFinal = linkF.replace("%3Fv%3D","?v=")
  #print(linkFinal)
  return(linkFinal)
 
  
get_song_url("molly playboi carti")
