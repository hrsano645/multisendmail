# 差し込みするためのGoogleスプレッドシートIDを入れてください。アクセスはoAuth2認証をしたアカウントでアクセス可能にすること
# SPREADSHEET_ID = ""

# シート名と列を指定してください
# RANGE_NAME = "シート1!A:E"

# SASHICOMI_BODYはメール本文のことです。複数行向け文字列を使います
# 差し込み用にformatメソッドを通しています。{}にはシートの見出し名を入れること。日本語は不可能なので注意

# SASHICOMI_BODY = """
# 差し込みテスト
# """

# 列の上部にある見出しを使う場合
# SASHICOMI_BODY = """
# 差し込みテスト
# id: {id}
# title: {title}
# """

# メール送付用情報です
# 送信元のメールアドレス
# sendmail_from = ""
# 送信時のメールタイトル
# sendmail_subject = ""
# 送信時のCC指定（リストで複数指定）
# sendmail_cc_addrs = [""]
