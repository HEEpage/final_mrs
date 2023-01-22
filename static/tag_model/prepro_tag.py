from keybert import KeyBERT
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from os import path
import re

STOP_WORDS = ['이', '가', '께', '께서', '에서', '을', '를', '고', '의', '와', '과', '랑', '며', '에', '은', '는', '만', '도', '까지', '조차', '들', '으로', '한', '하다', '으', '에게', '하']

def sub_special(s):
    return re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z ]','',s)

def kbert(df, title):

    array_text = pd.DataFrame([s]).to_numpy()

    bow = []
    kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
    for j in range(len(array_text)):
        keywords = kw_extractor.extract_keywords(array_text[j][0])
        bow.append(keywords)
    
    new_bow = []
    for i in range(0, len(bow)):
        for j in range(len(bow[i])):
            new_bow.append(bow[i][j])
    # print(new_bow)
    
    # 불용어 처리
    # split_txt = sub_special(new_bow[0][0]).split(' ')
    for i in range(len(new_bow)):
        new_bow[i] = list(new_bow[i])
        # print(new_bow[i])
        if new_bow[i][0][-1] in STOP_WORDS:
            # print(new_bow[i][0][-1])
            new_bow[i][0] = new_bow[i][0][:-1]
        new_bow[i] = tuple(new_bow[i])
    # print(new_bow)
            
    keyword = pd.DataFrame(new_bow, columns=['keyword', 'weight'])
    result = keyword.groupby('keyword').agg('sum').sort_values('weight', ascending=False).head(20)
    
    frequency_d = result.to_dict()
    wc = WordCloud(
        width=1000, 
        height=600, 
        background_color="white", 
        random_state=0, 
        font_path=r'c:\Windows\Fonts\malgun.ttf'
    )
    plt.imshow(wc.generate_from_frequencies(frequency_d['weight']))
    plt.axis("off")
    plt.show()
    # wc.to_file(path.join(d, "wordcloud.png"))
    
    return result

def run(input):
    total = []
    df = pd.DataFrame({'syno' : input})
    
    for s in df['syno']:
        res = kbert(s)
        print(res.index)
        # print(res.to_list())
        total.append(res.index.to_list())
        
    return total