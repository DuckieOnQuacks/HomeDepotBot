import requests
from bs4 import BeautifulSoup
import re
from random import randint

listOfTools = ["hammer","screwdriver"]

def addTool(nameOfNewTool):
    listOfTools.append(nameOfNewTool)
    
def getTool(toolName = None):
    if(toolName == None):
        tool = listOfTools[random.randint(0,len(listOfTools)-1)]
    else:
        tool = toolName
    urlTool = tool.replace(" ","%2520")
    url = "https://www.homedepot.com/s/" + urlTool + "?NCNI-5"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    print(soup) 
        
getTool("flux solder")
