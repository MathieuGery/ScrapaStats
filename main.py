import time
from datetime import datetime
from make_csv import make_csv, make_csv_for_yesterday_scores
from oddsportal_scraper.oddsportal_scraper import let_the_magic_begin
from soccerstats_scraper.soccerstats_scraper import scrap
from soccerstats_scraper.soccerstats_scraper import scrap_yesterday
from difflib import SequenceMatcher
from upload_to_gsheet import upload_to_gsheet

start_time = time.time()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Start at: ", current_time)
# Scraping the data from the website.
soccerstats_data = scrap("https://www.soccerstats.com/matches.asp?matchday=2&listing=2")
# Scraping the scores from yesterday.
prev_soccerstats_data = scrap_yesterday("https://www.soccerstats.com/matches.asp?matchday=0&daym=yesterday")
oddsportal_data = {}

while(True):
    try:
        oddsportal_data = let_the_magic_begin()
    except:
        print("Error with selenium, try again...")
        pass
    else:
        break

def find_the_match1(matchname, oddsportaldatas):
    highest = 0
    for odds_match in oddsportaldatas:
        ratio = SequenceMatcher(None, matchname, odds_match.get("match")).ratio()
        if (ratio > highest):
            highest = ratio
            obj = odds_match
    if (obj and highest >= 0.58):
        obj["soccestats_name"] = matchname
        obj["ratio"] = highest
        return obj
    return

def clean_obj(obj, over_under):
    ret = []
    for item in obj:
        if (item.get("o/u") in over_under):
            ret.append(item)
    return ret

for match in soccerstats_data:
    over_under = ["Over/Under +1.5", "Over/Under +2", "Over/Under +2.5", "Over/Under +3", "Over/Under +3.5", "Over/Under +4", "Over/Under +4.5"]
    obj = find_the_match1(match[11] + " - " + match[13], oddsportal_data)
    if (obj):
        match.append(obj.get("1").replace(".", ","))
        match.append(obj.get("X").replace(".", ","))
        match.append(obj.get("2").replace(".", ","))
        obj = clean_obj(obj.get("ou_stats"), over_under)
        for i in over_under:
            find = False
            for ou in obj:
                if (i == ou.get("o/u")):
                    match.append(ou.get("over"))
                    match.append(ou.get("under"))
                    find = True
            if (find == False):
                match.append("")
                match.append("")

make_csv(soccerstats_data)
make_csv_for_yesterday_scores(prev_soccerstats_data)
upload_to_gsheet()
print("--- %s seconds ---" % round((time.time() - start_time), 2))