# Import libraries
from asyncore import read
import csv
from multiprocessing.spawn import prepare

def prepare_data(data):
    for item in data:
        item.pop("ou_link")
        item.pop("bs")

def make_csv(data):
    header = ["1", "X", "2", "Over 1,5", "Over 2", "Over 2,5", "Over 3", "Over 3,5", "Over 4", "Over 4,5"]
    with open('./results/oddsportal.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
