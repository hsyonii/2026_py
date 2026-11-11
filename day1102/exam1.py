# 크롤링 : 웹페이지에 존재하는 데이터들을 수집하는 기술
# 크롤링 라이브러리 : 정적 - BeautifulSoup, request / 동적 - Seleium, Playwright
# *크롤링 전 확인
#   1. 크롤링 가능여부 확인 : 크롤링할 페이지 도메인주소 + /robots.txt
#   2. 개발자 도구 -> 크롤링 요소 선택하여 선택자or식별자 확인

# 정적
# ex ) 네이버 검색 정보 크롤링
# step 1. 크롤링할 주소 가져오기( 파라미터 정리 후 )
url = "http://search.naver.com/search.naver?&query=안양날씨"
# step 2. requests 라이브러리로 해당 주소 요청
import requests
re = requests.get(url) # requests.get(주소)
print(reponse) # <Response [200]> # HTTP CODE : 200 -> 통신 정상
# step 3. 요청한 페이지의 HTML 파싱
from bs4 import BeautifulSoup
# BeautifulSoup( response.text, "html.parser")
soup = BeautifulSoup( re.text, "html.parser")
print(soup)

# step 4. 특정한 식별자(마크업)의 텍스트 or 정보 추출
# soup.select(식별자), soup.select_one() : 식별자 여러개, 한개 정보 추출 
text = soup.select_one(".temperature_text")
print(text)
# step 5. 마크업 사이의 텍스트 추출
# text.get_text() : text에서 텍스트만 추출
print(text.get_text())

