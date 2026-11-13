# [ 1. 의사 결정 나무 ]
# : 단계별로 분기되어 최종단계에서 예측을 내리는 모델
# - 분류&회귀 모델 모두 가능
# - 스케일링 필요 X (전처리 단순하다.)
# - 깊이가 너무 깊으면 과적합 -> 규제 필요
import pandas as pd

# 와인 더미 데이터
url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'
df = pd.read_csv(url)

# alcohol, sugar, pH, class( 0: 레드 / 1: 화이트 )
X = df[ ['alcohol','sugar', 'pH'] ] # 피처(독립변수)
Y = df[ 'class' ] # 타깃(종속변수)
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 1) 결정 트리 모델
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
# 타깃 : ~~Classifier - 범주형 / ~~Regressor - 연속형
# 예) 타깃인 'class'가 0,1 -> 범주형
model = DecisionTreeClassifier()
model.fit(X_train,Y_train) # 분할 조건(가지치기) 자동 생성
print("Train Acc : ", model.score(X_train,Y_train)) # Accuracy(정확도)
print("Train Acc : ", model.score(X_test,Y_test))
# 출력)
# Train Acc :  0.996921300750433
# Train Acc :  0.8530769230769231 -> 훈련&테스트 세트 간 점수차 10%이상이면 과적합(규제 필요)

# 2) 트리 시각화
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
# plot_tree(모델, max_depth = n) : 트리 모델 시각화
# max_depth ? 모델 깊이 설정(생략 가능)
plot_tree(model,max_depth=2)
plt.show()

# 4) 타깃 클래스의 불균형
model = DecisionTreeClassifier(
    max_depth=3, # 깊이 제한
    min_samples_leaf=10, # 리프(최하위 분기)별 학습데이터 최소 개수
                         # -> 숫자를 크게 설정할수록 데이터가 과도하게 세세히 나뉘는것 막음.(트리 복잡도 낮춤)
    criterion="gini", # 분기 기준 설정 -> 분할별 지니 불순도가 낮아지도록 분기 기준 학습
                      # gini 불순도 ? 한 그룹 내 여러 클래스가 섞여있는 정도
                      # DecisionTreeClassifier에서 기본값은 gini
    random_state=42,
    class_weight='balanced' # 빈도낮은 클래스에 가중치 부여(불균형 보정)
)
model.fit(X_train,Y_train)
print("Train Acc: ",model.score(X_train, Y_train))
print("Test Acc: ", model.score(X_test,Y_test)) # 정확도 = 맞힌 개수 / 전체 개수
# Train대비 Test점수가 많이 저조하면? Train에만 잘맞는 '과적합'!!

# 5) 특성 중요도
print(model.feature_names_in_) # 피처명 시리즈로 반환
print(model.feature_importances_) # 피처별 예측 기여의 중요도 

# [ 2. 앙상블 ]
# : 여러모델을 조합하여 학습하는 복합 모델 구현
# - 배깅? 여러모델을 병렬학습 -> 모델별 결과를 보팅/확률평균 통해 결과, 랜덤 포레스트
# - 부스팅 ? 직렬 학습 -> 이전모델의 오답에 가중치 부여하여 다음 모델이 학습.

# 1) 랜덤 포레스트( 배깅 ) 
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(
    max_depth=3,
    class_weight="balanced",
    n_estimators= 100, # 생성할 결정 트리개수( 기본값 100, 일반적으로 1000~3000)
    max_features='sqrt', # 각노드에서 분할시 특성의 최대개수, 분류 : sqrt(제곱근) / 회기: log2 )
                         # 최대개수 만큼 랜덤으로 선택된 피처기준으로 모델 학습 -> 최대한 다양한 트리를 만들기 위함
    random_state=42,
    n_jobs=-1 # CPU 최대 사용
 )
model.fit(X_train,Y_train)
print("Train Acc: ",model.score(X_train, Y_train))
print("Test Acc: ", model.score(X_test,Y_test))

print(model.feature_names_in_)
print(model.feature_importances_)