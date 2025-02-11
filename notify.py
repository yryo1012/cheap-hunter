import requests
import os

# 環境変数からLIMEのトークンを取得
LIME_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# LIME通知用の関数
def send_lime_notify(message: str):
    if not LIME_TOKEN or not LINE_USER_ID:
        print("LINE_CHANNEL_ACCESS_TOKENが設定されていません")
        return
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LIME_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": LINE_USER_ID,
        "message": message
    }

    response = requests.post(url, headers=headers, data=data)

    # エラーチェック
    response.raise_for_status()

    print("LINEに通知しました")

def send_notify(tool="line", asin=None, olePrice=None, newPrice=None):
    if tool == "line":
        send_lime_notify("通知テスト")
    else:
        print("未対応の通知ツールです")