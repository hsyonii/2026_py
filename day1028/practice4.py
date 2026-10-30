# Python Pandas Practice4
import pandas as pd
from pathlib import Path

# [기본 제공 코드] CSV 파일 로드 및 구조 확인
df = pd.read_csv('./day1028/ecommerce_orders_cs_data.csv', encoding='utf-8-sig')

print("--- [데이터 기본 구조 확인] ---")
print(df.info())
print("\n--- [상위 5건 데이터] ---")
print(df.head())

# 1. 데이터 준비 및 구조 (Columns) 
# 링크: https://drive.google.com/file/d/1X22ll4NXhnCJp0tTYYqdRyCiS7VUAvUX/view?usp=sharing (다운로드)
# - 파일명 : ecommerce_orders_cs_data.csv (인코딩: utf-8-sig)
# - 컬럼 구성 (총 8개 열)
#   [0] Order_ID    : 주문 고유번호 (문자열, 중복 데이터 포함)
#   [1] Customer_ID : 고객 식별자 (정수형 -> 문자열 변환 필요)
#   [2] Order_Date  : 주문 일자 (YYYY-MM-DD 형식의 문자열)
#   [3] Category    : 상품 카테고리 (빈 문자열 '' 및 스페이스 공백 '   ' 결측치 포함)
#   [4] Price       : 개당 가격 (원, 결측치 NaN 포함)
#   [5] Quantity    : 주문 수량 (음수 및 999 등 비정상 이상치 포함)
#   [6] Payment     : 결제 수단 (신용카드, 간편결제, 계좌이체)
#   [7] Status      : 주문 상태 ('배송완료', '반품요청', '취소')

# 2. 단계별 미션
# [Step 1] 데이터 무결성 검증 및 기본 정제
# - 중복된 주문 행을 제거하고, 연속된 번호로 인덱스를 재정렬(reset_index)하세요.
# - 산술 연산 대상이 아닌 'Customer_ID' 컬럼의 타입을 문자열(str)로 변환하세요. ->'Customer_ID'는 정수형이지만 계산할 숫자가 아닌 고객식별번호이므로 문자열로 변환!!
# 자료.drop_duplicates().reset_index(drop=True) : 모든열의 값이 같은 중복 행 제거. *reset_idex(drop=True): 행번호(인덱스) 0부터 다시매겨줌. 필수!!
df = df.drop_duplicates().reset_index(drop=True)
# 자료.astype( 변환할타입 ) : 자료형변환 
df['Customer_ID'] = df['Customer_ID'].astype(str)
# 자료.dtype : 자료형 확인
print('Customer_ID 자료형:', df['Customer_ID'].dtype)

# [Step 2] 텍스트 공백 정제 및 결측치 대체
# - 'Category' 컬럼의 빈 문자열('')과 스페이스 공백('   ')을 결측치(None)로 일괄 치환하세요.
# - 다음 기준에 따라 결측치를 대체하세요.
#   * 'Category' 컬럼 : 가장 빈도가 높은 '최빈값(mode)'으로 대체
#   * 'Price' 컬럼    : 이상치 영향을 최소화하기 위해 '중앙값(median)'으로 대체
# .str.strip() : 문자열 (앞뒤)공백 제거 ( '  ' -> '' )
# .replace( 치환할값, 치환된값 )
df['Category'] = df['Category'].str.strip().replace('', None) # 공백있는 데이터를 ''(빈 문자열)로 변환후, ''을 None으로 치환
# .mode() : 해당 자료에서 최빈값 반환
# .fillna( 치환된값 ) : 해당자료에서 None인 데이터를 ()안의 데이터로 치환
df['Category'] = df['Category'].fillna(df['Category'].mode())
# .median() : 데이터 정렬됐을 때 중앙값 반환
df['Price'] = df['Price'].fillna(df['Price'].median()) # -> 결측치 중앙값으로 대체

# [Step 3] 이상치 보정 
# - 주문 수량('Quantity') 컬럼에 포함된 비정상 데이터(-1, 999 등)를 정상 유효 범위인 1개 이상 10개 이하로 경계 조정(clip)하세요.
# .ciip(lower = 하한값, upper=상한값) : 자료내 하한값~상한값 범위 외 데이터를 경계값(하한or상한값)에 맞춤
df['Quantity'] = df['Quantity'].clip(lower=1, upper=10)

# [Step 4] 비즈니스 파생변수 생성
# - 'Price'와 'Quantity'를 곱하여 총 주문 금액인 'Total_Amount' 파생 컬럼을 생성하세요.
# - 'Order_Date'를 날짜형(datetime)으로 변환한 뒤, 연도('Order_Year')와 월('Order_Month') 파생 컬럼을 각각 추출하세요.
# - `mask` 메서드를 활용하여 'Total_Amount'가 300,000원 이상인 주문 건을 'VIP', 나머지를 'Normal'로 분류하는 'VIP_Flag' 파생 컬럼을 생성하세요.
df['Total_Amount'] = df['Price'] * df['Quantity']
# pd.to_datetime(문자열형 자료) : 자료를 날짜형(datetime)으로 바꿈
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
# .dt.year / .dt.month : 날짜형자료에서 연도/월 만 추출
df['Order_Year'] = df['Order_Date'].dt.year
df['Order_Month'] = df['Order_Date'].dt.month
# .mask(조건, 바꿀값) : 조건이 참일경우 지정값으로 변경
# mask 메서드를 활용하려면 기존값 있어야하므로 일단 Normal로 채운 칼럼 생성
df['VIP_Flag'] = 'Normal'
df['VIP_Flag'] = df['VIP_Flag'].mask(df['Total_Amount'] >= 300000, 'VIP')

# [Step 5] 집계 및 정렬 
# - 카테고리('Category')별로 그룹화하여 다음 4가지 지표를 한 번에 다중 집계(agg)하세요.
#   * 주문건수 : 'Order_ID'의 개수(count)   -> 주문건수 = ('Order_ID','count)
#   * 총매출   : 'Total_Amount'의 합계(sum) -> 총매출 = ('Total_Amount','sum')
#   * 평균단가 : 'Price'의 평균(mean)       -> 평균단가 = ('Price','mean')
# - 집계된 결과 테이블을 '총매출' 기준 내림차순(ascending=False)으로 정렬하여 출력하세요.
# .groupby('기준칼럼') : 설정한 칼럼에서 같은데이터끼리 그룹화 ( ex - 'Category'가 같은것끼리 )
# .agg() (1) 하나의 열에 여러 함수 적용 : .agg(['함수1', '함수2', '함수3']) -> 코드 한줄로 여러함수의 결과값을 얻을 수 있음
#        (2) 열마다 다른 함수 적용 : .agg({
#                                       '열이름1' : '함수1'          -> 열:함수 1대1일경우 결과값 시리즈(딕셔너리)
#                                       '열이름1' : ['함수2,'함수3'] -> 함수 여러개도 가능
#                                       })
#        (3) 결과열 이름지정하여 함수적용 : .agg(
#                                               결과열이름 = ( '열이름1','함수1'), -> 결과열이름: 열, 'Category': 행
#                                               결과열이름2 = ('열이름2','함수2') ...
#                                              )
# .sort_values('기준 열', ascending=False or True) : 기준열 의 값 기준으로 Fasle: 내림차순 / True: 오름차순 정렬
category_summary = df.groupby('Category').agg(
    주문건수=('Order_ID', 'count'),
    총매출=('Total_Amount', 'sum'),
    평균단가=('Price', 'mean'),
)
category_summary= category_summary.sort_values('총매출', ascending=False)
print(category_summary)

# [Step 6] **One-Hot Encoding? 수치나 식별자가 아닌 범주형데이터를 컴퓨터가 이해하기 쉽도록 종류별로 새롭게 열을만들어 해당/미해당 두가지 데이터로 구분 
# - 머신러닝 모델 입력을 위해 명목형 범주 변수인 'Payment'와 'VIP_Flag'를 원-핫 인코딩(get_dummies)하세요.
# -> Payment_신용카드 , Patment_간편결제 , Payment_계좌이체 , VIP_Flag_Normal , VIP_Flag_VIP 와 같이 새로운 열 생성
# - 단, 결과값이 True/False가 아닌 1과 0의 정수형(dtype=int)으로 생성되도록 옵션을 지정하세요.
# pd.get_dummies(자료, colmns=['열이름','열이름'], dtype=값자료형): 원-핫인코딩결과를 나머지 열 그대로 포함하여 데이터프레임으로 반환(원본 유지)
df_encoded = pd.get_dummies(df, columns=['Payment', 'VIP_Flag'], dtype=int)
# ㄴ> df데이터프레임의 'Payment','VIP_Flag'열의 데이터를 원-핫인코딩하여 값을 0/1로 채운다.
