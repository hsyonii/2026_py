# Python 데이터분석 Practice6: 종합예제1
# 문제1 [ 타이타닉 생존 데이터 분석]
# 출처: Kaggle - Titanic: Machine Learning from Disaster

# [2. 가설]
# 가설 1: 여성과 아동의 생존율이 남성보다 월등히 높을 것이다. (사회적 보호 )
# 가설 2: 높은 객실 등급(1등석)을 이용한 승객일수록 생존율이 높을 것이다. (경제적 지위와 안전의 상관관계)
# 가설 3: 특정 항구(사우샘프턴 등)에서 탑승한 승객은 객실 등급 분포에 따라 생존율 차이가 발생할 것이다.

# [3. 자료수집 ]
# 3-1 : https://www.kaggle.com/competitions/titanic/overview
# 3-2 : train.csv 파일 판다스로 불러오기 

# [4. 데이터 전처리]
# 수치형 결측치 보정: '나이(Age)' 컬럼의 결측치는 이상치에 강건한(Robust) 분석을 위해 중앙값(Median)으로 대체해야 한다.
# 범주형 결측치 보정: '승선 항구(Embarked)' 컬럼의 결측치는 가장 빈번하게 등장하는 최빈값(Mode)으로 대체해야 한다.

# [5. 데이터 시각화 및 분석]
# 5-1 : 생존 분포 분석: 전체 생존자와 사망자의 비중을 파악할 수 있는 막대그래프 를 생성한다.
# 5-2 : 연령대별 상세 분석:나이에 따른 생존/사망 분포를 히스토그램으로 시각화한다.데이터의 흐름을 파악할 수 있도록 커널 밀도 추정 곡선(KDE)을 포함한다.
# 5-4 (성별): plt.bar을 사용하여 성별(Sex)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
# 5-5 (객실 등급): plt.bar을 사용하여 객실 등급(Pclass)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
# 5-6 (승선 항구): plt.bar을 사용하여 승선 항구(Embarked)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./py_practice/train.csv')

# [4. 데이터 전처리]
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode().iloc[0])

# 5-1. 전체 생존/사망 분포
counts = df['Survived'].value_counts().reindex([0, 1], fill_value=0)
plt.figure(figsize=(7, 5))
plt.title('(전체) 생존자 분포')
plt.bar(['사망', '생존'], counts.values)
plt.xlabel('생존 여부')
plt.ylabel('인원수')
plt.tight_layout()
plt.show()

# 5-2
bins = np.linspace(df['Age'].min(), df['Age'].max(), 31)
ages = np.linspace(bins[0], bins[-1], 200)
plt.figure(figsize=(9, 5))
for survived, label in [(0, '사망'), (1, '생존')]:
    group = df.loc[df['Survived'].eq(survived), 'Age']
    plt.hist(group, bins=bins, alpha=0.4, label=label)
plt.title('나이에 따른 생존/사망 분포')
plt.xlabel('나이')
plt.ylabel('인원수')
plt.legend()
plt.tight_layout()
plt.show()

# 5-4~5-6
plt.figure(figsize=(17, 5))
for position, column in enumerate(['Sex', 'Pclass', 'Embarked'], start=1):
    counts = pd.crosstab(df[column], df['Survived']).reindex(columns=[0, 1], fill_value=0)
    x = np.arange(len(counts))
    plt.subplot(1, 3, position)
    plt.bar(x - 0.2, counts[0], width=0.4, label='사망')
    plt.bar(x + 0.2, counts[1], width=0.4, label='생존')
    plt.xticks(x, counts.index)
    plt.title(f'{column}별 생존 여부')
    plt.xlabel(column)
    plt.ylabel('인원수')
    plt.legend()
plt.tight_layout()
plt.show()

# 가설1
df['비교 집단'] = np.select(
    [df['Age'].lt(18), df['Sex'].eq('female')],
    ['아동(18세 미만)', '성인 여성'],
    default='성인 남성'
)
print('[문제1] 전체 생존율: ', f"{df['Survived'].mean():.2%}")
print('비교 집단별 통계: ', df.groupby('비교 집단')['Survived'].agg(인원수='size', 생존율='mean'))
print('성별 통계: ', df.groupby('Sex')['Survived'].agg(인원수='size', 생존율='mean'))
print('객실 등급별 통계: ', df.groupby('Pclass')['Survived'].agg(인원수='size', 생존율='mean'))
print('항구별 통계: ', df.groupby('Embarked')['Survived'].agg(인원수='size', 생존율='mean'))
# 가설2, 3
print('항구별 등급 구성비: ', df.groupby('Embarked')['Pclass'].value_counts(normalize=True).unstack(fill_value=0))
print('항구/등급별 생존율: ', df.groupby(['Embarked', 'Pclass'])['Survived'].mean().unstack())

###########################################################
# 문제2[ 서울시 공공자전거 대여이력 분석]
# 출처: 서울 열린데이터 광장

# [2. 가설]
# 가설 1: 출퇴근 시간대(08시, 18시 전후)의 자전거 대여량이 다른 시간대에 비해 압도적으로 높을 것이다.
# 가설 2: 특정 지하철역 인근이나 유동인구가 많은 지역의 대여소가 대여량 상위권을 차지할 것이다.
# 가설 3: 이용시간과 이용거리 사이에는 강한 양의 상관관계가 존재할 것이다.

# [3. 자료수집]
# 3-1 : https://data.seoul.go.kr/dataList/OA-15182/F/1/datasetView.do
# https://drive.google.com/file/d/1tXfjwXu5HQUyKupqWeEiNk7ZlN0Xf7xw/view
# 3-2 : 2025년 1월, 2월 대여이력 CSV 파일 로드 (encoding='cp949')

# [4. 데이터 전처리 및 병합]
# 4-1 (병합): pd.concat을 사용하여 분리된 월별 데이터를 하나로 통합하고 인덱스를 재부여한다.
# 4-2 (정제): 결측치의 문자열 표현('\N')을 None으로 치환하고, 성별 데이터를 대문자로 통일 및 결측치를 'U'로 보정한다.
# 4-3 (형변환): 이용시간, 거리 등 주요 수치형 변수는 pd.to_numeric으로 변환하고, 날짜 데이터는 pd.to_datetime으로 객체화한다.
# 4-4 (파생변수): 대여일시에서 시간(Hour) 정보를 추출하여 '대여 시간대' 열을 새롭게 생성한다.

# [5. 데이터 시각화 및 분석]
# 5-1 (성별 분포): plt.bar을 사용하여 성별에 따른 따릉이 이용 비중을 시각화한다.
# 5-2 (시간대 분석): plt.bar을 사용하여 24시간 중 어느 시간대에 대여가 집중되는지 분석한다.
# 5-3 (인기 대여소): value_counts().head(10)를 활용하여 가장 활발한 상위 10개 대여소를 가로 막대 그래프로 시각화한다.
# 5-4 (상관관계): plt.imshow을 통해 이용시간, 이용거리, 시간대 등 수치 데이터 간의 밀접도를 분석한다.
columns = ['대여일시', '대여 대여소명', '성별', '이용시간(분)', '이용거리(M)']
data1 = pd.read_csv('./py_practice/서울특별시 공공자전거 대여이력 정보_2501.csv',
                    encoding='cp949', usecols=columns, dtype=str)
data2 = pd.read_csv('./py_practice/서울특별시 공공자전거 대여이력 정보_2502.csv',
                    encoding='cp949', usecols=columns, dtype=str)
# 4-1
data = pd.concat([data1, data2], ignore_index=True)

# 4-2
data = data.replace(r'\N', None)
data['성별'] = data['성별'].str.strip().str.upper().replace('', None).fillna('U')
# 4-3
for column in ['이용시간(분)', '이용거리(M)']:
    data[column] = pd.to_numeric(data[column], errors='coerce')
data['대여일시'] = pd.to_datetime(data['대여일시'], errors='coerce')
# 4-4
data['대여 시간대'] = data['대여일시'].dt.hour

# 5-1
gender_counts = data['성별'].value_counts().sort_index()
plt.figure(figsize=(7, 5))
plt.bar(gender_counts.index, gender_counts.values)
plt.title('성별 따릉이 이용 건수')
plt.xlabel('성별')
plt.ylabel('대여 건수')
plt.tight_layout()
plt.show()

# 5-2
hourly = data['대여 시간대'].value_counts().reindex(range(24), fill_value=0).sort_index()
hourly_table = hourly.rename_axis('대여 시간대').reset_index(name='대여 건수')
plt.figure(figsize=(12, 5))
plt.bar(hourly.index, hourly.values)
plt.xticks(range(24))
plt.title('시간대별 따릉이 대여 건수')
plt.xlabel('대여 시간대')
plt.ylabel('대여 건수')
plt.tight_layout()
plt.show()

# 5-3
top10 = data['대여 대여소명'].value_counts().head(10)
plt.figure(figsize=(12, 7))
plt.barh(top10.index, top10.values)
plt.gca().invert_yaxis()
plt.title('대여 건수 상위 10개 대여소')
plt.xlabel('대여 건수')
plt.ylabel('대여소')
plt.tight_layout()
plt.show()

# 5-4
corr = data[['이용시간(분)', '이용거리(M)', '대여 시간대']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', vmin=-1, vmax=1,
            cbar_kws={'label': '상관계수'})
plt.title('따릉이 이용 변수 간 상관관계')
plt.tight_layout()
plt.show()

print('\n[문제2] 전체 대여 건수:', len(data))
print('\n성별 이용 비중\n', data['성별'].value_counts(normalize=True))
print('\n시간대별 대여 건수\n', hourly)
print('\n인기 대여소 상위 10곳\n', top10)
print('\n상관계수\n', corr)
print('\n대여일시 변환 실패 건수:', data['대여일시'].isna().sum())

# 가설 해석: 출퇴근 시간과 다른 시간의 대여량을 비교한다.
# 상위 대여소가 지하철역 인근인지는 위치 자료로 추가 확인해야 한다.
# 이용시간과 거리의 상관계수로 양의 상관 강도를 판단한다.
# 시간대는 순환 변수이므로 선형 상관계수 해석에 주의한다.
