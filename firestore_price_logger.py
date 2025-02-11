import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# 環境変数からfirebaseの認証情報のパスを取得
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_API_KEY_PATH")
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

# firestore初期化処理
db = firestore.client()

def save_price_to_firestore(price: int, product_id: str, user_id: str):

    # 価格が取得できなかった場合は保存しない
    if not price:
        print("価格が取得できなかったため、保存しません")
        return

    # 現在時刻を取得
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "user_id": user_id,
        "product_id": product_id,
        "price": price,
        "created_at": now_str
    }   
    
    doc_id = f"{user_id}_{product_id}_{now_str}"
    # firestoreに保存
    db.collection("products").document(doc_id).set(data)
    
    print(f"保存しました: {data}")
