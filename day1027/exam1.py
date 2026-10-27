import numpy as np

x = np.array([[1,2,],[3,4,]])
y = np.array([[5,6,],[7,8]])
# 1. 병합
# vstack & hstack
z = np.vstack([x,y]) # 세로 쌓기
print(z)
                   # 가로 쌓기
z=np.hstack([x,y]) # [1 2 5 6]
print(z)           # [3 4 7 8]
# concatenate
z = np.concatenate((x,y), axis = 0) # axios = 0: 세로, 1: 가로
print(z)

# 2. 정렬
x= np.array([3,1,2,9,4])
# sort
# 오름차순
print(np.sort(x))
# 내림차순
print(np.sort(x)[::-1])
print(x) # -> 원본 영향 X

x.sort()
print(x) # -> 원본 변경됨

# 3. 필터링, 조건식
x = np.array([10,20,30,40,50])
print(x>30) # [ false false false true ture ]
print(x[x>30]) # [40,50]
y = np.array([1,2,3],[4,5,6],[7,8,9])
print(y%2 == 0)
print(y[y%2==0])

# 4. 삼항 연산자
# np.where(조건, 참, 거짓)
print(np.where(x>30,x,0))
print(np.where(y%2 == 0, 0,1))

# 다수 조건( and: &, or: |, not: ~ )
print(y[(y%2==0) & (y%4==0 )])
print(y[ ( y%2==0) | (y%4==0)])
