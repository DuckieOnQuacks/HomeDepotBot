
from random import randint


def givefact():
    global fact
    file = open("funfacts.txt", "r",encoding="utf8")
    fact_list = file.readlines()
    

    fact = fact_list[randint(0,163)]
    fact = fact.replace("\n", "")
    file.close()
    return fact
