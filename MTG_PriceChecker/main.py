import discord
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()




def convert(lst):
    return ' '.join(lst)


def filterer(dict):
    filtered = {k: v for k, v in dict.items() if v is not None}
    dict.clear()
    dict.update(filtered)
    return(dict)


def getCardData(URL):
    print(URL)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    # this is just to ensure that the page is loaded
    #time.sleep(3)

    html = driver.page_source

    soup = BeautifulSoup(html,
                         'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib

    tags = soup.find_all('a')
    urls = []
    setAndPrice = {}
    printsFlag = False
    ViewAllPrintsFlag = False
    for t in tags:
        temp = t.text.split()
        if "View" in temp and "all" in temp and "prints" in temp:
            ViewAllPrintsFlag = True

        if printsFlag is True and ViewAllPrintsFlag is False and temp:
            if not any("$" in s for s in temp):
                setAndPrice[convert(temp)] = None
            else:
                setAndPrice[list(setAndPrice.keys())[-1]] = convert(temp)

        if "Prints" in temp and printsFlag is False:
            printsFlag = True

        try:
            urls.append(t.attrs['href'])
        except:
            print('failed to find href')
    driver.close()
    driver.quit()
    return filterer(setAndPrice)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0] == '!':
        s = message.content.split('!')
        card = s[1]
        print(type(card))
        temp = card.replace(' ', '-')

        setAndPrice = getCardData("https://scryfall.com/search?q="+temp)

        if setAndPrice:
            ret = ""
            for i, j in setAndPrice.items():
                ret = ret + i + "\n" + "\t" + j + "\n"
            await message.channel.send(ret)
        else:
            await message.channel.send("Cannot find try again!")



client.run(TOKEN)