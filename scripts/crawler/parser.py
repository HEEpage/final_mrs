from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import numpy as np
import math
import time
import traceback

# keyword 추출 모델
from static.preprocessing.extract_tag import main

def topidParser(response=None):

    id_list = list()

    soup = BeautifulSoup(response.page_source, 'html.parser')

    movie_url = soup.select("div.thumb > a")

    for m_url in movie_url:
        movie_id = m_url.get('href').split("=")[-1]
        id_list.append(movie_id)

    return id_list

# 개봉년도 별 영화 id parser
def idParser(response=None):
    id_list = list()
 
    while(True):
        soup = BeautifulSoup(response.page_source, 'html.parser')

        # 페이지 당 영화 목록 가져오기
        movie_list = soup.select("#old_content > ul.directory_list > li > a")

        # 페이지 당 영화 id 가져오기
        for movie in movie_list:
            movie_id = movie.get('href').split("=")[-1]
            id_list.append(movie_id)
        
        # 만약 다음 페이지가 있다면?
        btn_next = soup.select_one("#old_content > div.pagenavigation > table > tbody > tr > td.next > a")
        if btn_next is not None:
            response.find_element(
                By.CSS_SELECTOR,                                                            
                "#old_content > div.pagenavigation > table > tbody > tr > td.next > a"
            ).click()
            response.implicitly_wait(5)
        else:
            break

    return id_list


# 영화 정보 parser
def infoParser ( response=None ):
    try:

        # 영화 정보 soup
        info_soup = BeautifulSoup(response.page_source, 'html.parser')

        # director, running_time, genre, cast, release_date, ratings
        info_spec_title = info_soup.select('dl.info_spec > dt')
        info_spec_value = info_soup.select('dl.info_spec > dd')

        director = ""
        r_time = None
        genre = "미분류"
        actors = "정보없음"
        ratings = ""
        date = ""

        for idx, spec in enumerate(info_spec_title):
            
            if "개요" in spec.text:
                spans = info_spec_value[idx].select('p > span')
                for span in spans:
                    if span.select_one('a') is None:
                        r_time = int(span.text.replace("분",""))
                    else:
                        if "nation" in span.select_one('a').get('href'):
                            nations = span.select('a')
                            nation = "|".join([ n.text.strip() for n in nations ])
                            
                            # 대한민국 또는 미국 영화가 아니면 더이상 가져오지 않는다
                            if ("대한민국" not in nation and "미국" not in nation) or (nation is None):
                                return print( ">>> 대한민국 또는 미국 영화가 아닙니다. 더이상 데이터를 가져오지 않습니다.")

                        elif "open" in span.select_one('a').get('href'):
                            dates = span.select('a')[-2:]
                            date = "".join([ d.text.strip() for d in dates ]).replace(".","-")

                        elif "genre" in span.select_one('a').get('href'):
                            genres = span.select('a')[:]
                            genre = "|".join([ g.text.strip() for g in genres ])         
            
            elif "감독" in spec.text:
                if info_spec_value[idx].select_one('p > a') is None:
                    director = info_spec_value[idx].select_one('p').text.strip()
                else:
                    director = info_spec_value[idx].select_one('p > a').text.strip()

            elif "출연" in spec.text:
                actors = "|".join([actor.text.strip() for actor in info_spec_value[idx].select('p > a')])

            elif "등급" in spec.text:
                if "국내" in info_spec_value[idx].select_one('p').text.strip():
                    ratings = info_spec_value[idx].select_one('p > a').text.strip()


        # title, poster-----------------------------------------------------------------
        title = info_soup.select_one('div.mv_info_area > div.mv_info > h3 > a').text.strip()
        if info_soup.select_one('div.poster > a > img') is None:
            img_url = info_soup.select_one('div.poster > img').get('src').strip().split('?')[0]
        else :
            img_url = info_soup.select_one('div.poster > a > img').get('src').strip().split('?')[0]

        # synopsis ---------------------------------------------------------------------
        response.find_element(
            By.CSS_SELECTOR,
            "#movieEndTabMenu > li:nth-child(1) > a"
        ).click()
        response.implicitly_wait(3)

        story, s_keyword = storyParser(response)

        # review
        iframe = info_soup.select_one("#pointAfterListIframe")['src']
        address = "https://movie.naver.com" + iframe
        response.get(address)

        grade, viewer, reviews = reviewParser(address, response)

        movie_info = {
            "title" : title,
            "poster" : img_url,
            
            "director" : director,
            "cast" : actors,
            
            "genre" : genre,
            "nation" : nation,
            "running_time" : r_time,
            "release_date" : date,
            "ratings" : ratings,

            "avg_grade" : grade,
            "viewer" : viewer,
            
            "synopsis" : story,
            "keyword" : s_keyword,
        }

        return movie_info, reviews
    
    except Exception as e:
        return print(traceback.format_exc())




# 영화 시놉시스 parser
def storyParser(response=None):

    story_soup = BeautifulSoup(response.page_source, 'html.parser')
    check = story_soup.select_one("div.story_area")
    
    story = ""
    story_keyword = ""

    if check is not None:
        context = story_soup.select_one("div.story_area > p.con_tx").get_text(strip=True)

        if check.select_one("h5.h_tx_story") is not None:
            head = story_soup.select_one("h5.h_tx_story").get_text(strip=True)
            story = head + context
        else:
            story = context

        # 시놉시스 키워드
        story_keyword = "|".join(main(story))

    return story , story_keyword

# 영화 리뷰 parser
def reviewParser(address, response=None):
    
    frame_soup = BeautifulSoup(response.page_source, 'html.parser')
    reviews = []
    total_score = 0

    if frame_soup.select_one("div.no_score_info") is not None:
        avg_grade = 0
        viewer = 0
        return avg_grade, viewer, reviews
        
    else:
        # 만약 리뷰어 수가 만명이 넘는다면 20 페이지 가져오고
        # 리뷰어 수가 만명이 넘지 않는다면 10 페이지 가져와보자

        # 리뷰어 수
        cnt = int(frame_soup.select_one("body > div > div > div.score_total > strong > em").text.replace(",",""))

        pages = math.ceil(cnt / 10)

        if  cnt <= 10000:
            for page in range(pages if pages < 10 else 10):
                
                response.get(f"{address}&page={page+1}")
                data_soup = BeautifulSoup(response.page_source, 'html.parser')

                lines = data_soup.select("body > div > div > div.score_result > ul > li")

                for idx, line in enumerate(lines):
                    # 평점
                    grade = float(line.select_one("div.star_score > em").get_text(strip=True))
                    total_score += grade

                    # 리뷰 글
                    ment = f"#_filtered_ment_{idx}"
                    # ment가 길다면...
                    unfold_ment = f"#_unfold_ment{idx} > a"

                    if line.select_one(unfold_ment) is None:
                        review = line.select_one(ment).get_text(strip=True)
                    else:
                        review = line.select_one(unfold_ment)['data-src']

                    # 리뷰 등록 일자
                    c_date = line.select_one("div.score_reple > dl > dt > em:nth-child(2)").get_text(strip=True).replace(".","-")

                    reviews.append([grade, review, c_date])
                    

        elif cnt > 10000 :
            for page in range(20):
                response.get(f"{address}&page={page+1}")
                data_soup = BeautifulSoup(response.page_source, 'html.parser')

                lines = data_soup.select("body > div > div > div.score_result > ul > li")

                for idx, line in enumerate(lines):
                    # 평점
                    grade = float(line.select_one("div.star_score > em").get_text(strip=True))
                    total_score += grade
                    # 리뷰 글
                    ment = f"#_filtered_ment_{idx}"
                    # ment가 길다면...
                    unfold_ment = f"#_unfold_ment{idx} > a"

                    if line.select_one(unfold_ment) is None:
                        review = line.select_one(ment).get_text(strip=True)
                    else:
                        review = line.select_one(unfold_ment)['data-src']

                    # 리뷰 등록 일자
                    c_date = line.select_one("div.score_reple > dl > dt > em:nth-child(2)").get_text(strip=True).replace(".","-")
                    
                    reviews.append([grade, review, c_date])

        viewer = len(reviews)

        if viewer == 0:
            avg_grade = 0
        else:
            avg_grade = round(total_score / viewer, 1)

        return avg_grade, viewer, reviews


def ottParser(m_title, m_director, response=None):
    
    netflix = 0
    watcha = 0
    tving = 0
    wavve = 0
    netflix_url = ""
    watcha_url = ""
    tving_url = ""
    wavve_url = ""


    #검색어 입력칸
    response.find_element(
        By.CSS_SELECTOR,
        "#root > div > div.css-1xm32e0 > header.css-6k8tqb > nav > div > div > ul > li.css-1c3wwgb > div > div > form > label > input"
    ).send_keys(f"{m_title} {m_director}")
    time.sleep(3)

    #검색어 입력칸
    response.find_element(
        By.NAME,
        "searchKeyword"
    ).send_keys(Keys.ENTER)
    time.sleep(3)
    

    soup = BeautifulSoup(response.page_source, 'html.parser')
    tag = "#root > div > div.css-1xm32e0 > section > section > div.css-ipmqep-StyledTabContentContainer.e1szkzar3 > div.css-12hxjcc-StyledHideableBlock.e1pww8ij0 > section > section.css-1s4ow07 > div > div.css-9dnzub > div > ul > li:nth-child(1) > a"

    if soup.select(tag) != []:
        path = soup.select_one(tag)['href']
        response.get("https://pedia.watcha.com" + path)

        movie_soup = BeautifulSoup(response.page_source, 'html.parser')

        watch_tag = "#root > div > div.css-1xm32e0 > section > div > div.css-10ofaaw > div > div > div > div:nth-child(1) > div.css-wpsvu8 > div.css-1nhig6u-RoundedCornerBlock-RoundedCornerBlock > div > section.w_exposed_cell.css-1impywp > div:nth-child(1) > div > header > h2"
        if movie_soup.select_one(watch_tag) is not None:
            view_tag = "#root > div > div.css-1xm32e0 > section > div > div.css-10ofaaw > div > div > div > div:nth-child(1) > div.css-uvsgck > div > div > section.w_exposed_cell.css-l1ynz5 > div.css-usdi1z > div.css-9dnzub > div > div > div > ul > li > a"
            view = soup.select(view_tag)

            for t in view:
                if t['title'] == "넷플릭스":
                    netflix = 1
                    netflix_url = t['href']
                elif t["title"] == "왓챠":
                    watcha = 1
                    watcha_url = t['href']
                elif t["title"] == "티빙":
                    tving = 1
                    tving_url = t["href"]
                elif t["title"] == "웨이브":
                    wavve = 1
                    wavve_url = t["href"]

    return {
        "netflix" : netflix,
        "watcha" : watcha,
        "tving" : tving,
        "wavve" : wavve,
        "netflix_url" : netflix_url,
        "watcha_url" : watcha_url,
        "tving_url" : tving_url,
        "wavve_url" : wavve_url,
    }

def theaterParser(response=None):

    theater_soup = BeautifulSoup(response.page_source, 'html.parser')

    theaters = theater_soup.select("#runningLayer > li > div > p > strong")

    theater_list = { "CGV" : 0, "롯데시네마" : 0, "메가박스" : 0 }
    for theater in theaters :
        t = theater.text.split(" ")[0]

        if t in theater_list.keys():
            if theater_list[t] == 0:
                theater_list[t] = 1

    return {
        "cgv" : theater_list["CGV"],
        "lotte" : theater_list["롯데시네마"],
        "megabox" : theater_list["메가박스"],
    }


def top10Parser(category, response=None):
    id_list = list()
    if category == "upcoming":
        time.sleep(8)
        soup = BeautifulSoup(response.page_source, 'html.parser')

        # movie 정보 url 가져오기
        movies = soup.select("#flick2 > li")

        upcoming_idx = 0 # '개봉 예정작' 테이블의 pk 값

        for movie in movies:
            movie_id = movie.get('data-id')
            id_list.append(movie_id)
            upcoming_idx += 1
    
    elif category == "boxoffice":
        time.sleep(3)
        soup = BeautifulSoup(response.page_source, 'html.parser')

        # movie 정보 url 가져오기
        movies = soup.select("#flick0 > li")

        boxoffice_idx = 0 # '현재 상영작' 테이블의 pk 값

        for movie in movies:
            movie_id = movie.get('data-id')
            id_list.append(movie_id)
            boxoffice_idx += 1

    return id_list

