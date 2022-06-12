from time import sleep
from coockies import coockies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

driver.get('https://www.oddsportal.com/matches/soccer/20220611/')
sleep(3)
driver.delete_all_cookies()
for coockie in coockies:
    driver.add_cookie(coockie)
driver.get('https://www.oddsportal.com/matches/soccer/20220611/')
sleep(3)
driver.refresh()
tbody = driver.find_element_by_xpath('//*[@id="table-matches"]/table/tbody')
print(tbody.text.replace(" 1 X 2 B's", ""))
print(type(tbody.text))
driver.quit()



# https://www.oddsportal.com/soccer/usa/usl-league-two/dayton-kings-hammer-Qys3cgmn/#over-under;2