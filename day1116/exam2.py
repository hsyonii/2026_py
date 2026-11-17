# [ LightGBM ?쒕떇 / ?쒕튃 ]
# ?곗씠????
# ================================================================
from pathlib import Path

import numpy as np
import pandas as pd
url = 'https://raw.githubusercontent.com/rashida048/Datasets/master/USA_cars_datasets.csv'
df = pd.read_csv(url)

df = df[df['price'] > 0]
num_cols = ['year', 'mileage']                                  # ?섏튂??
cat_cols = ['brand', 'model', 'title_status', 'color', 'state'] # 踰붿＜??遺꾨쪟
# 紐⑤뜽 ?깅뒫 ?μ긽?꾪빐 ?꾨찓??吏?앷린諛??뱀꽦(怨꾩궛?? 異붽??섎㈃ 醫뗫떎.

# 臾몄옄?댄삎 ?곗씠?곕뒗 'category'??낆쑝濡?蹂寃쏀뿤二쇱뼱?쇳븿
# category ? ?대옒?ㅼ뿉 0 ~ ?뺤닔 遺?ы븯??援щ텇 -> lightBGM???뺤닔媛 ?꾨땶 踰붿＜?뺤쑝濡??먮룞?숈뒿
for col in cat_cols:
    df[col] = df[col].astype('category')

X = df[num_cols + cat_cols]
Y = df['price']
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
# ================================================================

# 1. optuna : ?뚮씪誘명꽣 ?쒖튂 ?쇱씠釉앸윭由?
import optuna
from lightgbm import LGBMRegressor, early_stopping
optuna.logging.set_verbosity(optuna.logging.WARNING) # 濡쒓렇 ?④린怨?寃쎄퀬留?異쒕젰

# 2. ?먯깋諛⑹떇 ?ㅼ젙
# seed=42 ? random_state? 媛숈씠 ?ㅽ뻾?쒕쭏??媛숈? 寃곌낵 ?ы쁽
# 2-1. 紐⑹쟻?⑥닔 留뚮뱾湲?
def objective(trial):
    from sklearn.model_selection import KFold
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_r2_scores=[] # 媛??대뱶蹂?寃利??먯닔 ???
    best_iterations=[] # 媛??대뱶蹂?理쒖쟻 ?몃━ 踰덊샇 ???
    # ??trial??紐⑤뱺 ?대뱶?먯꽌 ?숈씪???뚮씪誘명꽣 議고빀???됯?
    for train_idx,val_idx in cv.split(X_train, Y_train) :
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        Y_tr, Y_val = Y_train.iloc[train_idx], Y_train.iloc[val_idx]
        model = LGBMRegressor(
            n_estimators=1000,
            # trial.suggest_XXX( '?뚮씪誘명꽣紐? , ?쒖옉媛? ?앷컪 )
            learning_rate=trial.suggest_float( 'learning_rate' , 0.01 , 0.1 )  ,
            num_leaves=trial.suggest_int( 'num_leaves' , 10, 30 ),
            max_depth=trial.suggest_int( 'max_depth' , 3 , 10 ),
            min_child_samples=trial.suggest_int( 'min_child_samples', 10 , 50 ),
            subsample=trial.suggest_float( 'subsample' , 0.6 , 1.0 ) ,
            subsample_freq=1, verbose=-1,random_state=42, n_jobs=-1 ,
            colsample_bytree=trial.suggest_float('colsample_bytree',0.6,1.0),
            # class_weight ?뚭?紐⑤뜽 ?대?濡??앸왂
        )
        # ?대뜑蹂??덈젴??寃利앹슜 ?숈뒿
        model.fit( X_tr , Y_tr , eval_set=[ (X_val,Y_val)] ,
                  callbacks=[ early_stopping( stopping_rounds=50, verbose=False ) ] )
         # 4-3 援먯감蹂??숈뒿 ?깅뒫 ???
        # K?대뱶蹂?寃利??됯? r2
        r2 = model.score( X_val , Y_val )
        cv_r2_scores.append( r2 )                       # k?대뱶蹂??됯? ?먯닔 ???
        best_iterations.append( model.best_iteration_ ) # k?대뱶蹂?理쒖쟻 ?몃━ 踰덊샇 ???
    # k?대뱶?먯꽌 ?곗텧??理쒖쟻 ?몃━ 媛쒖닔???됯퇏媛믪쓣 trial???띿꽦?쇰줈 ???
    # k?대뱶留뚰겮 援ы븳 理쒖쟻???몃━ 由ъ뒪?몄뿉???됯퇏媛믪쑝濡?trial ???
    trial.set_user_attr( 'best_n_estimators' , int( np.mean( best_iterations ) ) )
    return np.mean( cv_r2_scores ) # 寃利??됯? ?됯퇏 ?먯닔 諛섑솚

sampler = optuna.samplers.TPESampler( seed=42 )
# optuna.create_study(direction = 'maximize'or'minimize', sampler=?뚮씪誘명꽣?섑뵆??
# direction ? ?뚮씪誘명꽣議고빀???먯닔瑜??믪씠??or ??텛??諛⑺뼢?쇰줈 李얜룄濡??ㅼ젙.
# maximize - accuracy, f1, r2 / minimize - MAE, MSE, RMSE
study = optuna.create_study(direction='maximize',sampler=sampler)
# study.optimize( 紐⑹쟻?⑥닔, n_trials= 諛섎났??) : 諛섎났?섎쭔??紐⑹쟻?⑥닔 ?ㅽ뻾
study.optimize(objective,n_trials=20)

# 5) 理쒖쟻 紐⑤뜽
print('理쒖쟻 ?섏씠???뚮씪誘명꽣: ', study.best_params)
best_n_estimators = study.best_trial.user_attrs['best_n_estimators']
print('援먯감寃利??됯퇏 r2: ', study.best_value)
optimal_model = study.best_trial.user_attrs['best_n_estimators']
print('理쒖쟻?몃━: ', best_n_estimators)

# 6) 理쒖쟻 ?뚮씪誘명꽣濡?紐⑤뜽 ?숈뒿
final_model = LGBMRegressor(
    random_state=42,verbose = -1, n_jobs=-1,
    **study.best_params, # 理쒖쟻?뚮씪誘명꽣 ?ｊ린
    n_estimators=best_n_estimators,
    subsample_freq=1
)
final_model.fit( X_train , Y_train )
print( 'train r2: ', final_model.score( X_train , Y_train ) )
print( 'test r2: ', final_model.score( X_test , Y_test ) )
print( final_model.feature_name_ )
print( final_model.feature_importances_ )


# 7) jolib ???/ 濡쒕뱶
import joblib
model_path = Path(__file__).resolve().with_name('gbm_model.pkl')
joblib.dump(final_model, model_path)
model = joblib.load(model_path)

# 8)
new_cars = pd.DataFrame([
    {'year': 2019, 'mileage': 25000, 'brand': 'ford',   'model': 'f-150',  'title_status': 'clean vehicle',     'color': 'white', 'state': 'texas'},
    {'year': 2014, 'mileage': 85000, 'brand': 'nissan', 'model': 'altima', 'title_status': 'salvage insurance', 'color': 'black', 'state': 'california'}
])
for col in cat_cols:
    new_cars[col] = new_cars[col].astype('category')

preds = model.predict(new_cars)
print('?쒕튃紐⑤뜽 ?덉륫 (1踰덉감?? 媛寃? ', preds[0])
print('?쒕튃紐⑤뜽 ?덉륫 (2踰덉감?? 媛寃? ', preds[1])
