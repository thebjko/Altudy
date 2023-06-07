# for django-taggit
def custom_tag_string(tag_string):
    '''
    입력값을 스페이스/엔터키로만 구분해 태그로 저장합니다.
    '''
    if not tag_string:
        return []
    return tag_string.split()


# 수정 시 폼에 들어가는 태그 데이터들을 공백으로 구분하게
def space_joiner(tags):
    return ' '.join(t.name for t in tags)