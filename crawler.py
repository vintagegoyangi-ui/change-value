import requests
from bs4 import BeautifulSoup
import json
import os
import warnings
import re
from datetime import datetime

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def crawl():
    print("--- 크롤링 시작 ---")
    # 환율 정보를 직접 담고 있는 테이블 페이지로 주소를 변경해 더 안정적으로 가져옵니다.
    url = "https://finance.naver.com/marketindex/exchangeList.naver"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://finance.naver.com/marketindex/'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.encoding = 'euc-kr'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 모든 행(tr)을 가져와서 통화명을 찾습니다.
        rows = soup.select("table.tbl_exchange tbody tr")
        
        usd = ""
        jpy = ""

        for row in rows:
            symbol = row.select_one(".tit a")
            if symbol:
                name = symbol.text.strip()
                # 매매기준율(sale) 클래스의 값을 가져옵니다.
                value = row.select_one(".sale").text.replace(',', '').strip()
                
                if "미국 USD" in name:
                    usd = value
                elif "일본 JPY" in name:
                    jpy = value

        if not usd or not jpy:
            print("데이터 추출 실패! HTML 구조를 분석합니다...")
            # 디버깅용: 테이블이 비어있는지 확인
            print(f"찾은 행 개수: {len(rows)}")
            return

        data = {
            "usd": usd,
            "jpy": jpy,
            "time": datetime.now().strftime('%Y.%m.%d %H:%M')
        }

        print(f"추출 성공: {data}")

        # 파일 저장
        file_path = os.path.join(os.getcwd(), 'exchange.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"파일 저장 완료: {file_path}")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    crawl()
