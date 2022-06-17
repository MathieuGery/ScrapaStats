import json
from make_csv import make_csv
from oddsportal_scraper.oddsportal_scraper import let_the_magic_begin
from soccerstats_scraper.soccerstats_scraper import scrap
from difflib import SequenceMatcher

soccerstats_data = scrap()
oddsportal_data = let_the_magic_begin()
print(json.dumps(oddsportal_data, indent=4))

def find_ou_in_match(ou_oddsportal, ou):
    for ou_odd in ou_oddsportal:
        if (ou_odd == ou):
            return True
    return False

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

for match in soccerstats_data:
    over_under = ["Over/Under +1.5", "Over/Under +2", "Over/Under +2.5", "Over/Under +3", "Over/Under +3.5", "Over/Under +4", "Over/Under +4.5"]
    obj = find_the_match1(match[10] + " - " + match[12], oddsportal_data)
    if (obj):
        match.append(obj.get("1"))
        match.append(obj.get("X"))
        match.append(obj.get("2"))
        for ou in obj.get("ou_stats"):
            found = False
            for i in over_under:
                if (i == ou.get("o/u") ):
                    match.append(ou.get("over"))
                    match.append(ou.get("under"))
                    found = True
            if (found == False):
                match.append("None")
                match.append("None")

for i in soccerstats_data:
    print(i)
make_csv(soccerstats_data)