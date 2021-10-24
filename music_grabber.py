import re
import requests
from random import randint
from bs4 import BeautifulSoup


def get_song_list(username):
  url = "https://www.last.fm/player/station/user/" + username + "/recommended"
  link_array = []  
  for x in range (0,3):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    try:
      for lines in soup:
        pattern = "https://(.*?),"
        try: 
          song = re.search(pattern,str(lines)).group(1)
        except:
          print("fail to get any links")
    except:
      print("youre dumb asf")
    link_array.append(song)
  final_song = link_array[1]
   
  return final_song




