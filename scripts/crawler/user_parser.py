from bs4 import BeautifulSoup
import time
from movies.models import Movie

def userParser(response=None):
    userList = list()

    # 스크롤 높이 가져옴
    last_height = response.execute_script("return document.body.scrollHeight")
    while(True):
        response.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

        soup = BeautifulSoup(response.page_source, 'html.parser')
        tag = "#root > div > div.css-1xm32e0 > section > section > div > div > div > ul > div > div.css-4obf01 > div.css-1cvf9dk > a"
        users_url = soup.select(tag)
        print(len(users_url))
        
        if len(users_url) >= 80:
            
            for url in users_url:
                userList.append((url['title'],url['href']))

            break
            
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = response.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    return userList

def userLogParser( userList , response=None ):

    userLog = {}

    # user 정보 가져오깅
    for name, user_url in userList:
        
        userlogList = []

        response.get("https://pedia.watcha.com" + user_url + "/contents/movies")
        soup = BeautifulSoup(response.page_source, 'html.parser')
        tag = " #root > div > div.css-1xm32e0 > section > section > section > div:nth-child(1) > div > header > span"
        print(soup.select_one(tag))
        m_cnt = soup.select_one(tag).text
        print("영화 평가 개수 >>>>> ", m_cnt)


        response.get("https://pedia.watcha.com" + user_url + "/contents/movies/ratings")

        # 스크롤 높이 가져옴
        last_height = response.execute_script("return document.body.scrollHeight")

        while(True):
            response.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            soup = BeautifulSoup(response.page_source, 'html.parser')
            tag = "#root > div > div.css-1xm32e0 > section > section > div.css-12hxjcc-StyledHideableBlock.e1pww8ij0 > section > div.css-1gkas1x-Grid.e1689zdh0 > div > ul > li > a > div.css-ixy093"
            infomations = soup.select(tag)
            print(len(infomations))
            
            if len(infomations) >= int(m_cnt):
                
                for info in infomations:

                    title = info.select_one("div.css-niy0za").text
                    grade = info.select_one("div.css-m9i0qw").text.split("★")[-1].strip()

                    # 저장된 영화에 있는지 확인하고 user log 저장
                    if Movie.objects.filter(title__contains = title).count()==1:
                        print(">>>>>>>>>>>>>>>", title)
                        movie_id = Movie.objects.get(title__contains=title).id
                        userlogList.append({ "movie_id" : movie_id, "grade" : float(grade) * 2})
                
                userLog[name.split(" ")[0]] = userlogList
                break
            
            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = response.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    return userLog