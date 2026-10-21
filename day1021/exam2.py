# 튜플: (요소,요소,요소...), 리스트와 비슷한 자료형
# 차이점? 한번 결정된 요소 수정 불가능 -> 리스트보다 속도 빨라 읽기모드용 객체(VO)와 같은곳에서 사용
tuple_test = (10,20,30)
tuple_test[0] # -> 10
tuple_test[0] = 40 # -> 오류

tuple_test2 = 10,20,30 # 소괄호 생략가능
tuple_test3 = ( 10, ) # 요소가 한개일때에도 쉼표 필요

# 스왑
a, b = b, a

# 콜백함수
# JS에서 onClick(함수)와 같은형식
def call_10times(func): # 매개변수 자리에 다른 함수 넣어줌 ( 소괄호() 생략 )
    func()
    
def print_hello():
    print("안녕하세요")
    
call_10times(print_hello()) # -> print_hello()의 실행결과를 call_10times 에 전달
call_10times(print_hello) # -> 매개로 print_hello 함수 자체를 전달

# filter( 함수, 리스트 ), map( 함수, 리스트 )
# 반환타입) 연산 결과인 객체의 주소만 반환, 결과값 list로 형변환 필요하다.
def power(item):
    return item*item

def under_3(item):
    return item<3

list_a = [ 1,2,3,4,5 ]
output_a = map(power,list_a)
output_b = filer(under_3,list_a)
print( list(output_a) ) # -> 1,4,9,16,25
print( list(output_b) ) # -> 1,2

# 람다 (화살표 함수) : 간단하게 함수 선언하는 방법.
# 함수명 = lamda 매개변수 : 리턴값
power2 = lambda x : x*x
under3_2 = lambda x : x<3 # -> true/ false 반환

# 인라인 람다
output_c = map(lambda x : x*x, list_a) # map(power2, list_a)하지 않고 함수 동작문을 map()내부에 작성

# 제너레이터: 주소값을 반환하는 함수?
def 함수():
    print("함수 호출")
    yield "test"