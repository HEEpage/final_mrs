import pandas as pd
import numpy as np
import re
from konlpy.tag import Okt
import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

########### 이렇게 해도 되는건가...? ##############
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
#################################################


def text_preprocessor(review):

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

def find_N(review):
    okt = Okt()
    STOP_WORDS = ['의','가','이','은','들','는','좀','잘','걍','갑자기','과','도','을','를','으로','자','에','와','한','하다','에서','로','하고','위해']

    tmp = []
    for j in range(   len(  okt.pos( review )) ):
        text,tag = okt.pos( review )[j]
        if tag.startswith("N") and (text not in STOP_WORDS) and len(text)>1:
            tmp.append(text)
    return tmp

# def main(input):
def main(input):
    # 강제 자바 홈 path 설정해주기 (trouble shooting) 
    import os
    os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-11.0.17\bin\server'
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",'JAVA_HOME' in os.environ)
    
    for i in range(len(input)):
        # input[i]["review"] = text_preprocessor(input[i]["review"])
        input["review"] = text_preprocessor(input["review"])

    data = pd.DataFrame(input)
    data['review'] = data['review'].apply(lambda s: find_N(s))

    text_lst = []
    # for i in range(len(data.review)):
    #     text = nltk.Text(data.review.iloc[i])
    #     text_lst.append(text.vocab().most_common(10))

    text_lst = [ text.vocab().most_common(10) for text in nltk.Text(data.review)   ]

    return dict(text_lst).keys()
    # return dict(text_lst[0]).keys()

