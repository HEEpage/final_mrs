from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import numpy as np
import math
import time
import traceback


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
        
        if len(users_url) >= 10:
            
            for url in users_url:
                userList.append((url['title'],url['href']))

            break
            
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = response.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

   
    # user 정보 가져오깅
    for name, user_url in userList:

        response.get("https://pedia.watcha.com" + user_url + "/contents/movies")
        soup = BeautifulSoup(response.page_source, 'html.parser')
        tag = " #root > div > div.css-1xm32e0 > section > section > section > div:nth-child(1) > div > header > span"
        print(soup.select_one(tag))
        m_cnt = soup.select_one(tag).text
        print("영화 평가 개수 >>>>> ",m_cnt)


        response.get("https://pedia.watcha.com" + user_url + "/contents/movies/ratings")

        # 스크롤 높이 가져옴
        last_height = response.execute_script("return document.body.scrollHeight")

        while(True):
            response.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            soup = BeautifulSoup(response.page_source, 'html.parser')
            tag = "#root > div > div.css-1xm32e0 > section > section > div.css-12hxjcc-StyledHideableBlock.e1pww8ij0 > section > div.css-1gkas1x-Grid.e1689zdh0 > div > ul > li > a > div.css-ixy093"
            infomations = soup.select(tag)
            print(len(infomations))
            
            if len(infomations) >= 10:
                
                for info in infomations:

                    title = info.select_one("div.css-niy0za").text
                    grade = info.select_one("div.css-m9i0qw").text.split("★")[-1].strip()

                    print(name.split(" ")[0], title, grade)

                break
                
            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = response.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
