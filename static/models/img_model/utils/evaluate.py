import os
import ast
import glob
import pandas as pd
import configparser
from annoy import AnnoyIndex


# Importing variables
config = configparser.ConfigParser()
config.read('C:/final_project/final_mrs/static/models/img_model/config.ini')

# 추천될 이미지의 임베딩 데이터 경로 가져오기
embedding_df_dir = glob.glob(os.path.join(config.get("EVALUATE", "RESULTS"), "*.csv"))
embedding_df_path = max(embedding_df_dir, key=os.path.getctime)
embedding_df_path = embedding_df_path.replace("\\", "/")

# 추천될 이미지의 임베딩 데이터 경로에 따른 csv 파일 읽어오기
embedding_df = pd.read_csv(embedding_df_path)
num_of_records = embedding_df.shape[0]

# 읽어온 임베딩 데이터를 리스트로 저장
all_images = embedding_df["img"].values.tolist()
all_embeddings = embedding_df["embedding"].values.tolist()
all_embeddings = [ast.literal_eval(emb) for emb in all_embeddings]

all_genres = embedding_df["genres"].tolist()
all_index = list(range(num_of_records))

index_to_image = dict(zip(all_index, all_images))
index_to_embedding = dict(zip(all_index, all_embeddings))
index_to_genre = dict(zip(all_index, all_genres))

embedding_dimension = 2048
index = AnnoyIndex(embedding_dimension, "dot") # nearest-neighbor

# We unbatch the dataset because Annoy accepts only scalar (id, embedding) pairs.
for idx, embedding in enumerate(all_embeddings):
    index.add_item(idx, embedding)

# Build a N-tree ANN index.
N = 100
index.build(N)
index.save(os.path.join(config.get("EVALUATE", "RESULTS"), "embeddings_index_{}.ann".format(embedding_df_path.split("/")[-1].replace(".csv", ""))))

def generateViz(mySet): # , name
    image_set = []
    genre_set = []
    for mov in mySet:
        query_embedding = index_to_embedding[mov]
        candidates = index.get_nns_by_vector(query_embedding, 5) # 3개 추천 받기, 넣은 벡터에 대해 가장 가까운 5개 벡터 반환
        genre_set.append(index_to_genre[mov])
        image_set.append(index_to_image[mov])
        genre_set += [index_to_genre[i] for i in candidates]
        image_set += [int(index_to_image[i].split(".")[0]) for i in candidates]

    return image_set[2:]

def getImage(movie_id):
    input = movie_id
    input_id = str(input) + ".png"

    # 영화 id를 받고 어떤 파일과 비교하여 그 파일의 인덱스를 가져오기
    driver_image_set = [all_images.index(input_id)] # 사용자의 평점이 가장 높은 영화
    
    return generateViz(driver_image_set)