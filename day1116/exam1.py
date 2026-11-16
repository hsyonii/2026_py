# 데이터셋 가져오기
# ============================================================
import pandas as pd
url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'
df = pd.read_csv(url)
# 피처&타겟 설정
X = df[['alcohol', 'sugar', 'pH']]
Y = df['class'] 
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)
# =============================================================

# 1) 모델만들기
# LightGBM : LGBMClassifier - 분류 / LGBMRegressor - 회귀
from lightgbm import LGBMClassifier
model = LGBMClassifier(
    # 파라미터(설정 값)
    n_estimators=100, # 추정기(개별트리) 개수, 기본값 100
    learning_rate=0.05, # 학습률 : 각 트리의 반영 비율, 기본값 0.1
                        # -> 학습률이 작으면 더 많은 트리 필요, 너무 많은 트리를 작은 학습률로 학습하면 과적합될수도 있음.
    num_leaves=15, # 트리별 최대 리프 노드개수
    max_depth=6,
    min_child_samples=20 , # 리프 노드 최소 샘플 수
    subsample=0.8, # 학습(트리)마다 랜덤으로 전체데이터(행) 80%만 사용 -> 계산값 반올림 하여 사용
    subsample_freq=1, # 랜덤 데이터 교체 주기( ex - 1이면 트리 1개마다 데이터 다시 뽑기 ), 기본값0으로 subsample과 꼭 같이 설정!!
    colsample_bytree=0.8, # 학습마다 랜덤으로 전체피처(열) 80% 사용
    class_weight="balanced", # 분류모델에서 클래스 비율 불균형 완화(소수 클래스에 가중치 부여)
    random_state=42,
    n_jobs=-1, # 학습시 CPU 최대값 사용
    verbose=-1 # 학습 로그 숨김
    )

# 2) 모델 학습 수행
# eval_set = [( 테스트데이터 )] : 학습도중 모델 성능확인 위해 지정하는 데이터 인자
# callbacks = [ 모델학습중 실행할 기능 ]
# early_stopping(stopping_rounds = n ) : 학습 조기 종료
# stopping_rounds ? 성능최고기록 n 회이상 미갱신시 학습중단, 기록 갱신시 0부터 다시 센다.
from lightgbm import early_stopping
model.fit(X_train, Y_train, # 학습에 사용할 데이터
          eval_set=[(X_test,Y_test)], # 테스트(성능평가)에 사용할 데이터
          callbacks=[early_stopping(stopping_rounds = 50, verbose=False)] # 콜백( 조기종료 )
          )
# -> 손실함수 결과 오차 최적되면 중단

# 3) 학습 결과 확인
print(model.best_iteration_) # 최적의 트리 반복수, 최종 번호
print(model.feature_name_) # 피처목록 반환
print(model.feature_importances_) # 피처별 중요도 반환

# 4) 학습한 모델로 예측, 평가지표
from sklearn.metrics import f1_score
# X_train,Y_train,X_test,Y_test : 실제 데이터(모두정답) / Y_pred : X_test로 예측한 답안지(정답지 - Y_test)
Y_pred = model.predict(X_test)
# 모델은 데이터가 아닌 규칙만을 학습함. -> 학습에 사용했던 데이터를 넣은 성능평가도 유의미.
print(model.score(X_train,Y_train)) # X_train으로 예측, Y_train으로 채점 -> 트레인 셋 정확도
print(model.score(X_test,Y_test)) # -> 테스트 셋 정확도
print(f1_score(Y_test,Y_pred,average='macro')) # f1_score(정답, 예측, average = 'macro') : 예측과 정답을 비교하여 f1종합점수(precision,recall)
# average='macro' ? 각 클래스의 점수의 산술평균( 클래스별 데이터 개수에 비중두지 않고 동일한 비중 )

# 5) 정답없는 데이터에 모델 실제로 사용하기
new_wine = pd.DataFrame([[11.5, 2.3, 3.1], [13.8, 11.2, 3.3]])
new_pred = model.predict(new_wine)
print('예측1 : ',new_pred[0]) # 레드
print('예측2 : ',new_pred[1]) # 화이트
