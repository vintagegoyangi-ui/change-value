import requests
from bs4 import BeautifulSoup
import json
import os

def crawl():
    url = "https://finance.naver.com/marketindex/"
    
    # [수정] 네이버가 크롤러를 차단하지 못하도록 브라우저 정보를 보냅니다.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # [수정] 태그 선택자를 더 정확하게 지정합니다.
        usd_tag = soup.select_one(".head.usd .value")
        jpy_tag = soup.select_one(".head.jpy_100 .value")
        date_tag = soup.select_one(".date")

        if not usd_tag or not jpy_tag:
            raise Exception("환율 데이터를 찾을 수 없습니다. 네이버 페이지 구조가 변경되었을 수 있습니다.")

        usd = usd_tag.text
        jpy = jpy_tag.text
        date_text = date_tag.text if date_tag else "시간 정보 없음"
        
        data = {
            "usd": usd,
            "jpy": jpy,
            "time": date_text.strip()
        }
        
        # 파일 저장
        file_path = os.path.join(os.path.dirname(__file__), 'exchange.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"파일 생성 완료: USD {usd}, JPY {jpy}")
        
    except Exception as e:
        print(f"크롤링 중 에러 발생: {e}")
        exit(1)

if __name__ == "__main__":
    crawl()
