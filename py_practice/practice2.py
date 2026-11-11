import numpy as np
# [기본 제공 코드] CSV 파일 로드 (헤더 제외, 콤마 구분)
data = np.genfromtxt('./practice/customer_purchase_data.csv', delimiter=',', skip_header=1)
# 데이터 구조 확인: [ID, Visits, Stay_Time, Cart_Items, Purchase_Amount]
print(f"데이터 형태: {data.shape}")

# step 1.
sales = np.array(data[:, 4])
print(sales)
# 평균 구매금액
print(np.mean(sales))
# 총 매출액
print(np.sum(sales))

# [Step 2]
# - 조건: '방문 횟수(1번 열)가 20회 이상' 이거나(|) '구매 금액(4번 열)이 2000달러 이상'인 고객을 '충성 고객'으로 분류하세요.
# - 위 조건에 해당하는 충성 고객들의 '고객ID(0번 열)'만 추출하여 출력하세요.
충성고객 = (data[:,1>= 20] | (data[:,4]>=2000))
print( 충성고객 )
print(data[충성고객, 0])

# [Step 3] 구매 전환율 및 효율성 계산
# - '구매 금액(4번 열) / 방문 횟수(1번 열)'를 계산하여 방문당 평균 매출인 `arpv` 배열을 생성하세요.
# - 방문당 평균 매출(`arpv`)이 가장 높은 고객의 인덱스를 찾고, 해당 고객의 '고객ID(0번 열)'를 출력하세요.
구매금액 = (data[:,4]/data[:,1])
print( 구매금액 )
a = np.argmax(구매금액)
print(data[a,0])

# [Step 4] 휴면 고객 및 이탈 위험군 식별
# - 조건: '방문 횟수(1번 열)가 3회 이하' 이면서(&) '장바구니 담은 횟수(3번 열)가 1회 이하'인 고객을 '이탈 위험 고객'으로 분류하세요.
# - 이 조건에 해당하는 고객들의 전체 데이터(행)를 추출하고, 대상 고객이 총 몇 명인지 출력하세요.
이탈위험 = (data[:,1]<=3 ) & (data[:,3]<=1)
print(data[이탈위험,:])
대상고객 = len(data[이탈위험,:])
print(대상고객)

# [Step 5] 고객 등급 정규화 및 VVIP 선정
# - 구매 금액(`sales`) 데이터를 0과 1 사이의 값으로 정규화(Min-Max Scaling) 하세요. * 공식 : ( x - 최솟값 ) / ( 최댓값 - 최솟값 )
# - 정규화된 값이 0.9 이상(상위 10% 수준)인 고객을 'VVIP'로 정의하고, 해당 VVIP 고객들의 모든 정보(Row 전체)를 추출하여 출력하세요.
# -- 추출된 VVIP 고객 데이터를 '구매 금액(4번 열)' 기준 내림차순(높은 금액 순)으로 정렬하여 상위 5명의 정보를 출력하세요.
정규화 = (sales-np.min(sales)) / (np.max(sales)- np.min(sales))
vvip = 정규화>= 0.9
vvips = data[vvip,:]
vvips = np.sort(vvips)[::-1]
print(vvips[:5])