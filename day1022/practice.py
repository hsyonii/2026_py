numbers = [ 12,44,223, 98,101, 89]

for number in numbers:
    if number%2 == 0: # 짝수
        print(str(number) + "는  짝수")
    else:
        print(str(number) + "는 홀수")
        
for number in numbers:
    length = len(str(number))
    print(str(number)+"는"+str(length)+"자릿수 입니다.")
    
a = "안녕하세요"
b = "안녕히가세요"
print(a,b)
a,b = b,a
print(a,b)