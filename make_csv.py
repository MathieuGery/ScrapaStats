import csv


def make_csv(data):
    header = ["Date", "Country", "BTS", "FTS", "CS", "W%", "TG", "PPG", "GP", "Scope", "Pays", "Time", "Pays", "Scope", "GP", "PPG", "TG", "W%", "CS", "FTS", "BTS", "", "1", "X", "2", "Over 1,5", "Under 1,5", "Over 2", "Under 2", "Over 2,5", "Under 2,5", "Over 3", "Under 3", "Over 3,5", "Under 3,5", "Over 4", "Under 4", "Over 4,5", "Under 4,5"]
    with open('./results/final.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)