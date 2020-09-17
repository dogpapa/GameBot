# 라이브러리
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from lightgbm import LGBMClassifier
import joblib
from sklearn.metrics import classification_report

# Unique ID -> Actore
df = pd.read_csv("C:/Users/pc/Desktop/Jupyter/01. 개인공부/SK_infosec/게임봇탐지/WORKSPACE/AION Game data set file(raw).csv", index_col = 'Actor')

# 정규화 과정
scaler = joblib.load('gamebot_scaler.pkl')

# scaler.fit(df)
df_scaled = pd.DataFrame(scaler.transform(df), columns = df.columns)
df_scaled.set_index(df.index, inplace = True)

# 모델 -> LGBM 알고리즘(GridsearchCV 하이퍼파라미터 적용)
model = joblib.load('gamebot_model.pkl')
pred = model.predict(df_scaled)

# 예측
pred = pd.DataFrame({'Prediction':pred})

# 결과
save01 = df[['same_point_connection_rate','Login_day_count','playtime_per_day','avg_money','Item_get_ratio','Exp_get_ratio']].reset_index()
save02 = pd.concat([save01, pred], axis = 1)

def change_output(data):
    if data == 0:
        return 'Human'
    else:
        return 'Gamebot'

save02['Prediction'] = save02['Prediction'].apply(change_output)

# 최종 아웃풋 파일
save02.rename(columns = {'same_point_connection_rate':'Same ip Login ratio','Login_day_count':'Login Day count(max=88)',
                         'playtime_per_day':'Play Time per Day','avg_money':'Average Money','Item_get_ratio':'Item Get ratio',
                         'Exp_get_ratio':'Exp. Get ratio','Prediction':'Type'}, inplace = True)

# Index는 Unique
save02.set_index(save02.Actor, inplace = True)
save02.drop(columns = 'Actor', inplace = True)

# 화면(봇 유저만 출력)
cond = (save02['Type'] == 'Gamebot')
output = save02.loc[cond]

##################################################

df = save02[save02.columns.difference(['Type'])]
tg = save02[['Type']].reset_index()

# 정규화 스케일링 작업
scaler = MinMaxScaler()
scaler.fit(df)
df_scaled = pd.DataFrame(scaler.transform(df), columns = df.columns)

# 데이터프레임 작업
dftg = pd.concat([df_scaled, tg], axis = 1)
dftg.set_index('Actor')

# 휴먼 유저
cond_human = (dftg['Type'] == 'Human')
human = dftg.loc[cond_bot]

# 휴먼 유저 육각형 특성값(중앙값 기준)
human_money = human['Average Money'].median()
human_exp = human['Exp. Get ratio'].median()
human_item = human['Item Get ratio'].median()
human_login = human['Login Day count(max=88)'].median()
human_playtime = human['Play Time per Day'].median()
human_ip = human['Same ip Login ratio'].median()

# 샘플 데이터 (448753 <- 확인하고자 하는 데이터의 인덱스 입력)
if 448753 in output.index:
    bot_money = bot['Average Money'].median()
    bot_exp = bot['Exp. Get ratio'].median()
    bot_item = bot['Item Get ratio'].median()
    bot_login = bot['Login Day count(max=88)'].median()
    bot_playtime = bot['Play Time per Day'].median()
    bot_ip = bot['Same ip Login ratio'].median()    
    print("완료")
else:
    print("오류")