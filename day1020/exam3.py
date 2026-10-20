# min, max, sum
numbers = [ 103,52,273,32 ]
print(min(numbers)) # -> 32
print(max(numbers)) # -> 273
print(sum(numbers)) # -> 합계

# reversed
print(reversed(numbers)) # ->[]

# int(), float(), str(), list() : ()의 값을 해당 타입으로 변환

# 문자열.join(리스트) : 리스트 요소 사이마다 문자열 삽입
print("""안녕하세요
      안녕하세요""") # -> """여러줄""" 입력가능
# =
print("안녕하세요\n안녕하세요")
# =
print(("안녕하세요\n""안녕하세요"))
# =
print("\n".join(["안녕하세요","안녕하세요"]))

print("-".join("유재석")) #유-재-석 -> 문자열도 리스트이기 때문에 적용 가능
