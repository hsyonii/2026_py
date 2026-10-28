import numpy as np
# Python NumPy Practice1

# [문제 1]
# 1. 0부터 18까지 2씩 증가하는 1차원 정수 배열 arr_step을 np.arange로 생성하시오.
# 2. 0.0부터 1.0 사이를 균등하게 5개 구간으로 나눈 배열 arr_lin을 np.linspace로 생성하시오.
# np.arange( 시작, 끝, 간격값 ) : 일정 간격의 배열 생성
print('\n[문제 1]')
arr_step = np.arange(0,19,2)
# np.linspace( 시작, 끝, num = 개수 ) : 시작~끝 범위 일정한 간격으로 지정한 개수의 값 생성
# 5개 구간으로 나누려면 경계 값은 6개 필요함
arr_lin = np.linspace(0.0, 1.0, num = 6)
print(arr_step)
print(arr_lin)

# [문제 2]
# 1. 모든 요소가 0으로 채워진 2행 3열의 배열 zeros_arr을 생성하시오.
# 2. 모든 요소가 1로 채워진 2행 3열의 배열 ones_arr을 생성하시오.
# 3. 생성한 zeros_arr의 모양(shape)과 전체 요소 개수(size)를 각각 출력하시오.
# np.zeros((행, 열)), np.ones((행, 열)) : 0과 1로 채운 배열 생성
print('\n[문제 2]')
zeros_arr = np.zeros((2, 3))
ones_arr = np.ones((2, 3))
print(zeros_arr)
print(ones_arr)
# 자료.shape : 자료의 모양 , 자료.size : 요소 개수
print(zeros_arr.shape)
print(zeros_arr.size)

# [문제 3]
# 1. 문자열 리스트 ['python', 'numpy']를 np.bytes_ 타입의 배열로 생성하여 dtype을 확인하시오.
# 2. 실수형 배열 arr_float = np.array([1.7, 2.4, 3.9], dtype=np.float32)을 np.int32 타입으로 형변환하여 소수점이 절삭된 새 배열을 출력하시오.
arr_str = np.array(['python', 'numpy'],dtype = np.bytes_)
print('\n[문제 3]')
print(arr_str.dtype)
arr_float = np.array([1.7, 2.4, 3.9], dtype=np.float32)
arr_int = arr_float.astype(np.int32)
print(arr_int)

# [문제 4]
# 2차원 배열 arr = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])에 대해:
# 1. 1행 2열의 값과 음수 인덱스만을 사용한 마지막 행 마지막 열의 값을 각각 추출하시오.
# 2. 배열 내에서 50을 초과하는 요소들만 불리언 인덱싱으로 추출하여 1차원 배열로 출력하시오.
arr = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
print('\n[문제 4]')
# 첫 번째 행, 두 번째 열 (인덱스는 0부터 시작)
print(arr[0, 1])  # 20
print(arr[-1, -1])  # 90
print(arr[arr > 50])  # [60 70 80 90]


# [문제 5]
# 동일한 2차원 배열 arr = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]]) 기준으로:
# 1. 모든 행의 1번 열 데이터([20, 50, 80])와 2번 행의 모든 열 데이터([70, 80, 90])를 각각 슬라이싱하시오.
# 2. 0번 인덱스 행과 2번 인덱스 행 전체를 인덱싱으로 한 번에 추출하시오.
print('\n[문제 5]')
print(arr[:, 1])  # [20 50 80]
print(arr[2, :])  # [70 80 90]
print(arr[[0, 2], :])

# [문제 6]
# 배열 x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])에서
# 상단 1개 행과 우측 3개 열이 교차하는 서브 배열 을 2차원 슬라이싱 문법([행_슬라이싱, 열_슬라이싱])으로 추출하시오.
print('\n[문제 6]')
x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(x[:1, -3:])  # [[1 2 3]]: 2차원 유지

# [문제 7]
# 배열 x = np.array([10, 20, 30, 40, 50])에 대해:
# 1. 슬라이싱[1:3] 이후 독립 복사 [0]= 1000을 대입했을 때 원본 x가 유지됨을 확인하시오.
print('\n[문제 7]')
x = np.array([10, 20, 30, 40, 50])
x_copy = x[1:3].copy()
x_copy[0] = 1000
print('복사본:', x_copy)  # [1000 30]
print('원본:', x)  # [10 20 30 40 50]

# [문제 8]
# 두 배열 a = np.array([1, 2, 3]), b = np.array([4, 5, 6])에 대해:
# 1. 두 배열의 요소별 곱셈(a * b)과 거듭제곱(a ** 2) 결과를 계산하시오.
# 2. 배열 a의 모든 요소에 5를 더한 결과와 요소별 제곱근(np.sqrt)을 구하시오.
print('\n[문제 8]')
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a * b)  # [4 10 18]
print(a ** 2)  # [1 4 9]
print(a + 5)  # [6 7 8]
print(np.sqrt(a))

# [문제 9]
# 배열 x = np.arange(1, 11) (1부터 10까지의 정수 배열)에서:
# 1. 비트 연산자 '&'를 사용하여 '3 초과이면서 8 미만'인 요소만 추출하시오.
# 2. 비트 연산자 '|'를 사용하여 '2 이하이거나 9 이상'인 요소만 추출하시오.
print('\n[문제 9]')
x = np.arange(1, 11)
print(x[(x > 3) & (x < 8)])  # [4 5 6 7]
print(x[(x <= 2) | (x >= 9)])  # [1 2 9 10]

# [문제 10]
# 두 배열 x = np.array([10, 20, 30]), y = np.array([15, 20, 25])에 대해:
# 1. 두 배열의 같은 위치 요소끼리 비교하여 x >= y 결과를 불리언 배열로 출력하시오.
# 2. 조건 (x < 20) | (x == 30)을 만족하는 x의 요소들만 불리언 인덱싱으로 추출하시오.
print('\n[문제 10]')
x = np.array([10, 20, 30])
y = np.array([15, 20, 25])
print(x >= y)  # [False True True]
print(x[(x < 20) | (x == 30)])  # [10 30]
