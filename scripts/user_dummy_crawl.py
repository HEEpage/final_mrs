from scripts.crawler import SeleniumRequest
from scripts.crawler.user_parser import userLogParser
import numpy as np
import json

def run():
    
    # 크롤링 객체 생성
    # np.load 하는 부분이랑 json 파일로 저장하는 부분 숫자 바꿔주고 돌려주쎄용!

    request = SeleniumRequest()

    totalList = np.load('./static/data/user_list_0.npy', allow_pickle=True)

    u_url = "https://pedia.watcha.com/ko-KR/users/djaxb44zMvLw8/contents/movies"
    userLog = request.get(u_url, totalList.tolist(), callback=userLogParser)

    # 저장하기
    with open(f'./static/data/user_log_data_0.json', 'w', encoding="utf-8") as f:
        json.dump(userLog, f, ensure_ascii=False, indent=4)
