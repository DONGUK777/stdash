import streamlit  as st
import matplotlib.pyplot as plt
import pandas as pd
import requests

# st.subheader('요청 / 처리 건수(h)')

# 탭 생성 : 첫번째 탭의 이름은 Tab A 로, Tab B로 표시합니다. 
tab1, tab2= st.tabs(['시간 당 요청 수' , '시간 당 요청 및 처리 건수'])

def load_data():
    url = 'http://43.202.66.118:8003/all'
    r = requests.get(url)
    d = r.json()
    return d

data = load_data()
df = pd.DataFrame(data)

# 요청 시간 Groupby
df['request_time'] = pd.to_datetime(df['request_time'])
df['req_time'] = df['request_time'].dt.strftime('%Y-%m-%d %H')
df_req = df.groupby('req_time').count()

# 처리 시간 Groupby
df['prediction_time'] = pd.to_datetime(df['prediction_time'])
df['pre_time'] = df['prediction_time'].dt.strftime('%Y-%m-%d %H')
df_pre = df.groupby('pre_time').count()

# TODO
# request_time, prediction_time 이용해 '%Y-%m-%d %H' 형식
# 즉 시간별 GROUP BY CONUNT 하여 plt 차트 그려보기
with tab1:
    plt.bar(df_req.index, df_req['num'], color='black')
    plt.title("Requests by DateTime")
    plt.xlabel('DateTime')
    plt.ylabel('Count Requests')
    plt.xticks(rotation = 45)

    # 화면에 그리기
    st.pyplot(plt)

with tab2:
    plt.bar(df_req.index, df_req['num'], color='orange')
    plt.plot(df_pre.index,df_pre['num'], 'green', marker='o')
    plt.title("Requests / Prediction by DateTime")
    plt.xlabel('DateTime')
    plt.ylabel('Count Requests')
    plt.xticks(rotation = 45)

    # 화면에 그리기
    st.pyplot(plt)
