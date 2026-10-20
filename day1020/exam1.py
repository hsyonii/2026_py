## 1. 리스트: [ a, b, c ]
# *인덱스: [n] , 0 ~

# 리스트 선언하기 
list1 = [ 123, 456, 789, 0 ]

# 인덱싱
print ( list1[3] ) # -> 결과: 0
# *print( ): ()안의 내용 출력

# 슬라이싱
print ( list1[1:3] ) # -> 결과: [1]~[2]( 1부터 3전까지 )

# 요소 값 수정하기
list1[2] = "문자열"

print( list1[-2] ) # -> 결과: True ( 인덱싱 음수로 가능 )

print( list1[2][1] ) # -> 결과: "문" ( 문자열도 리스트다 )

print ( list1[1][0] ) # -> 오류 ( 문자 or 숫자 1차원 값 불가능)

# 고차원 배열
list2 = [ a, b, c ] # 1차원
list3 = [ [1,2], [3,4],[5,6] ] # 2차원
print( list3[1][0] ) # -> 결과: 3

# 리스트 연산
list4 = [ 1,2,3 ]
list5 = [ 4,5,6 ]
print( list4 + list5 ) # -> 결과: [ 1,2,3,4,5,6 ]인 리스트 반환

print( list4*3 ) # -> [ 1,2,3,1,2,3,1,2,3 ]
print(len(list4)) # -> 3
# *len(): 길이 반환

# 서로다른 n 차원끼리의 연산
list6 = [ [1,2],[3,4] ]
print(list5+list6) # -> [ 1,2,3,[1,2],[3,4] ]

# 리스트.append(): 리스트 맨뒤에 요소 추가
list5.append("추가") # -> list5 = [4,5,6,"추가"]

# 리스트.insert( 인덱스, 요소 ): 인덱스 지정하여 요소 삽입
list5.insert( 0, "추가추가" ) # -> list5 = [ "추가추가",4,5,6,"추가" ]

list7 = [1,2]
# 방법 1)
list7+[3] # [ 1,2,3 ]인 제 3의 리스트 생성( list7 영향X ) 
# 방법 2)
list7.append(3) # list7=[1,2,3]

# del 리스트[인덱스]: 요소 삭제하기
lista = [1,2,3,4,5]
listb = [6,7,8,9]
del lista[0] # -> lista = [2,3,4,5]
del listb[0:2] # 슬라이싱 적용 가능, -> listb = [8,9]
#리스트.pop(인덱스): 요소 삭제하기
lista.pop(1) # -> lista = [2,4,5]
# .pop vs del?

# 리스트.remove(값): (값)과 일치하는 값 삭제
lista.remove(4) # -> lista=[2,5]
# 리스트.clear(): 리스트 비움(전체 삭제)
listb.clear()

# [ 시작인덱스 : 끝인덱스 : 단계 ]
numbers = [1,2,3,4,5,6,7,8]
print(numbers[0:5:2]) # 0번부터 5번 인덱스 전까지 2씩 증가하며 슬라이싱 -> 0,2,4번
print(numbers[::-1]) # 역순으로 슬라이싱, 시작 및 끝인덱스 생략시 기본값 0 ~ 끝 인덱스

# 리스트.sort(): 리스트 오름차순 정렬
# 리스트.sort(reverse = True): 내림차순 정렬
listc [ 12, 34 ,56 ,78, 90 ]
listc.sort() # -> [90,78,56,34,12] 

# 값 in 리스트: 리스트에 값 이 있는지 확인
print(34 in listc) # -> true
print( 52 not in listc ) # -> true

 
## 2. 반복문
# for 반복변수 in 자료 :
#   실행문
for e in listc :
    print(e)

# 전개 연산자
# *리스트
print(*listc)

# 범위함수
# range
# 1) range(시작값, 끝값+1) -> 시작값 생략시 0 부터
print(range(5)) # -> 0,1,2,3,4
list(range(3)) # -> [0,1,2]
# 2) range(시작값, 끝값, 단계)
print(list(range(0,11,2))) # [0,2,4,6,8,10]

for i in range(10,0,-1): #역순으로 반복문 작성 가능
    print(i)

# 예제) 1~10에서 홀수만 출력하기
for i in range(1,11,2):
    print(i)
    
# while
n = 1
while n <= 10:
    print(n)
    
lista = [1,2,1,2]
value=2
while value in lista:
    list.remove(value) # -> lista = [1,1]
    
# break, continue
for i in range(1,11,1):
    print(i)
    if i == 3:
        break

for i in range(1,11,1):
    print(i)
    if i == 3:
        continue
