# Import libraries
import requests
import csv
import re
import os
import datetime
from bs4 import BeautifulSoup

# Set the URL you want to webscrape from
url = 'https://www.soccerstats.com/matches.asp?matchday=2&listing=2'

def make_csv(data):
    #Create results folder
    try:
        os.mkdir("./results")
    except:
        pass
    header = ["Country", "BTS", "FTS", "CS", "W%", "TG", "PPG", "GP", "Scope", "Pays", "Time", "Pays", "Scope", "GP", "PPG", "TG", "W%", "CS", "FTS", "BTS"]
    with open('./results/soccerstats.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

def get_tomorrow_date_for_csv():
    tdate = datetime.date.today() + datetime.timedelta(days=1)
    return str(tdate).replace("-", "/")

def scrap():
    # Connect to the URL
    response = requests.get(url)

    # Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(response.text, "html.parser")

    table_data = soup.find('tbody')
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    data = []
    for key in table_data:
        temp_row = []
        temp_row.append(get_tomorrow_date_for_csv())
        for row in key.findAll("td"):
            temp_row.append(re.sub(CLEANR, '', str(row).replace(" ", "")))
        data.append(temp_row)
    make_csv(data)
    return data
