import json
import os
from pprint import pprint
import pickle

import dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from pathlib import Path

import config

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    # "https://mail.google.com/",
    'https://www.googleapis.com/auth/gmail.readonly',
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
]

dotenv.load_dotenv()
# TODO: 2021/10/21 .envにbase64でエンコードしたclient_secret.jsonをロードする
# client_secret_file = os.environ[""]
CLIENT_SECRETS_FILE=Path(__file__).parent / 'client_secret.json'

# configから情報を取得
# pythonスクリプトな定義ファイルを読み込む
# SHEET_ID = config.SHEET_ID
# SASHICOMI_BODY = config.SASHICOMI_BODY

def get_authenticated_service(scopes, api_service_name, api_version):
    """
        oAuth2のinstalledAppsでブラウザ認証で行う
        scopesを渡して認証した後に、api_service_nameとapi_versionでscopesの範囲でのAPIアクセスオブジェクトをbuildする
    """

    # ref: https://developers.google.com/sheets/api/quickstart/python#step_3_set_up_the_sample, https://dev.classmethod.jp/articles/oauth2client-is-deprecated/
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, scopes)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)

def main():

    # それぞれの認証=>APIアクセスオブジェクトを用意
    gsheet_service = get_authenticated_service(SCOPES, 'sheets', 'v4')
    gmail_service = get_authenticated_service(SCOPES, 'gmail', 'v1')

    # Googleスプレッドシートから設定にある表をget
    
    sheet = gsheet_service.spreadsheets()
    SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    SAMPLE_RANGE_NAME = 'Class Data!A2:E'

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))

    # 情報を収集して、メールアドレスと差し込み文章を用意

    # Gmail APIで下書きを生成する
    
    # Call the Gmail API
    results = gmail_service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ =="__main__":
    main()