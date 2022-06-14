from glob import escape
import re
import json
import datetime
from time import sleep
import copy
from difflib import SequenceMatcher
from coockies import coockies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def useRegex(input):
    pattern = re.compile(r"20:00 ", re.IGNORECASE)
    return pattern.match(input)

def get_tomorrow_date():
    tdate = datetime.date.today() + datetime.timedelta(days=1)
    return str(tdate).replace("-", "")

def clean_ligue_string(string):
    if (string[0] == ' '):
        return string[1:]
    return string

def extract_link_to_oe(ligue, links):
    highest = 0
    ret_link = ""

    for link in links:
        ratio = SequenceMatcher(None, ligue, link).ratio()
        if (ratio > highest):
            highest = ratio
            ret_link = link
    return ret_link + "#over-under;2"

def create_json_from_data(data):
    ret_data = []
    begin = ""
    temp_obj = {}
    toto = False
    previous_item = ''
    previous_ligue = ''
    current_ligue = ''

    for item in data:
        if (item == "»" or toto == True):
            if (toto):
                current_ligue = clean_ligue_string(previous_ligue) + '/' +  clean_ligue_string(item)
                toto = False
            else:
                toto = True
                previous_ligue = previous_item
        if (item.isnumeric() and begin == 'Step5'):
            temp_obj["bs"] = copy.deepcopy(item)
            begin = ""
            ret_data.append(copy.deepcopy(temp_obj))
            temp_obj = {}
        if (isfloat(item) and begin == 'Step4'):
            temp_obj["2"] = copy.deepcopy(item)
            begin = "Step5"
        if (isfloat(item) and begin == 'Step3'):
            temp_obj["X"] = copy.deepcopy(item)
            begin = "Step4"
        if (isfloat(item) and begin == 'Step2'):
            temp_obj["1"] = copy.deepcopy(item)
            begin = "Step3"
        if ("-" in item and begin == ""):
            begin = "Step2"
            temp_obj["match"] = copy.deepcopy(re.sub("^[\d\s\:]+", '', item))
        if (current_ligue):
            temp_obj["ligue"] = current_ligue
        previous_item = item
    return ret_data

def scraper(tdate):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    DRIVER_PATH = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    url = 'https://www.oddsportal.com/matches/soccer/' + tdate
    print("URL :", url)
    driver.get(url)
    sleep(3)
    driver.delete_all_cookies()
    for coockie in coockies:
        driver.add_cookie(coockie)
    driver.get(url)
    sleep(3)
    driver.refresh()
    tbody = driver.find_element_by_xpath('//*[@id="table-matches"]/table/tbody')
    data = tbody.text.replace(" 1 X 2 B's", "")
    links = []
    for elem in driver.find_elements_by_xpath("//a[@href]"):
        links.append(elem.get_attribute("href"))
    driver.quit()
    return (data.splitlines(), links)

def create_oe_links(matchs, links):
    for match in matchs:
        ligue = match.get("ligue").replace(" ", "-").lower()        
        link = "https://www.oddsportal.com/soccer/" + ligue + "/" + match.get("match").replace(" ", "-").lower()
        link = link.replace("---", "-")
        match["mabite"] = link
        match["oe_link"] = extract_link_to_oe(link, links)

data, links = scraper(get_tomorrow_date())
data = create_json_from_data(data)
create_oe_links(data, links)

print(json.dumps(data, indent=4))
# print(extract_link_to_oe("https://www.oddsportal.com/soccer/argentina/liga-profesional/talleres-cordoba-newells-old-boys" ,links))
# https://www.oddsportal.com/soccer/argentina/liga-profesional/talleres-cordoba-newells-old-boys-xjmv8869/
# print(links)
# https://www.oddsportal.com/soccer/usa/usl-league-two/dayton-kings-hammer-Qys3cgmn/#over-under;2

# https://www.oddsportal.com/soccer/morocco/botola-pro/olympique-khouribga-chabab-mohammedia-CIAc17YB/






# https://www.oddsportal.com/soccer/sweden/division-2-norra-svealand/korsnas-kvarnsveden-bw5uJRke/#over-under;2
# https://www.oddsportal.com/soccer/sweden/division-2-norra-svealand/#over-under;2