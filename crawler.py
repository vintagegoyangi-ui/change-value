import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_exchange_rate():
    url = "https://finance.naver.com/marketindex/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # USD와 JPY 데이터 추출
        usd = soup.select_one(".head.usd .value").text
        jpy = soup.select_one(".head.jpy_100 .value").text

        data = {
            "usd": usd,
            "jpy": jpy,
            "time": soup.select_one(".date").text.strip()
        }

        # 결과 저장
        with open('exchange.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("환율 데이터 업데이트 완료")
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    fetch_exchange_rate()
