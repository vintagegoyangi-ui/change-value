import requests
from bs4 import BeautifulSoup
import urllib3

# SSL 인증서 경고 메시지 무시하기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_naver_weather(city_name):
    url = f"https://search.naver.com/search.naver?query={city_name}+날씨"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # verify=False 를 추가하여 SSL 검증을 건너뜁니다.
        res = requests.get(url, headers=headers, verify=False)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        curr_temp = "정보없음"
        curr_status = "정보없음"
        
        # 1. 현재 날씨 추출 (국내/해외 분기 처리)
        if soup.select_one(".temperature_text"):
            temp_tag = soup.select_one(".temperature_text strong")
            if temp_tag:
                # 숫자와 소수점만 남기기
                curr_temp = "".join(c for c in temp_tag.get_text(strip=True) if c.isdigit() or c == '.')
            
            status_tag = soup.select_one(".temperature_info .weather.before_slash")
            if status_tag:
                curr_status = status_tag.get_text(strip=True)
                
        elif soup.select_one(".summary_area"):
            temp_tag = soup.select_one(".summary_area .current")
            if temp_tag:
                curr_temp = temp_tag.get_text(strip=True).replace("°", "")
            
            status_tag = soup.select_one(".summary_area .weather")
            if status_tag:
                curr_status = status_tag.get_text(strip=True)

        # 2. 주간 날씨 추출
        # 국내/해외 공통적으로 주간 리스트를 담는 클래스들을 체크합니다.
        weekly_items = soup.select(".list_date_after .item_date") or soup.select(".week_list .menu_item") or soup.select(".week_item")
        weekly_count = len(weekly_items)

        print(f"✅ {city_name} 완료: {curr_temp}도 | {curr_status} | 주간데이터 {weekly_count}건")

    except Exception as e:
        print(f"❌ {city_name} 에러 발생: {e}")

if __name__ == "__main__":
    print("--- 네이버 날씨 최종 크롤링 시작 (SSL 검증 우회 버전) ---")
    target_cities = ["서울", "부산", "도쿄", "오사카", "후쿠오카"]
    
    for city in target_cities:
        get_naver_weather(city)
