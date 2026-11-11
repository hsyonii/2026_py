import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Windows 기준 Malgun Gothic, Mac: AppleGothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 시드 고정 및 데이터 생성
np.random.seed(42)
n_samples = 200

common_data = {
    '고객ID': [f'USER_{i:03d}' for i in range(1, n_samples + 1)],
    '연령': np.random.randint(20, 60, size=n_samples),
    '월이용금액': np.random.normal(loc=150, scale=40, size=n_samples).round(1),  # 단위: 천원
    '구매건수': np.random.poisson(lam=5, size=n_samples),
    '만족도점수': np.clip(np.random.normal(loc=75, scale=12, size=n_samples), 40, 100).round(1),
    '회원등급': np.random.choice(['Bronze', 'Silver', 'Gold', 'VIP'], size=n_samples, p=[0.4, 0.3, 0.2, 0.1]),
    '주요결제수단': np.random.choice(['신용카드', '간편결제', '계좌이체'], size=n_samples, p=[0.5, 0.35, 0.15]),
    '재구매여부': np.random.choice(['Yes', 'No'], size=n_samples, p=[0.7, 0.3])
}

df = pd.DataFrame(common_data)

# [공통 샘플/더미 데이터셋 정의]
# - 고객ID: 'USER_001' ~ 'USER_200' (총 200명)
# - 연령: 20세 ~ 59세 정수형 난수
# - 월이용금액: 평균 150, 표준편차 40 정규분포 난수 (단위: 천원, 소수점 첫째자리)
# - 구매건수: 모수 5 포아송 분포 난수
# - 만족도점수: 평균 75, 표준편차 12 정규분포 난수 (최소 40, 최대 100 클리핑)
# - 회원등급: ['Bronze', 'Silver', 'Gold', 'VIP'] (비율 4:3:2:1)
# - 주요결제수단: ['신용카드', '간편결제', '계좌이체'] (비율 50%, 35%, 15%)
# - 재구매여부: ['Yes', 'No'] (비율 70%, 30%)

# 문제 1: 다중 선 그래프
# 공통 데이터프레임(df) 상위 10개 행(df.head(10))의 인덱스를 x축으로 하여 두 지표의 추이를 하나의 선 그래프로 그리시오.
# **x축: 상위 10행 데이터의 인덱스(df.head(10).index)
# 선 1: '월이용금액', 라벨 '월이용금액' -> **y축
# 선 2: '만족도점수', 라벨 '만족도점수' -> **y축
# - 조건: 두 지표의 흐름을 비교할 수 있도록 범례(legend)를 표시하고 제목을 '상위 10명 고객 지표 추이'로 설정하시오.
# 자료.head(개수) : 자료 앞에서부터 n개 행 가져옴
top10 = df.head(10)
# plt.figure(figsize=(가로,세로)) : 인치 단위로 그래프를 그릴 배경 사이즈 지정하여 생성
plt.figure(figsize=(9, 5))
# plt.plot(x축, y축, marker='데이터마커모양', label='표시할 이름(범례)'): 그래프에 선 추가
# -> marker는 'o':원, 's':네모
# 자료.index : 자료의 인덱스 추출 ( 시리즈, 데이터프레임에 사용가능 )
plt.plot(top10.index, top10['월이용금액'], marker='o', label='월이용금액')
plt.plot(top10.index, top10['만족도점수'], marker='s', label='만족도점수')
# plt.title('제목')
plt.title('상위 10명 고객 지표 추이')
plt.grid(True, linestyle=':', alpha=0.6)  # 눈금 위치에 점선 격자 표시
plt.legend() # 범례표시
plt.show() # 그래프 출력

# 문제 2: 범주별 빈도 막대그래프
# 공통 데이터프레임(df)의 '주요결제수단'별 결제 건수(빈도수)를 막대그래프로 시각화하시오.
# x축: 결제수단 종류 (df['주요결제수단'].value_counts().index)
# y축: 결제수단별 빈도수 (df['주요결제수단'].value_counts().values)
# - 조건: x축에 결제수단, y축에 건수를 매핑하여 결제수단 간 규모를 비교하고 축 레이블과 제목을 설정하시오.
# 열.value_counts() : 해당열에 데이터별로 건수를 세어 시리즈(딕셔너리)로 반환
payment_counts = df['주요결제수단'].value_counts()
plt.figure(figsize=(8, 5)) # 배경 그리기
# plt.bar(x축,y축)
plt.bar(payment_counts.index, payment_counts.values)
plt.title('주요 결제수단별 빈도')
plt.xlabel('결제수단')
plt.ylabel('건수')
plt.show()

# 문제 3: 연속형 변수 간 관계 분석 산점도
# 공통 데이터프레임(df)의 '연령'과 '월이용금액' 두 수치형 변수 간의 관계를 산점도로 시각화하시오.
# - 데이터: x축 '연령', y축 '월이용금액'
# - 조건: 두 변수 간의 상관성 및 분포 패턴을 확인할 수 있도록 각각 x축과 y축에 매핑하고 제목을 설정하시오.
plt.figure(figsize=(8, 5))
# plt.scatter(x좌표,y좌표, alpha=점투명도) : 산점도 표시
plt.scatter(df['연령'], df['월이용금액'], alpha=0.7)
plt.title('연령과 월이용금액의 관계')
plt.xlabel('연령(세)')
plt.ylabel('월이용금액(천원)')
plt.show()

# 문제 4: 연속형 수치 데이터 분포 분석
# 공통 데이터프레임(df)의 '만족도점수' 데이터를 활용하여 구간별 빈도 분포를 !!히스토그램!!으로 나타내시오.
# - 데이터: '만족도점수'
# - 조건: 구간(bins) 수를 10개로 설정하여 점수 구간별 데이터의 밀집도와 형태를 확인하시오.
plt.figure(figsize=(8, 5))
# plt.hist(수치데이터, bins=구간개수, color='색상',edgecolor='테두리색', alpha='투명도'): 히스토그램 생성
plt.hist(df['만족도점수'], bins=10, edgecolor='black') # bins=10 -> 데이터범위를 일정한 10개구간으로 나눔
plt.title('만족도점수 분포')
plt.xlabel('만족도점수(점)')
plt.ylabel('빈도(명)')
plt.show()

# 문제 5: 단일 변수 5수치 요약 및 이상치 탐색
# 공통 데이터프레임(df)의 '월이용금액' 데이터를 활용하여 중심 위치와 *사분위수 범위를 박스플롯으로 시각화하시오.
# *사분위수? 데이터를 오름차순으로 정렬한뒤 4등분할때 기준이되는값 3개(Q1,Q2,Q3) -> Q2: 중앙값
# - 데이터: '월이용금액'
# - 조건: 데이터의 중앙값, 사분위수(Q1, Q3), 정상 범위 및 이상치(Outlier)가 드러나도록 박스플롯을 생성하시오.
plt.figure(figsize=(6, 5))
# plt.boxplot(데이터, vert=True/False, patch_artist=True/False) : 박스 플롯 생성
# vert = True: 박스방향세로(기본값), False: 가로 / patch_artist=True: 박스색 채우기(기본값)
plt.boxplot(df['월이용금액'])
plt.xticks([1], ['월이용금액'])
plt.title('월이용금액 분포와 이상치')
plt.ylabel('월이용금액(천원)')
plt.show()

# 문제 6: 범주형 데이터 빈도 집계
# Seaborn을 활용하여 회원등급별 인원수와 각 등급 내 재구매 여부 분포를 카운트플롯으로 시각화하시오.
# - 데이터: 공통 데이터프레임(df)
# - 조건: x축에 '회원등급'을 배치하고, '재구매여부' 컬럼을 세부 구분 그룹(hue)으로 매핑하여 집계하시오.

# 문제 6 풀이: hue로 각 회원등급 안의 재구매 여부를 나눕니다.
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='회원등급', hue='재구매여부',
              order=['Bronze', 'Silver', 'Gold', 'VIP'],
              hue_order=['Yes', 'No'])
plt.title('회원등급별 재구매 여부 분포')
plt.xlabel('회원등급')
plt.ylabel('인원수(명)')
plt.legend(title='재구매여부')
plt.show()

# 문제 7: 범주별 수치 분포 비교
# Seaborn을 활용하여 주요 결제수단 그룹에 따른 월이용금액의 분포 차이를 박스플롯으로 비교하시오.
# - 데이터: 공통 데이터프레임(df)
# - 조건: x축에 '주요결제수단', y축에 '월이용금액'을 매핑하여 결제수단별 금액 수준과 분산 정도를 한 화면에서 비교하시오.
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='주요결제수단', y='월이용금액')
plt.title('주요 결제수단별 월이용금액 분포')
plt.xlabel('주요결제수단')
plt.ylabel('월이용금액(천원)')
plt.show()

# 문제 8: 다변량 상관계수 행렬 시각화
# Seaborn을 활용하여 공통 데이터프레임(df) 내 연속형 수치 변수 간의 선형 관계 강도를 히트맵으로 나타내시오.
# - 데이터: df의 '연령', '월이용금액', '구매건수', '만족도점수' 컬럼 피어슨 상관계수 행렬(.corr())
# - 조건: 각 셀에 계산된 상관계수 수치를 표시(annot=True)하여 변수 간 상관성의 방향과 크기를 직관적으로 파악할 수 있게 하시오.
corr_matrix = df[['연령', '월이용금액', '구매건수', '만족도점수']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            vmin=-1, vmax=1, center=0, square=True)
plt.title('수치형 변수 간 상관계수')
plt.show()

# 문제 9: 그룹 구분을 포함한 다변량 산점도
# Seaborn을 활용하여 '구매건수'와 '만족도점수'의 관계를 회원등급별로 세분화하여 시각화하시오.
# - 데이터: 공통 데이터프레임(df)
# - 조건: x축에 '구매건수', y축에 '만족도점수'를 매핑하고, 점의 그룹 구분 기준(hue)으로 '회원등급'을 적용하시오.
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='구매건수', y='만족도점수', hue='회원등급',
                hue_order=['Bronze', 'Silver', 'Gold', 'VIP'], alpha=0.7)
plt.title('회원등급별 구매건수와 만족도점수의 관계')
plt.xlabel('구매건수(건)')
plt.ylabel('만족도점수(점)')
plt.legend(title='회원등급')
plt.show()

# 문제 10: 다변량 상호 분포 탐색 그리드
# Seaborn을 활용하여 공통 데이터프레임(df) 주요 수치형 변수 쌍 간의 일대일 관계와 개별 분포를 한 번에 조망할 수 있는 페어플롯을 생성하시오.
# - 데이터: df의 '연령', '월이용금액', '만족도점수', '재구매여부' 컬럼
# - 조건: '재구매여부'를 그룹 구분 기준(hue)으로 설정하여 연속형 변수 간 산점도와 각 변수별 분포 형태를 동시에 확인하시오.
pair_grid = sns.pairplot(
    data=df[['연령', '월이용금액', '만족도점수', '재구매여부']],
    vars=['연령', '월이용금액', '만족도점수'],
    hue='재구매여부',
    hue_order=['Yes', 'No'],
    diag_kind='hist',
    plot_kws={'alpha': 0.7},
)
pair_grid.figure.suptitle('재구매 여부에 따른 주요 수치형 변수 관계', y=1.02)
plt.show()
