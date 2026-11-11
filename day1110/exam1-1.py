import joblib

# 1) 모델 불러오기
# joblib.load('파일경로')
model = joblib.load('./day1110/fish_model.pkl')

# 2) 모델 테스트( 임의의 입력값 넣어 예측값 출력하기 )
import pandas as pd
sample = pd.DataFrame({"Length2":[32], "Height":[10], 'Width': [4]})
predict = model.predict(sample)
print(predict)