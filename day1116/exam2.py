\xef\xbb\xbf# [ LightGBM 튜닝 / 서빙 ]
# 데이터 셋
# ================================================================
from pathlib import Path

import numpy as np
import pandas as pd
url = 'https://raw.githubusercontent.com/rashida048/Datasets/master/USA_cars_datasets.csv'
df = pd.read_csv(url)

df = df[df['price'] > 0]
num_cols = ['year', 'mileage']                                  # 수치형
cat_cols = ['brand', 'model', 'title_status', 'color', 'state'] # 범주형 분류
# 모델 성능 향상위해 도메인 지식기반 특성(계산식) 추가하면 좋다.

# 문자열형 데이터는 'category'타입으로 변경헤주어야함
# category ? 클래스에 0 ~ 정수 부여하여 구분 -> lightBGM이 정수가 아닌 범주형으로 자동학습
for col in cat_cols:
    df[col] = df[col].astype('category')

X = df[num_cols + cat_cols]
Y = df['price']
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
# ================================================================

# 1. optuna : 파라미터 서치 라이븝러리
import optuna
from lightgbm import LGBMRegressor, early_stopping
optuna.logging.set_verbosity(optuna.logging.WARNING) # 로그 숨기고 경고만 출력

# 2. 탐색방식 설정
# seed=42 ? random_state와 같이 실행시마다 같은 결과 재현
# 2-1. 목적함수 만들기
def objective(trial):
    from sklearn.model_selection import KFold
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_r2_scores=[] # 각 폴드별 검증 점수 저장
    best_iterations=[] # 각 폴드별 최적 트리 번호 저장
    # 한 trial의 모든 폴드에서 동일한 파라미터 조합을 평가
    for train_idx,val_idx in cv.split(X_train, Y_train) :
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        Y_tr, Y_val = Y_train.iloc[train_idx], Y_train.iloc[val_idx]
        model = LGBMRegressor(
            n_estimators=1000,
            # trial.suggest_XXX( '파라미터명' , 시작값, 끝값 )
            learning_rate=trial.suggest_float('learning_rate', 0.01, 0.1),
            num_leaves=trial.suggest_int('num_leaves', 10, 30),
            max_depth=trial.suggest_int('max_depth', 3, 10),
            min_child_samples=trial.suggest_int('min_child_samples', 10, 50),
            subsample=trial.suggest_float('subsample', 0.6, 1.0),
            subsample_freq=1, verbose=-1, random_state=42, n_jobs=-1,
            colsample_bytree=trial.suggest_float('colsample_bytree', 0.6, 1.0),
            # class_weight 회귀모델 이므로 생략
        )
        # 폴더별 훈련용/검증용 학습
        model.fit( X_tr , Y_tr , eval_set=[(X_val, Y_val)],
                  callbacks=[ early_stopping( stopping_rounds=50, verbose=False ) ] )
         # 4-3 교차별 학습 성능 저장
        # K폴드별 검증 평가 r2
        r2 = model.score( X_val , Y_val )
        cv_r2_scores.append( r2 )                       # k폴드별 평가 점수 저장
        best_iterations.append( model.best_iteration_ ) # k폴드별 최적 트리 번호 저장
    # k폴드에서 산출된 최적 트리 개수의 평균값을 trial의 속성으로 저장
    # k폴드만큼 구한 최적의 트리 리스트에서 평균값으로 trial 저장!
    trial.set_user_attr( 'best_n_estimators' , int( np.mean( best_iterations ) ) )
    return np.mean( cv_r2_scores ) # 검증 평가 평균 점수 반환

sampler = optuna.samplers.TPESampler( seed=42 )
# optuna.create_study(direction = 'maximize'or'minimize', sampler=파라미터샘플러)
# direction ? 파라미터조합을 점수를 높이는 or 낮추는 방향으로 찾도록 설정.
# maximize - accuracy, f1, r2 / minimize - MAE, MSE, RMSE
study = optuna.create_study(direction='maximize',sampler=sampler)
# study.optimize( 목적함수, n_trials= 반복수 ) : 반복수만큼 목적함수 실행
study.optimize(objective,n_trials=20)

# 5) 최적 모델
print('최적 하이퍼 파라미터: ', study.best_params)
best_n_estimators = study.best_trial.user_attrs['best_n_estimators']
print('교차검증 평균 r2: ', study.best_value)
optimal_model = study.best_trial.user_attrs['best_n_estimators']
print('최적트리: ', best_n_estimators)

# 6) 최적 파라미터로 모델 학습
final_model = LGBMRegressor(
    random_state=42,verbose = -1, n_jobs=-1,
    **study.best_params, # 최적파라미터 넣기
    n_estimators=best_n_estimators,
    subsample_freq=1
)
final_model.fit(X_train, Y_train)
print('train r2: ', final_model.score(X_train, Y_train))
print('test r2: ', final_model.score(X_test, Y_test))
print(final_model.feature_name_)
print(final_model.feature_importances_)


# 7) jolib 저장 / 로드
import joblib
model_path = Path(__file__).resolve().with_name('gbm_model.pkl')
joblib.dump(final_model, model_path)
model = joblib.load(model_path)

# 8)
new_cars = pd.DataFrame([
    {'year': 2019, 'mileage': 25000, 'brand': 'ford', 'model': 'f-150', 'title_status': 'clean vehicle', 'color': 'white', 'state': 'texas'},
    {'year': 2014, 'mileage': 85000, 'brand': 'nissan', 'model': 'altima', 'title_status': 'salvage insurance', 'color': 'black', 'state': 'california'},
])
for col in cat_cols:
    new_cars[col] = new_cars[col].astype('category')

preds = model.predict(new_cars)
print('서빙모델 예측 (1번차량) 가격: ', preds[0])
print('서빙모델 예측 (2번차량) 가격: ', preds[1])
