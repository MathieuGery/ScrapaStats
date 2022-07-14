import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import emails, sheetid

def upload_to_gsheet():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_secrets.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    try:
        sheet = client.open('Soccer')
    except:
        sheet = client.create('Soccer')
    
    try:
        sheet2 = client.open('Soccer-Scores')
    except:
        sheet2 = client.create('Soccer-Scores')
    
    for email in emails:
        sheet.share(email, perm_type='user', role='writer')
        sheet2.share(email, perm_type='user', role='writer')

    print(sheet.id)
    print(sheet2.id)
    content = open('./results/final.csv', 'r').read()
    client.import_csv(sheetid, content)
    content = open('./results/yesterday_scores.csv', 'r').read()
    client.import_csv(sheet2.id, content)
