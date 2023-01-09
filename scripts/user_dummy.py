from scripts.crawler import SeleniumRequest
from scripts.crawler.user_parser import userParser

def run():
    
    # 크롤링 객체 생성
    request = SeleniumRequest()

    # user dummy crawling
    url = "https://pedia.watcha.com/ko-KR/contents/mOk7BJO/comments"
    request.get(url, callback=userParser)

