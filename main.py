from price_checker import get_price
from firestore_price_logger import save_price_to_firestore
from fetch_from_firestore import fetch_latest_price
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

# .envファイルから環境変数を読み込む
load_dotenv()
# (仮)
LINE_USER_ID = os.getenv("LINE_USER_ID")
# 環境変数からfirebaseの認証情報のパスを取得
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_API_KEY_PATH")
# とりあえず適当なページ
URL = "https://www.amazon.co.jp/dp/B0BNL5ZTLX/?coliid=I112RMLGB3NOHK&colid=1G2LE02S482SL&psc=0&ref_=list_c_wl_lv_ov_lig_dp_it"

def initialize_firestore():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)

def createMessage(oldPrice, newPrice):
    message = f"価格が変更されました！\n\n"
    message += f"変更前の価格: {oldPrice}円\n"
    message += f"変更後の価格: {newPrice}円"
    return message

def main():
    initialize_firestore()
    newPrice, asin = get_price(URL)
    # 価格とASIN両方取得できた場合のみ保存
    if newPrice and asin:
        print(f"価格: {newPrice}円, ASIN: {asin}")
        save_price_to_firestore(newPrice, asin, LINE_USER_ID)
        oldPrice = fetch_latest_price(LINE_USER_ID, asin)
        if oldPrice is None:
            print("No matching document found.")
            return
        else:
            print(f"The latest price is: {oldPrice}")
            
    else:
        print("価格またはasinが取得できませませんでした")
        return

if __name__ == "__main__":
    main()