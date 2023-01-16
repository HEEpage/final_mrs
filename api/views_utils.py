def obj_to_movie(obj, flag=True):
    """
    obj 의 각 속성을 serialize 해서, dict 로 변환한다.
    serialize: python object --> (기본 타입) int, float, str
    :param obj:
    :param flag: True (모두 보냄, /api/post/99/ 용), False (일부 보냄, /api/post/list/ 용)
    :return:
    """
    movie = dict(vars(obj))

    if obj.id:
        movie['id'] = obj.id

    if obj.running_time:
        movie['running_time'] = obj.running_time
    else:
        movie['running_time'] = "정보없음"


    if obj.avg_grade:
        movie['avg_grade'] = obj.avg_grade
    else:
        movie['avg_grade'] = "정보없음"


    if obj.viewer:
        movie['viewer'] = obj.viewer
    else:
        movie['viewer'] = "정보없음"

        
    del movie['_state'], movie['status'], movie['cnt_click']

    if not flag:
        del movie['director'], movie['cast'], movie['synopsis'], movie['keyword'], 

    return movie