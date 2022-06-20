import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import emails

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
    for email in emails:
        sheet.share(email, perm_type='user', role='writer')

    print(sheet.id)
    content = open('./results/final.csv', 'r').read()
    client.import_csv(sheet.id, content)
