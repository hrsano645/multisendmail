import base64
import os
import pickle
import traceback
from email.mime.text import MIMEText
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
]

CLIENT_SECRETS_FILE = Path(__file__).parent / "client_secret.json"

# configから情報を取得
# pythonスクリプトな定義ファイルを読み込む
SPREADSHEET_ID = config.SPREADSHEET_ID
RANGE_NAME = config.RANGE_NAME
SASHICOMI_BODY = config.SASHICOMI_BODY
USER_ID = "me"


def get_authenticated_service(scopes, api_service_name, api_version):
    """
    oAuth2のinstalledAppsでブラウザ認証で行う
    scopesを渡して認証した後に、api_service_nameとapi_versionでscopesの範囲でのAPIアクセスオブジェクトをbuildする
    """

    # ref: https://developers.google.com/sheets/api/quickstart/python#step_3_set_up_the_sample, https://dev.classmethod.jp/articles/oauth2client-is-deprecated/
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, scopes
            )
            creds = flow.run_console()
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(api_service_name, api_version, credentials=creds)


def main():

    # それぞれの認証=>APIアクセスオブジェクトを用意
    gsheet_service = get_authenticated_service(SCOPES, "sheets", "v4")
    gmail_service = get_authenticated_service(SCOPES, "gmail", "v1")

    # Googleスプレッドシートから設定にある表をget
    result = (
        gsheet_service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    # 列見出しで辞書化する
    fieldname = values[0]
    # 列見出しは"mail"固定だが、"email"があればemailにする
    # TODO: 2021/10/22 ここは列見出し名が曖昧な場合もあるので、決めうちの指定を複数用意する
    mail_keyname = "mail"
    if "email" in fieldname:
        mail_keyname = "email"
    mapd_values = [dict(zip(fieldname, row)) for row in values[1:]]

    # 情報を収集して、メールアドレスと差し込み文章を用意
    mailaddr_and_body = [
        {"email": row[mail_keyname], "body": SASHICOMI_BODY.format(**row)}
        for row in mapd_values
    ]

    # print(mailaddr_and_body)
    # exit()

    # メール下書きを生成する
    sender = config.sendmail_from
    subject = config.sendmail_subject
    cc_list = config.sendmail_cc_addrs

    for addr_and_body in mailaddr_and_body:

        to = addr_and_body["email"]
        message_text = addr_and_body["body"]
        message = MIMEText(message_text, _charset="utf-8")
        message["to"] = to
        message["from"] = sender
        message["subject"] = subject
        message["Cc"] = ",".join(cc_list)
        message_body = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

        try:
            send_message_body = {"message": message_body}
            draft = (
                gmail_service.users()
                .drafts()
                .create(userId=USER_ID, body=send_message_body)
                .execute()
            )
            print(
                "下書き生成 Draft id: {}\nDraft message: {}".format(
                    draft["id"], draft["message"]
                )
            )

        except HttpError:
            print("Gmail APIへアクセスできませんでした。")
            traceback.print_exc()


if __name__ == "__main__":
    main()
