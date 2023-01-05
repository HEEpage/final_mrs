# 현재 상영하는 영화 scrap

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import json
import time
import traceback

import os
from urllib.request import urlretrieve
from PIL import Image

def run() :

    #크롬 옵션 객체 생성
    options = webdriver.ChromeOptions()
    options.add_argument("--start-fullscreen") # 전체화면으로 실행
    # options.add_argument("--headless") # 브라우저 창 없이 실행


    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()),
        options = options
    )

    movie_id = 127398
    driver.get(f"https://movie.naver.com/movie/bi/mi/point.naver?code={movie_id}")


    # 영화 정보 soup
    info_soup = BeautifulSoup(driver.page_source, 'html.parser')


    # 감독, 출연 배우, 관람 등급
    info_spec_title = info_soup.select('dl.info_spec > dt')
    info_spec_value = info_soup.select('dl.info_spec > dd')

    director = None
    r_time = None
    genre = "미분류"
    country = None
    actors = "정보없음"
    ratings = None
    date = None

    for idx, spec in enumerate(info_spec_title):
        if "감독" in spec.text:
            if info_spec_value[idx].select_one('p > a') is None:
                director = info_spec_value[idx].select_one('p').text.strip()
            else:
                director = info_spec_value[idx].select_one('p > a').text.strip()

        elif "출연" in spec.text:
            actors = ",".join([actor.text.strip() for actor in info_spec_value[idx].select('p > a')])

        elif "등급" in spec.text:
            if "국내" in info_spec_value[idx].select_one('p').text.strip():
                ratings = info_spec_value[idx].select_one('p > a').text.strip()

        elif "개요" in spec.text:
            spans = info_spec_value[idx].select('p > span')
            for span in spans:
                if span.select_one('a') is None:
                    r_time = int(span.text.replace("분",""))
                else:
                    if "nation" in span.select_one('a').get('href'):
                        countries = span.select('a')
                        country = ",".join([ c.text.strip() for c in countries ])
                        
                    elif "open" in span.select_one('a').get('href'):
                        dates = span.select('a')[-2:]
                        date = "".join([ d.text.strip() for d in dates ]).replace(".","-")

                    elif "genre" in span.select_one('a').get('href'):
                        genres = span.select('a')[:]
                        genre = ",".join([ g.text.strip() for g in genres ])


    #평점 / 평점 준 사람 수 / 추천 나이 / 추천 성별
    main_score = info_soup.select_one('div.main_score')
    recommend_info = info_soup.select_one("strong.grp_review")

    grade = None
    viewer = None
    recommend_age = None
    recommend_gender = None

    if main_score is not None:
        grade_info = info_soup.select_one("div.sc_area")
        grades = grade_info.select("div.star_score > em")
        grade = float("".join([g.text.strip() for g in grades]))

        viewer = int(grade_info.select_one('span.user_count > em').text.replace(",","").strip())
        
        if recommend_info is not None:
            recommend = recommend_info.select_one('em').text.split("대")
            recommend_age = int(recommend[0].strip())
            recommend_gender = 1 if recommend[1].strip() == "여성" else 0



    #영화 정보 + 포스터 url
    title = info_soup.select_one('div.mv_info_area > div.mv_info > h3 > a').text.strip()
    if info_soup.select_one('div.poster > a > img') is None:
        img_url = info_soup.select_one('div.poster > img').get('src').strip().split('?')[0]
    else :
        img_url = info_soup.select_one('div.poster > a > img').get('src').strip().split('?')[0]


    #시놉시스
    story = None
    driver.find_element(
        By.CSS_SELECTOR,                                                            
        "#movieEndTabMenu > li:nth-child(1) > a"
    ).click()

    driver.implicitly_wait(3)

    story_soup = BeautifulSoup(driver.page_source, 'html.parser')
    check = story_soup.select_one("div.story_area")

    if check is not None:
        context = story_soup.select_one("div.story_area > p.con_tx").get_text(strip=True)
        # print(context)
        if check.select_one("h5.h_tx_story") is not None:
            head = story_soup.select_one("h5.h_tx_story").get_text(strip=True)
            story = head + context
        else:
            story = context

    # -------------- IMAGE DOWNLOAD TEST --------------------

    # 스크랩 시작 전(for문 전)에 작성

    # 이미지 저장할 폴더 경로 
    img_folder_path = 'C:/final_project/final_mrs/static/imgs'

    # -------------------------------------------------------

    # img_url 가져오고 나서 작성

    # 폴더가 없으면 새로 생성
    if not os.path.isdir(img_folder_path) :
        os.mkdir(img_folder_path)

    img_path = './static/imgs/{}{}'.format(movie_id, '.png')

    urlretrieve(img_url, img_path)

    image = Image.open(img_path)
    image = image.resize((450,600))
    image.save(img_path)

    # ------------------------------------------------------

    print("===================================")

    print("제목 : ", title)
    print("포스터 : ", img_path)
    print("개봉일 : ", date)
    print("장르 : ", genre)
    print("제작국가 : ", country)
    print("감독 : ", director)
    print("출연진 : ", actors)
    print("상영시간 : ", r_time)
    print("관람등급 : ", ratings)
    print("평점 : ", grade)
    print("평점 참여자 수 : ", viewer)
    print("시놉시스 : ", story)

    print("===================================")

    # recommend_age,recommend_gender

    driver.quit()