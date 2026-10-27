import numpy as np
# 1차원 배열  통계 함수
x = np.array([1,2,3,4,5])
y = np.array([1,2,3,4,5])
total = np.sum(y)
print(total)
print (np.min(x), np.max(x)) # 최소, 최댓값
print (np.argmin(x), np.argmax(x)) # 최소, 최댓값 위치
print(np.sum(x), np.mean(x), np.median(x)) # 합, 평균, 중앙값
print(np.var(x)) # 분산도
print(np.std(x)) # 표준편차( = 분산**2 )
print(np.sqrt(x)) # 양의 제곱근

# 2차원 배열 "
y = np.array([[1,2,3],[4,5,6]])
print(np.min(y), np.max(y)) # 1, 6
print(np.min(y, axis= 0),np.max(y, axis =1)) # axis = 0: 열 마다, 1: 행 마다
print (np.argmin(y), np.argmin(y))
print(np.sum(y,axis = 0 ), np.mean(y,axis = 0), np.median(y, axis =1 ))
print(np.var(x), np.std(x),np,sqrt(x))