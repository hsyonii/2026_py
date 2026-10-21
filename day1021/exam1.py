# 함수 정의하기
# def 함수명(매개변수):
#   실행문
def print_3_time():
    print("안녕")
    print("안녕")
    print("안녕")
# 정의한 함수 호출
print_3_time()

# 예)
def print_n_time(value,n):
    for i in range(n):
        print(value)
print_n_time("ㅎㅇ",5) # -> ㅎㅇ 5번 출력
print_n_time("ㅂㅇ") # -> 에러, 정해진 매개변수 형식 지켜야함

## 전개연산자?
# 가변 매개변수
# def 함수명(매개변수, ... ,*가변매개변수):
#   실행문
# 조건 1) 가변매개변수의 위치는 가장 뒤
# 조건 2) 1번만 사용 가능
def print_n_time2(n,*values):
    for i in range(n):
        for value in values : # -> 안녕하세요 즐거운 파이썬 ( value 값 한번씩 )
            print(value)
            
print_n_time2(3, "안녕하세요", "즐거운", "파이썬") # -> 안녕하세요 즐거운 파이썬 * 3번 출력

## 키워드 매개변수?
print("안녕하세요", end = "\n") # end: 함수실행후 무엇을 할지 지정

# 기본 매개변수
def print_n_time4(*values, n=2): # 매개변수 = 기본값 
    for i in range(n):
        for value in values:
            print ( value )

print_n_time4("안녕","안녕","안녕하세요", n=3 ) # -> 안녕 안녕 안녕하세요 * 3 번출력
print_n_time4("안녕","안녕하세요",3) # -> 안녕 안녕하세요 3 * 2번출력

# 자료 없는 리턴 vs 자료 있는 리턴
def return_test():
    print("A위치 입니다.")
    return # 함수 종료
    print("B위치 입니다.")

return_test() # -> B위치 입니다.는 출력되지 않음.

def return_test2():
    return 100

value = return_test2()
print(value) # -> 100

# 예제)
def sum_all(start, end):
    output = 0
    for i in range(start . end + 1):
        output += i
    return output

print("0 to 100:" ,sum_all(0,100))
print("0 to 1000:", sum_all(0,1000))
print("50 to 100:", sum_all(50,100))
print("500 to 1000:", sum_all(500,1000))

def sum_all(start=0, end=100, step=1):
    output = 0
    for i in range(start,end+1,step):
        output += i
    return output

print("A.", sum_all(0,100,10))
print("B.", sum_all(end=100))
print("C.", sum_all(end=100, step=2))

# 재귀함수
def factorial2(n):
    if n == 0:
        return 1
    else:
        return n*factorial1(n-1)
# vs
# 일반 반복문
def factorial1(n):
    output = 1
    for i in range(1,n+1):
        output*=i
    return output

factorial1(3)

# 예제) 구구단
# 재귀
def 구구단(단=2,곱=1):
    # 재귀 탈출조건 먼저 필수로 작성
    if(단>9):          # 경우1. 곱 올리는 경우
        return         # 경우2. 곱이 끝나고 단 올리는견우
    if(곱>9):          # 경우3. 단 끝나는 경우           -> 함수 종료
        구구단(단+1,1)
        return
    print(단*곱)
    구구단(단, 곱+1)
# vs
# 일반 반복문
for 단 in range (2,10,1):
    for 곱 in range (1,10,1):
        print(str(단)+"x"+str(곱)+"="+str(단*곱))
        
# 예제) 피보나치수열
