import seaborn as sns
# 1) seaborn에서 더미 데이터 가져오기
df = sns.load_dataset('penguins')
df.info()

# 2) 전처리 - 결측치 제거
df.dropna().reset_index # 결측행제거하고 인덱스 맞춤
df.info()

# 3) 다중분류 실습 위한 특성 / 타깃
X = df.drop(columns=['species']) # '종'을 제외한 나머지 특성을 X
Y = df['species'] # '종'을 Y

# 4)
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=42)

# 5) 복합형 파이프라인(수치형 + 범주형) 위한 수치형과 범주형 분리
num_features = ['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g'] # 수치형
cat_features = ['island', 'sex'] # 범주형

# 6) 복합 특성 
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# ColumnTransformer(transformers=[('식별자', 변환기, 컬럼목록)])
# OneHotEncoder() : 범주형 자료들을 각각 새로운 컬럼으로 만들어 0,1로 표현
# drop = 'first' : 전체 데이터가 0이면 첫번째 범주로 인정. ( 첫번째 범주에 대한 새 칼럼 만들지 않는다. )
# sparse_output=False : 변환된 자료들을 numpy로 변환
pp = ColumnTransformer(transformers=[('num', StandardScaler() , num_features ),
                                     ('cat', OneHotEncoder(drop='first',sparse_output=False), cat_features )])

# 7) 파이프 라인만들기
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
# Pipeline([('식별자', 변환기/모델 )])
pipe = Pipeline([('pp',pp),('model', LogisticRegression(C=1.0))])
pipe.fit(X_train)