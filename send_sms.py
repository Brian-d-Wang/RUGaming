import os
#from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import requests
from bs4 import BeautifulSoup
# from selenium import webdriver 
# from selenium.webdriver.common.keys import Keys 
import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])
def sms_greeting():
    body = request.values.get('Body', None)
    resp = MessagingResponse()
    body = re.sub(r'[^a-zA-Z0-9 ]', '', body)
    body = body.lower()
    try:
        ind = body.index("im")
        meme = body[ind + 3:len(body)]
        resp.message("Hi " + meme + ", I'm dad")
        return str(resp)
    except:
        resp.message(sms_reply(body))
        return str(resp)

def sms_reply(game_message):
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number    
    bod = re.sub(r'[^a-zA-Z0-9]', '', game_message)
    title = bod
    bod = bod.replace("1", "i")
    bod = bod.replace("2", "ii")
    bod = bod.replace("3", "iii")
    bod = bod.replace("4", "iv")
    bod = bod.replace("5", "v")
    bod = bod.replace("6", "vi")
    bod = bod.replace("7", "vii")
    bod = bod.replace("8", "viii")
    bod = bod.replace("9", "ix")
    body = bod.lower()

    # Start our TwiML response
    #resp = MessagingResponse()
    price, location, link = scraping(body)
    wordy = " on sale for: "
    stra = title + wordy + price + " at: " + location + " " + link 
    # Determine the right reply for this message
    #resp.message(stra)
    #return str(resp)
    return stra

def scraping(game_name):

    #s = Service(r'C:/Users/cool4/Downloads/chromedriver_win32')
    driver = webdriver.Chrome(executable_path=r'C:/Users/cool4/Downloads/chromedriver_win32/chromedriver.exe')

    driver.get('https://isthereanydeal.com/#/filter:&search/%s'%game_name)
    time.sleep(1) 
    SCROLL_PAUSE_TIME = 0.4


    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    pagesource = driver.page_source

    #page = requests.get('https://isthereanydeal.com') # Getting page HTML through request
    soup = BeautifulSoup(pagesource, 'lxml') # Parsing content using beautifulsoup
    a = soup.select("a[href^=?game_name]")
    print(a)
    price = soup.find('a', {'data-evt' : '["shop","click","%s"]'%(game_name)})
    if (price == None):
        return
    else:
        try: 
            rest = price.find_all_next('a', {'data-evt' : '["shop","click","%s"]'%(game_name)})
            place = rest[len(rest)-1]['data-slc']
            link = rest[len(rest)-1]['href']
            return rest[len(rest)-1].text, place , link
        except: 
            rest = price
            place = rest['data-slc']
            link = rest['href']
            return(rest.text, place , link)

# def scrape2(genre):
#     page = requests.get('https://www.metacritic.com/browse/games/genre/metascore/%s/all?view=detailed'%genre)
#     soup = BeautifulSoup(page.content, 'html.parser')
      
#     #games = soup.find(')

if __name__ == "__main__":
    app.run(debug=True)
    