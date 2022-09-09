import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from config import telegram_token, sheetid, chat_ids

class Calc:
    def __init__(self, data):
        self.data = data
    
    def calc1(self):
        "Si les valeurs de la colonne H ET de la colonne R sont supérieures ou égales à 2 ET si les valeurs de la colonne"
        "AA est supérieure ou égale à 1,49 alors à ce moment je voudrais que les infos du match soient envoyées sur Telegram."
        res = []
        for item in self.data:
            if (item.get("H") != "" and item.get("R") != "" and item.get("AA") != ""):
                h = float(item.get("H").replace(",", "."))
                r = float(item.get("R").replace(",", "."))
                aa = float(item.get("AA").replace(",", "."))
                if (h >= 2 and r >= 2 and aa >= 1.49):
                    print("ca match:"," ",item.get("L"), "", h, " ",r ," ", aa)
        return res

def create_json(data):
    cols = ['a','b','c','d','e','f','g','h','i','j','k','l',
                'm','n','o','p','q','r','s','t','u','v','w',
                'x','y','z','aa','ab','ac','ad','ae','af',
                'ag','ah','ai','aj','ak','al','am','an']
    res = []
    for row in data[1:]:
        temp_obj = {}
        for i in range(1, len(data[0])):
            temp_obj[cols[i].upper()] = row[i]
        res.append(temp_obj)
    return res

def get_sheet(sheetid):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('./google_secrets.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheetid)
    worksheet = sheet.worksheet('Soccer')
    data = worksheet.get_all_values()
    data = create_json(data)
    return data

def send_message(data):
    for chatid in chat_ids:
        requests.post(f"https://api.telegram.org/bot{telegram_token}/sendMessage", data={"chat_id": chatid, "text": data})

def main():
    res = get_sheet(sheetid)
    calc_instance = Calc(res)
    calc = calc_instance.calc1()
    send_message(calc)
    return

if __name__ == '__main__':
    main()