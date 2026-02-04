import requests
from bs4 import BeautifulSoup
import json
import os
import warnings
from datetime import datetime

# SSL 경고 비활성화
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def crawl():
    print("--- 환율 업데이트 시작 ---")
    
    # 데이터 소스 URL
    url = "https://finance.naver.com/marketindex/exchangeList.naver"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    try:
        # verify=False로 접속 안정성 확보
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.encoding = 'euc-kr'
        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.select('table.tbl_exchange tbody tr')
        
        usd = ""
        jpy = ""

        for row in rows:
            title_tag = row.select_one('td.tit a')
            if not title_tag:
                continue
                
            name = title_tag.text.strip()
            price = row.select_one('td.sale').text.replace(',', '').strip()

            if "미국 USD" in name:
                usd = price
            elif "일본 JPY" in name:
                jpy = price

        if usd and jpy:
            data = {
                "usd": usd,
                "jpy": jpy,
                "time": datetime.now().strftime('%Y.%m.%d %H:%M')
            }
            
            # [수정] 파일 저장 경로를 절대 경로로 지정하여 GitHub Actions 에러 방지
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, 'exchange.json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            print(f"✅ 업데이트 성공: USD {usd}, JPY {jpy}")
        else:
            print("❌ 데이터를 찾지 못했습니다.")
            exit(1)

    except Exception as e:
        print(f"🔥 에러 발생: {e}")
        exit(1)

if __name__ == "__main__":
    crawl()
