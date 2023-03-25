from scripts.crawler import SeleniumRequest
from scripts.crawler.user_parser import userParser, userLogParser
import numpy as np
import json, os


def run():

    # 크롤링 객체 생성
    request = SeleniumRequest()
    urls = [
        "https://pedia.watcha.com/ko-KR/contents/mOk7BJO/comments",
        "https://pedia.watcha.com/ko-KR/contents/mdRE38b/comments",
        "https://pedia.watcha.com/ko-KR/contents/m5X3Rgd/comments",
        "https://pedia.watcha.com/ko-KR/contents/m5agQGD/comments",
        "https://pedia.watcha.com/ko-KR/contents/mY5QVRW/comments",
        "https://pedia.watcha.com/ko-KR/contents/mdMgLx2/comments",
        "https://pedia.watcha.com/ko-KR/contents/mWJjpQW/comments",
        "https://pedia.watcha.com/ko-KR/contents/m5rQwBD/comments",
        "https://pedia.watcha.com/ko-KR/contents/mdMBlkR/comments",
        "https://pedia.watcha.com/ko-KR/contents/mOgjx80/comments"
    ]
    
    # user dummy crawling ---------------------------------------------------------------
    totalList = []

    for url in urls:
        userList = request.get(url, callback=userParser)
        print(userList)
        totalList += userList

    totalList = list(set(totalList))
    print(len(totalList))

    # name, url 저장
    np.save('./static/data/user_list.npy', totalList)


    # 10개씩 나누어 저장
    userList = [totalList[i: i + 10] for i in range(0, len(totalList), 10)]
    for i in range(len(userList)):
        np.save(f'./static/user_data/user_list_{i}.npy', userList[i])

    
    # 유저 영화 기록 크롤링 ----------------------------------------------------------------
    request = SeleniumRequest()

    for i in range(31, 36):

        totalList = np.load(f'./static/user_data/user_list_{i}.npy', allow_pickle=True)

        u_url = "https://pedia.watcha.com/ko-KR/users/djaxb44zMvLw8/contents/movies"
        userLog = request.get(u_url, totalList.tolist(), callback=userLogParser)

        # 저장하기
        with open(f'./static/data/user_log_data_{i}.json', 'w', encoding="utf-8") as f:
            json.dump(userLog, f, ensure_ascii=False, indent=4)
