from textwrap import indent
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

def create_diver_for_ou_scraper():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def ou_scraper(url, driver):

    print("URL :", url)
    driver.get(url)
    # sleep(4)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    tables = soup.find_all('div', {"class": ["table-container"], "style": ""})
    ret = []
    for tab in tables:
        temp_obj = {}
        if (len(tab["class"]) != 1):
            continue
        infos = tab.find_all("a")
        temp_obj["o/u"] = infos[0].text[:-1]
        if (len(infos) >= 4):
            temp_obj["over"] = infos[2].text.replace(".", ",")
            temp_obj["under"] = infos[1].text.replace(".", ",")
            temp_obj["payout"] = tab.find('span').text
        ret.append(temp_obj)
    return ret
