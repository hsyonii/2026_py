import seaborn as sns
print(sns.__version__)

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 윈도우 기준 한글 폰트 설정 및 마이너스 부호 깨짐 방지
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 시본 기본 테마 적용 (폰트 설정 유지)
sns.set_theme(font='Malgun Gothic', rc={'axes.unicode_minus': False}, style='whitegrid')

np.random.seed(42)
n = 100
df = pd.DataFrame({
  '나이': np.random.randint(20, 60, size=n),
  '소득': np.random.randint(2500, 9000, size=n),
  '신용점수': np.random.randint(500, 850, size=n),
  '멤버십': np.random.choice(['일반', 'VIP'], size=n, p=[0.7, 0.3]),
  '이탈여부': np.random.choice([0, 1], size=n, p=[0.75, 0.25]) # 0: 유지, 1: 이탈
})
# 나이가 많을수록 소득이 높은 경향 부여
df['소득'] += df['나이'] * 40

# 카운트 플롯 ( 범주형 빈도 집계 )
# sns.countplot( data= 데이터프레임(df) , x= "범주형 컬럼명(가로축)", hue = "그룹(빈도) 컬럼명", palette="색상 테마")
sns.countplot(data=df, x="멤버십", hue="이탈여부", palette= "Set1")
plt.title('멤버십 등급별 이탈빈도') # 그래프 출력시 제목 지정
plt.show() # 그래프 화면에 표시

# 범례 
plt.legend(title="이탈 여부", labels = ['유지(0)', '이탈(1)'])
plt.show()

# 박스플롯(범주형 수치 분포)
#sns.boxplot(data=데이터프레임, x="범주형 컬럼명", y = "수치형 컬럼명", hue="그룹(빈도) 컬럼명" , palette= "색상")
sns.boxplot(data=df, x="멤버십", y = "소득", hue="이탈여부" , palette= "Pastel2")
plt.title("멤버십 이탈 여부에 따른 소득 분포")
plt.show()

# 히트맵
# 상관게수 : 변수1의 값이 변하면 다른변수의 값도 증가/감소 하는 관계 수치화 해둔것( -1 ~ +1 )
# 데이터프레임.corr() : 상관계수 행렬 계산
numeric_df = df[['나이', '소득', '신용점수']] # 문자열(범주형) 제외한 수치형만 추출
corr_matrix = numeric_df.corr()
print( corr_matrix ) 

# sns.heatmap(상관계수행렬, cmap="색상맵", fmt="소수점형식", fmt = '.소수점f', annot = True)
sns.heatmap(corr_matrix, cmap="coolwarm",fmt='.2f',annot=True)
plt.title("상관계수 히트맵")
plt.show()

# 산점도
# sns.scatterplot( data = 데이터 프레임, x = "수치칼럼명", y="수치칼럼명", hue = )
sns.scatterplot(data=df, x = '나이', y ='소득', hue = '이탈여부')
plt.title(" 나이 vs 소득 산점도 ")
plt.show()