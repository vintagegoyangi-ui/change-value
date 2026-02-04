import requests
from bs4 import BeautifulSoup
import json
import os
import warnings
from datetime import datetime

# [참고] final.py의 SSL 경고 비활성화 적용
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def crawl():
    # 환율 메인 페이지
    url = "https://finance.naver.com/marketindex/"
    
    # [참고] final.py에서 사용 중인 안정적인 HEADERS 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # verify=False를 추가하여 SSL 인증서 오류로 인한 차단을 방지합니다.
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.encoding = 'euc-kr'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 태그를 찾을 때 좀 더 범용적인 클래스명을 사용합니다.
        usd_tag = soup.select_one(".usd .value")
        jpy_tag = soup.select_one(".jpy_100 .value")
        date_tag = soup.select_one(".date")

        if not usd_tag or not jpy_tag:
            # 첫 번째 시도가 실패할 경우, 다른 영역(#exchangeList)에서 다시 시도합니다.
            usd_tag = soup.select_one("#exchangeList .usd .value")
            jpy_tag = soup.select_one("#exchangeList .jpy_100 .value")

        if not usd_tag:
            raise Exception("데이터 추출 실패: 네이버 페이지에서 환율 태그를 찾을 수 없습니다.")

        usd = usd_tag.text.replace(',', '')
        jpy = jpy_tag.text.replace(',', '')
        date_text = date_tag.text.strip() if date_tag else datetime.now().strftime('%Y.%m.%d %H:%M')
        
        data = {
            "usd": usd,
            "jpy": jpy,
            "time": date_text
        }
        
        # 파일 저장 경로 (레포지토리 루트)
        file_path = os.path.join(os.path.dirname(__file__), 'exchange.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"성공적으로 데이터를 저장했습니다: {data}")
        
    except Exception as e:
        print(f"크롤링 중 에러 발생: {e}")
        exit(1)

if __name__ == "__main__":
    crawl()
