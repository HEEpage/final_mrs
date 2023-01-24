from statistics import mean, mode
import operator


# 별점 분포
def get_grades(logs) :
    grade_log = [ log.grade for log in logs ]

    grades = {
        'len_val' : len(grade_log), 
        'mean_val' : mean(grade_log), 
        'mode_val' : mode(grade_log)}

    return grades


# 선호 키워드
def get_keywords(logs) :

    total_keyword = {}
    for log in logs :

        tmp = log.movie_id.keyword.split('|')

        for t in tmp :
            if not t in total_keyword :
                total_keyword[t] = [0, 0, 0]

            total_keyword[t][1] += 1
            total_keyword[t][2] += log.grade
            total_keyword[t][0] = total_keyword[t][2] / total_keyword[t][1]

    keyword = { k : v for k, v in total_keyword.items() if v[1] >= 2 }

    sorted_value = sorted(keyword.items(), key = operator.itemgetter(1), reverse = True)

    return sorted_value


# 선호 배우
def get_casts(logs) :

    total_cast = {}
    for log in logs :

        tmp = log.movie_id.cast.split('|')

        for t in tmp :
            if not t in total_cast :
                total_cast[t] = [0, 0, 0]

            total_cast[t][1] += 1
            total_cast[t][2] += log.grade
            total_cast[t][0] = total_cast[t][2] / total_cast[t][1]


    cast = { k : v for k, v in total_cast.items() if v[1] >= 2 }

    sorted_value = sorted(cast.items(), key = operator.itemgetter(1), reverse = True)

    return sorted_value


# 선호 감독
def get_directors(logs) :

    total_directors = {}
    for log in logs :
        if not log.movie_id.director in total_directors :
            total_directors[log.movie_id.director] = [0, 0, 0]

        total_directors[log.movie_id.director][1] += 1
        total_directors[log.movie_id.director][2] += log.grade
        total_directors[log.movie_id.director][0] = total_directors[log.movie_id.director][2] / total_directors[log.movie_id.director][1]

    directors = { k : v for k, v in total_directors.items() if v[1] >= 2 }

    sorted_value = sorted(directors.items(), key = operator.itemgetter(1), reverse = True)

    return sorted_value


# 선호 장르
def get_genres(logs) :

    total_genre = {}
    for log in logs :

        tmp = log.movie_id.genre.split('|')

        for t in tmp :
            if not t in total_genre :
                total_genre[t] = [0, 0, 0]

            total_genre[t][1] += 1
            total_genre[t][2] += log.grade
            total_genre[t][0] += total_genre[t][2] / total_genre[t][1]


    genre = { k : v for k, v in total_genre.items() if v[1] >= 2 }

    sorted_value = sorted(genre.items(), key = operator.itemgetter(1), reverse = True)

    return sorted_value


# 감상 시간
def get_times(logs) :
    total = sum([ log.movie_id.running_time for log in logs if log.movie_id.running_time != None])
    hour = total // 60
    minute = total % 60

    return {'hour' : hour, 'minute' : minute}

# 실행
def stats(logs) :

    info = {
        "grades" : get_grades(logs),
        "keywords" : get_keywords(logs)[:20],
        "directors" : get_directors(logs)[:5],
        "casts" : get_casts(logs)[:5],
        "genres" : get_genres(logs)[:5],
        "times" : get_times(logs),
    }
    
    return info