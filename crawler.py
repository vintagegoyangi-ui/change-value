import requests
from bs4 import BeautifulSoup
import json
import os

def crawl():
    url = "https://finance.naver.com/marketindex/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        usd = soup.select_one(".head.usd .value").text
        jpy = soup.select_one(".head.jpy_100 .value").text
        
        data = {
            "usd": usd,
            "jpy": jpy,
            "time": requests.utils.quote(soup.select_one(".date").text) # 시간 정보 추가
        }
        
        # 파일 저장 경로를 현재 스크립트 위치로 명시
        file_path = os.path.join(os.path.dirname(__file__), 'exchange.json')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("파일 생성 완료:", data)
        
    except Exception as e:
        print("크롤링 중 에러 발생:", e)
        exit(1) # 에러 발생 시 프로세스 종료해서 Actions에 알림

if __name__ == "__main__":
    crawl()
