import requests
from bs4 import BeautifulSoup

# 設定
# amazonのBot対策回避のためのヘッダー設定
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9"
}

def get_price(URL: str):
    response = requests.get(URL, headers=HEADERS, timeout=10)

    # エラーチェック
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    
    # 価格を取得
    whole_price = soup.select_one("span.a-price-whole")
    fanction_price = soup.select_one("span.a-price-fraction")

    if whole_price and fanction_price and fanction_price.text.strip():
        price = int(whole_price.text.replace(',', '') + fanction_price.text.strip())
    elif whole_price:
        price = int(whole_price.text.replace(',', ''))
    elif fanction_price and fanction_price.text.strip():
        price = int(fanction_price.text.strip())
    else:
        print("価格が取得できませんでした")
        return None, None
    
    # ASINを取得
    asin = soup.select_one("#ASIN")
    if asin:
        asin = asin.get("value")
    else:
        print("ASINが取得できませんでした")
        return None

    return price, asin
    