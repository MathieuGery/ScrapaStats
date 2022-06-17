import json

from numpy import array
from make_csv import make_csv
from oddsportal_scraper.oddsportal_scraper import let_the_magic_begin
from soccerstats_scraper.soccerstats_scraper import scrap
from difflib import SequenceMatcher

soccerstats_data = scrap()
oddsportal_data = let_the_magic_begin()

def find_ou_in_match(ou_oddsportal, ou):
    if (ou_oddsportal == ou):
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

def clean_obj(obj, over_under):
    ret = []
    for item in obj:
        if (item.get("o/u") in over_under):
            ret.append(item)
    return ret

for match in soccerstats_data:
    over_under = ["Over/Under +1.5", "Over/Under +2", "Over/Under +2.5", "Over/Under +3", "Over/Under +3.5", "Over/Under +4", "Over/Under +4.5"]
    obj = find_the_match1(match[10] + " - " + match[12], oddsportal_data)
    if (obj):
        match.append(obj.get("1"))
        match.append(obj.get("X"))
        match.append(obj.get("2"))
        obj = clean_obj(obj.get("ou_stats"), over_under)
        print(len(obj))
        for i in over_under:
            find = False
            for ou in obj:
                if (i == ou.get("o/u")):
                    match.append(ou.get("over"))
                    match.append(ou.get("under"))
                    find = True
            if (find == False):
                match.append("None")
                match.append("None")

make_csv(soccerstats_data)