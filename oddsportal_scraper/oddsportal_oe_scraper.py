from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scraper(url):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    DRIVER_PATH = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    print("URL :", url)
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    tables = soup.find_all('div', {"class": ["table-container"], "style": ""})
    for tab in tables:
        temp_obj = {}
        if (len(tab["class"]) != 1):
            continue
        infos = tab.find_all("a")
        temp_obj["o/u"] = infos[0].text
        temp_obj["over"] = infos[2].text
        temp_obj["under"] = infos[1].text
        temp_obj["payout"] = tab.find('span').text
        print(temp_obj)
    driver.quit()
    return 

scraper("https://www.oddsportal.com/soccer/usa/usl-league-two/houston-fc-ahfc-royals-WYPon4DJ/#over-under;2")