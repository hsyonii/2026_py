# [ 로지스틱 회귀 ] : 입력데이터를 보고 특정 범주에 속할 확률 구하는 분류 모델
import pandas as pd
df = pd.read_csv('./day1104/Fish.csv')

# 1. 이진분류
# 1) 이진분류 실습위한 정답지 2개만 사용
df = df [ (df['Species'] == 'Bream') | (df['Species']=='Smelt') ]
X = df[['Weight', 'Length1','Length2','Length3','Height','Width']]
Y = df['Species']

# 2) 분리
from sklearn.model_selection import train_test_split
# stratify = Y ? 타깃 무작위 분리 한 경우 클래스(값) 비율 일정 유지, 분류 모델에서 필수 사용
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state = 42,
    stratify = Y
    )

# 3) 스케일링
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit(X_train)
X_train_scaled = ss.transform(X_train)
X_test_scaled = ss.transform(X_test)

# 4) 로지스틱 모델 사용
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
# .fit(입력,정답) : 모델 학습
# .predict(테스트입력값) : 새로운 입력을 넣어 예측값 얻음
model.fit(X_train_scaled, Y_train)
Y_pred = model.predict(X_test_scaled)
print(Y_pred)

# 5) 결과 속성
# 모델.classes_ : 정답 클래스 종류 시리즈로 반환
print(model.classes_)
# 모델.predict_proba(데이터) : 데이터별 각 클래스가 정답일 확률 반환  
print( model.predict_proba(X_test_scaled[:3])) # X_test_scaled 처음인덱스부터 3번인덱스 전까지
# 6) 정확도 평가
# accuracy_score(테스트정답지, 테스트예측값) : 정답지와 예측값을 비교하여 전체개수 대비 맞힌개수로 정확도 평가
from sklearn.metrics import accuracy_score
acc = accuracy_score(Y_test, Y_pred)
print(acc)

