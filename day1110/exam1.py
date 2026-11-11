import pandas as pd
df = pd.read_csv("./day1104/Fish.csv")

# [예제] 물고기의 Length, Height, Width 로 Weight 예측하기
# 1) 예측을 위한 값을 한 데 모음
X = df[['Length2', 'Height','Width']]
# 2) 정답 값 추출
Y = df['Weight']

# 3) 훈련/테스트 세트 만들기
from sklearn.model_selection import GridSearchCV,KFold,train_test_split # 라이브러리 내 특정 함수만 import 가능
# train_test_split( X, Y , test_size = 훈련용 비율, random_state = 42 ) : 예측, 정답 값을 받아 훈련 위한 튜플 자료(X_train,X_test,Y_train,Y_test)로 반환
# radom_state = 42 ? 코드를 다시 실행해도 동일한 결과 나오도록 함.
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

from sklearn.preprocessing import PolynomialFeatures
# PolynomialFeatures(degree = 제곱차수, include_bias=True or False) : 횡적 증식 함수
# 횡적증식 ? 행의 개수(종적증식, 일반적 데이터 증식)가 아닌 열의 개수가 증식
#           적은 칼럼으로 구성된 평면적 데이터를 입체적으로 증식시켜 모델 성능 향상.
# include_bias = True or False ? 입력값 행렬에 상수 1 추가(행렬 연산에서 연산 속도 향상 위함)
poly = PolynomialFeatures(degree=2, include_bias=False)
poly.fit(X_train) # 데이터 변환준비( 데이터 형식을 확인하고 poly에 저장 )
X_train_poly = poly.transform(X_train) # poly에서 설정한 값을 X_train에 적용, .fit()후 .transform()해야함
# = .fit_transform()
X_test_poly = poly.transform(X_test) # test엔 fit하지 않는다.

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit(X_train_poly)
X_train_scaled = ss.transfrom(X_train_poly)
X_test_scaled = ss.transform(X_test_poly)
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit( X_train_scaled , Y_train )
# 7) 결정계수 
print( 'r2 : ' , model.score( X_train_scaled , Y_train ))
print( 'r2 : ' , model.score( X_test_scaled , Y_test ))

from sklearn.pipeline import Pipeline
# Pipeline([("식별자", 클래스명())])
pipe_model = Pipeline([
    ('poly',PolynomialFeatures(degree=2, include_bias=False)), # [4]
    ('scaler',StandardScaler()),                               # [5]
    ('re',LinearRegression())                                  # [6]
    ])
# 9) 파이프라인 으로 학습 
pipe_model.fit( X_train , Y_train )
print( 'r2 : ' , pipe_model.score( X_train , Y_train ))
print( 'r2 : ' , pipe_model.score( X_test , Y_test ))

# [K-fold 기법]
# 1. 파이프라인 만들기
pipe_model = Pipeline([
    ('poly',PolynomialFeatures(degree=2, include_bias=False)), # [4]
    ('scaler',StandardScaler()),                               # [5]
    ('re',LinearRegression())                                  # [6]# 9) 파이프라인 으로 학습 
    ])

param_grid = {'poly__degree':[2,3],'ridge__alpha':[0.001,0.01,0.1,10,100]}
# KFold(n_splits=k개의 동일한 폴드로 분할, shuffle=True or False, random_state = 42)
kf = KFold(n_splits=5, shuffle=True, random_state = 42) # 데이터를 5개로 나누어 4개학습/1개검증 하는 과정을 5번(교차 검증)
# 그리드 서치CV : 교차 검증 및 다양한 파라미터 자동실행하고 최적 성능 모델 찾아줌
grid=GridSearchCV(
    estimator=pipe_model,
    param_grid=param_grid,
    scoring='r2',
    cv = kf,
    n_jobs=-1
)
# 그리드 서치로 학습
grid.fit(X_train,Y_train)
# 주요 속성
best_model = grid.best_estimator_ # 가장 성능 좋은 모델 반환
print(grid.best_params_) # 가장 성능 좋은 파라미터 조합
print(grid.best_score_) # 교차 검증에서 평균 점수 반환
# 최적 모델로 평가
print('r2 : ', best_model.score(X_train,Y_train) )
print('r2 : ', best_model.score(X_test,Y_test) )

# 서빙 : 학습된 모델을 저장하여 다른곳에서 호출
# 고사양GPU(코랩)에서 학습 -> 실제 서버에서 호출
import joblib
# 1) 모델 저장
# joblib.dump(모델, 저장할 경로)
joblib.dump(best_model, './day14/fish_model.pkl')
# 2) 다른 파이썬 파일에서 저장된 모델 불러오기