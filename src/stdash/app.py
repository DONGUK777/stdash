import streamlit  as st
import matplotlib.pyplot as plt
import pandas as pd
import requests

st.title('CNN JOB MON')

def load_data():
    url = 'http://43.202.66.118:8003/all'
    r = requests.get(url)
    d = r.json()
    return d

data = load_data()
df = pd.DataFrame(data)

# TODO
# request_time, prediction_time 이용해 '%Y-%m-%d %H' 형식
# 즉 시간별 GROUP BY CONUNT 하여 plt 차트 그려보기

df['request_time'] = pd.to_datetime(df['request_time'])
df['req_time'] = df['request_time'].dt.strftime('%Y-%m-%d %H')
df_req = df.groupby('req_time').count()

df['prediction_time'] = pd.to_datetime(df['prediction_time'])
df['pre_time'] = df['prediction_time'].dt.strftime('%Y-%m-%d %H')
df_pre = df.groupby('pre_time').count()

plt.bar(df_req.index, df_req['num'], color='orange')
plt.plot(df_pre.index,df_pre['num'], 'green', marker='o')
plt.xlabel('DateTime')
plt.ylabel('Count Requests')
plt.xticks(rotation = 45)

# 화면에 그리기
st.pyplot(plt)
