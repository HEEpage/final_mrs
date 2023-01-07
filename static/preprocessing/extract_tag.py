import pandas as pd
import numpy as np
import re
import os
from konlpy.tag import Okt
import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

def textPreprocessor(review):

    #특수문자 제거
    pattern = r'\([^)]*\)'  # ()&()안 문자 제거
    review = re.sub(pattern=pattern, repl='', string=review)

    pattern = r'\[[^)]*\]'  # []&[]안 문자 제거
    review = re.sub(pattern=pattern, repl='', string=review)

    pattern = r'\<[^)]*\>'  # <>&<>안 문자 제거
    review = re.sub(pattern=pattern, repl='', string=review)

    pattern = r'\{[^)]*\}'  # {}&{}안 문자 제거
    review = re.sub(pattern=pattern, repl='', string=review)

    pattern ="[‘](.*?)[’]"
    review = re.sub(pattern=pattern, repl='', string= review )

    pattern ="[“](.*?)[”]"
    review = re.sub(pattern=pattern, repl='', string= review )

    pattern = "[\'](.*?)[\']" 
    review = re.sub(pattern=pattern, repl='', string= review )

    pattern = "[\"](.*?)[\"]"  
    review = re.sub(pattern=pattern, repl='', string= review )
    
    review =re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z ]','',review)
    return review

def findNoun(review):
    okt = Okt()
    STOP_WORDS = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍',
    '갑자기', '과', '도', '을', '를', '으로', '자', '에', '와', '한',
    '하다', '에서', '로', '하고', '위해', '지금껏', '여느']

    tmp = []
    for j in range(len(okt.pos(review))):
        text,tag = okt.pos(review)[j]
        if tag.startswith("N") and (text not in STOP_WORDS) and len(text) > 1:
            tmp.append(text)
    return tmp

def main(input):
    data = findNoun(textPreprocessor(input))
    text_lst = nltk.Text(data).vocab().most_common(5)
    return list(dict(text_lst).keys())

