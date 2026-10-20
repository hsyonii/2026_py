# 1. 딕셔너리
# 딕셔너리명 = { key : value, ... } -> key중복불가 value중복가능

dict1 = { 'name':'어벤져스' , 'type':'영화'}
# dict['key']: 값 호출
print(dict1['name']) # -> '어벤져스'

# dict['key']=value : 요소 추가
dict1['price']=10000
# 이미 존재하는 key 일 경우 수정
dict1['type']='드라마' # -> 'type':'드라마'

# del dict['key']: 삭제
del dict1['price']

# 키 in dict : 키 값의 존재여부 확인, true/false 반환
print('price' in dict1) # false

# 키값으로 속성값 호출하기
# 1) dict['key'] -> 없으면 예외(오류)발생
# 2) dict.get(key) -> 없으면 None 반환
print(dict1.get('name'))
# print(dict1['price']) # -> 예외

# 1-1. 딕셔너리에서의 반복문
# for key in dict:
#   실행문
for key in dict1 :
    print(dict1.get(key))
    print(dict1[key])