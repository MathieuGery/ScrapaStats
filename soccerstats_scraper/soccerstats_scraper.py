# Import libraries
from operator import contains
import requests
import csv
import re
import os
import datetime
from bs4 import BeautifulSoup


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

def scrap(url):
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
    return data

def check_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def scrap_yesterday(url):
        # Connect to the URL
    response = requests.get(url)

    # Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(response.text, "html5lib")

    # table_data = soup.find_all('td', class_="steam")style="border-bottom:1px solid #cccccc;"
    # table_data = soup.findAll('tr', {'bgcolor': '#f0f0f0', 'style': ['border-top:1px solid #cccccc;', 'border-bottom:1px solid #cccccc;']})
    scores_top = soup.find_all('tr', {'style': 'border-top:1px solid #cccccc;', 'bgcolor': '#f0f0f0', 'height': 22})
    scores_bottom = soup.find_all('tr', {'style': 'border-bottom:1px solid #cccccc;', 'bgcolor': '#f0f0f0', 'height': 22})
    scores_top_array = []
    scores_bottom_array = []
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    data = []
    for i in scores_top:
        name = re.sub(CLEANR, '', str(i.find("td")))
        score = re.sub(CLEANR, '', str(i.find("b")))
        tuple = (name, score)
        scores_top_array.append(tuple)
    for i in scores_bottom:
        name = re.sub(CLEANR, '', str(i.find("td")))
        score = re.sub(CLEANR, '', str(i.find("b")))
        tuple = (name, score)
        scores_bottom_array.append(tuple)
    
    for top, bottom in zip(scores_top_array, scores_bottom_array):
        if (top[0] and top[1] and bottom[0] and bottom[1]):
            data.append([top[0], top[1]])
            data.append([bottom[0], bottom[1]])
    return data