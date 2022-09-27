import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from config import telegram_token, sheetid, chat_ids

class Calc:
    def __init__(self, data):
        self.data = data
    
    def __check_if_null(self, array):
        for item in array:
            if item == "":
                return False
        return True

    def calc1(self):
        "Si les valeurs de la colonne H ET de la colonne R sont supérieures ou égales à 2 ET si les valeurs de la colonne"
        "AA est supérieure ou égale à 1,49 alors à ce moment je voudrais que les infos du match soient envoyées sur Telegram."
        res = "🚨 Over 2,5 🚨\n\n"
        size = len(res)
        for item in self.data:
            if (item.get("H") != "" and item.get("R") != "" and item.get("AA") != ""):
                h = float(item.get("H").replace(",", "."))
                r = float(item.get("R").replace(",", "."))
                j = float(item.get("J").replace(",", "."))
                aa = float(item.get("AA").replace(",", "."))
                if (h >= 2 and r >= 2 and aa >= 1.49 and j >= 3):
                    res += f"🏳️ {item.get('C')}\n"
                    res += f"⚽️ Match: {item.get('L')} - {item.get('N')}\n"
                    res += f"📅 Date: {item.get('B')}\n"
                    res += f"⏱  Horaire: {item.get('M')}\n"
                    res += f"🏆 Cote: {item.get('AE')}\n\n"
        if (len(res) == size):
            res += "⏩ No bet for tomorrow"
        return res

    def calc2(self):
        res = "🚨 1X 🚨\n\n"
        size = len(res)
        for item in self.data:
            if self.__check_if_null([item.get("I"), item.get("G"), item.get("X"), item.get("Y")]):
                i = float(item.get("I").replace(",", "."))
                g = float(item.get("G").replace(",", ".").replace("%", ""))
                x = float(item.get("X").replace(",", "."))
                y = float(item.get("Y").replace(",", "."))
                var =  (x * y) / (x + y)
                if (var >= 1.9 and i >= 2.2 and g >= 70):
                    res += f"🏳️ {item.get('C')}\n"
                    res += f"⚽️ Match: {item.get('L')} - {item.get('N')}\n"
                    res += f"📅 Date: {item.get('B')}\n"
                    res += f"⏱  Horaire: {item.get('M')}\n"
                    res += f"🏆 Cote: {var}\n\n"
        if (len(res) == size):
            res += "⏩ No bet for tomorrow"
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
    calc = calc_instance.calc2()
    send_message(calc)
    return

if __name__ == '__main__':
    main()