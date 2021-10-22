# multisendmail

PyCon mini Shizuokaで使う、メール送付下書き生成用スクリプト

## 必要なもの

- Python3.7以降
- `pip install -r requirements.txt` にてパッケージインストール
- クライアントシークレットが必要です。Google Cloud Consoleで作成してください。
  - フローはoAuth2のブラウザ認証、インストール済みアプリで行ってます。
- 利用するGmailアカウントにて、oAuth2認証が必須: 対象のスコープはスクリプト内の`SCOPES`を参照してください
  - Gmail API
  - Google Sheet API
- config.pyが必要になります。詳しくはconfig_sample.pyを参照してください。
  - Googleスプレッドシートの差し込み用本文
- 送付用の情報を入れたGoogleスプレッドシート
  - スプレッドシートの権限は上で利用したGmailアカウントでもアクセス可能にしてください。
  - TODO: 2021/10/22 ここにサンプルのGoogleスプレッドシートを載せる


## 使い方

```python
# generate python venv
$ python -m venv .venv
# activate venv
# create config.py
# run script. first, authcentation oauth2
$ python multisendmail.py
```
