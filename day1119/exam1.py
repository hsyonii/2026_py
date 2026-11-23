# 데이터셋
import pandas as pd
url = "https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt"
df = pd.read_table(url, names=['rating', 'review'])
# 평점 3 제외
df = df[df['rating'] != 3]
# 평점 4이상은 긍정
df['label'] = (df['rating'] >= 4).astype(int)
# 5000개 데이터 샘플
df_sample = df.sample(n=10000, random_state=42).reset_index(drop=True)
print(df_sample.shape)
print(df_sample.head(3))

# 1) 텍스트 전처리 : 정규 표현식
# 정규표현식? 특정 문자열을 찾거나 바꾸는 규칙
# re.sub(r'[ 표현식 ]', 치환문자)
import re

cleaned_list = [] # 걸러진 목록
for text in df_sample['review']:
    text = re.sub(r'[ ^가-힣a-zA-Z0-9\s ]','',str(text))
    # .join() : 각 리스트 항목 사이에 특정 문자 연결 
    # vs 
    # .split() : 문자열내 특정문자 기준 분리하여 리스트 반환
    cleaned_text = ' '.join(text.split())
    cleaned_list.append=(cleaned_text)

df_sample['cleaned_review'] = cleaned_list
print(df_sample.head(3))

# 2) (kiwi) 한국어 형태소 분석기
from kiwipiepy import Kiwi
kiwi = Kiwi()
kiwi.add_user_word(word,'NNG')

from kiwipiepy.utils import Stopwords
kiwi_stopwords = Stopwords()
custom_stopwords = {'그냥','그저','모른다.'}
def tokenize_kiwi(text):
    tokens = kiwi.tokenize(text,stopwords=kiwi_stopwords)
    target_tags = {'NNG','NNP','VV','VA','MAG'}
    result = []
    for t in tokens : 
        if t.tag in target_tags and t.form not in custom_stopwords :
            if len(t.form) > 1 or t.form in {'못','잘'}:
                word = t.form +'다' if t.tag in { 'VV', 'VA'} else t.form
                result.append(word)
    return result

test_word = df_sample['cleaned_review'].iloc[0]
print(test_word)
print(tokenize_kiwi(test_word))
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(
    df_sample['cleaned_review'],df_sample['label'],
    random_state=42,
    stratify=df_sample['label'],
    test_size=0.2
)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(
    tokenizer=tokenize_kiwi,
    token_pattern=None,
    )
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)
print(X_train_tfidf.shape)
print(X_test_tfidf.shape)

# 긍정부정
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(C=1.0,max_iter=1000,random_state=42)
print(model.fit(X_train_tfidf,Y_train))
print(model.score(X_test_tfidf,Y_test))
Y_pred = model.predict(X_test_tfidf)

from sklearn.metrics import f1_score
print('f1: ',f1_score(Y_test, Y_pred))

print(X_train_tfidf.toarray()[0][:10])

new_reviews = [
    "배송도 정말 빠르고 가성비 최고입니다! 재구매 의사 있어요.",
    "마감 상태가 엉망이고 실밥이 다 터져서 왔네요. 최악입니다.",
    "그냥 가격만큼 하는 것 같아요. 특별히 좋지도 나쁘지도 않음."
]
cleaned_new =[]
for text in new_reviews:
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]','',str(text))
    cleaned_new.append(''.join(text.split()))
new_tfidf = tfidf.transform(cleaned_new)

probs = model.predict(new_tfidf)
for i in range(len(new_reviews)):
    pos = probs[i][1]
    if pos >=0.6 : 
        contents = '긍정ㅇ'
    elif pos<=0.4:
        contents = '부정'
    else :
        contents=' 중립'
    print(f'리뷰',{new_reviews[i]})
    print(f'감성분석:, {contents},긍정확률: {pos},부정확률:{probs})
    
    