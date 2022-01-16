from flask import Flask, render_template, request, redirect, url_for, Response, session
import psycopg2
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route("/", methods=['post', 'get'])
def index():
    options = Options()
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-sh-usage')
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=options)
    driver.get('https://www.nseindia.com/get-quotes/equity?symbol=BCG')

    # Wait for the page to fully load
    time.sleep(3)

    # Step 2: Parse HTML code and grab tables with Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    market_depth= soup.find(id='marketDepthTable')
    scrip_info= soup.find(id='equityInfo')
    # Step 3: Read tables with Pandas read_html()
    marketdata = pd.read_html(str(market_depth))

    result = []
    allrows = market_depth.findAll('tr')
    for row in allrows:
        result.append([])
        allcols = row.findAll('td')
        for col in allcols:
            thestrings = [s for s in col.findAll(text=True)]
            thetext = ''.join(thestrings)
            result[-1].append(thetext)
    
    scrip_result= []
    scrip_allrows = scrip_info.findAll('tr')
    for row in scrip_allrows:
        scrip_result.append([])
        scrip_allcols = row.findAll('td')
        for col in scrip_allcols:
            scrip_thestrings = [s for s in col.findAll(text=True)]
            scrip_thetext = ''.join(scrip_thestrings)
            scrip_result[-1].append(scrip_thetext)
    finalData=result + scrip_result

    driver.close()


    return render_template("index.html", data=finalData)


if __name__ == '__main__':
   app.run(debug=True)
