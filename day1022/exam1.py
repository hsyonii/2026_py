# 예외 처리
# try:  except:
input_a=input("정수 입력: ")
try: # 에외가 발생할 가능성 있는 코드
    int(input_a)
except: # 예외가 발생했을 때 실행할 코드
    print("정수가 아닙니다.")
    
# pass : 예외처리 넘기기
try:
    int(input_a)
except:
    pass # -> 예외 오류 띄우지 않고 넘김

# else : 예외가 발생하지 않았을때에만 실행할 코드
else:
    print("정수가 맞습니다.")
    
# finally
try:
    file = open("info.txt", "w") # 파일 쓰기모드(w)로 열기(생성)
    예외.발생() # 일부러 예외발생
    file.close() # 파일 닫기
except:
    print("예외 발생")
print(file.closed) #false -> 예외발생되어 파일닫기 실행안됨.

# 예외 객체: 발생한 예외 정보 갖는 객체
# Exception : 최상위 예외 클래스( 두개 이상의 except 있을경우 항상 마지막애 위치 )
# except 예외클래스명 as 변수명:
# 예제)
numbers = [ 52,34,155,33,11 ] 
try: # 오류 코드
    num_input = int(input('정수입력: '))
    print(numbers[num_input])
except ValueError as e : 
    print( e )
except IndexError as e: # 예외 구분하여 에러 원인 명확하게 파악
    print ( e )
except Exception as e :
    print( e )
    
# 강제 예외 발생: raise 문
try:
    # 미구현인 부분 
    raise NotADirectoryError # 강제로 예외발생
except NotADirectoryError as e :
    print(e)
    
# global
a = 10 # 전역 스택
def 함수():
    global a
    a += 1 # -> 오류, 전역 변수 수정 시에 global 필수
    print ( a ) # global 없어도 전역 스택 단순 호출은 가능
    b = 20 # 함수 스택 

함수()