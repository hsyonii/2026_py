# 2) 부스팅 - GBM
url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'

import pandas as pd

df = pd.read_csv(url)
# alcohol,sugar,pH,class( 0:레드 / 1:화이트 )
X = df[ ['alcohol', 'sugar' , 'pH']]    # 독립변수
Y = df[ 'class' ]                       # 종속변수 

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42,stratify=Y) # 분할 

# 2-1) GBM
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
# 모델비교
# learning_rate : 경사하강법에서 오차 보정하기위한 이동단위, 학습률( 기본값 0.1 )
# LightGBM 에서 max_depth 기본값 -1(무제한) -> 과대적합 주의
# verbose = -1 : 실행중 트리 처리 로그 끄기
model = {
    "XGBoost" : XGBClassifier( n_estimators = 100, learning_rate = 0.05, max_depth = 4, random_state = 42, n_jobs =-1 ), # n_estimators에서 설정한 값이전에 최적모델 탐색되면 중단
    "LightGBM" : LGBMClassifier( n_estimators=100, learning_rate= 0.05,max_depth = 4, random_state = 42, n_jobs =-1, verbose = -1 )
}
import time
from sklearn.metrics import f1_score
for name, model in models.items() :
    start = time.time()
    model.fit(X_train, Y_train)
    end = time.time() - start # 학습 소요시간 계산 
    Y_pred = model.predict(X_test) # 예측
    print("======= 모델명 : ", name )
    print("> 학습 소요 시간 : ", end,"초")
    print("> train acc : ", model.score(X_train, Y_train))
    print("> test acc : ", model.score(X_test, Y_test))
    print("> f1 score : ",f1_score(Y_test,Y_pred))