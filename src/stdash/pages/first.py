import streamlit  as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
import altair as alt
import numpy as np
import os

def load_data():
    DB = os.getenv('DB')
    DB_PORT =os.getenv('DB_PORT')
    url = f'http://{DB}:{DB_PORT}/all'
    r = requests.get(url)
    d = r.json()
    return d

st.markdown("# First 🌭")

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

tab1, tab2,= st.tabs(['시간 당 요청 수', '시간 당 요청 및 처리 건수'])

with tab1:
    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(df_req.index, df_req['num'], color='steelblue')
    plt.title("Requests by DateTime")
    plt.xlabel('DateTime')
    plt.ylabel('Count Requests')
    plt.xticks(rotation = 45)
    for bar in bars1:
        yval = bar.get_height()  # 막대의 높이 가져오기
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')
    # 화면에 그리기
    st.pyplot(plt)

with tab2:
    plt.figure(figsize=(10, 6))
    plt.bar(df_req.index, df_req['num'], color='orange', label='num of requests')
    plt.plot(df_pre.index,df_pre['num'], color='steelblue', marker='o', label='num of predictions')
    plt.legend(title="NUM")
    plt.title("Requests / Prediction by DateTime")
    plt.xlabel('DateTime')
    plt.ylabel('Count Requests')
    plt.xticks(rotation = 45)
    # 화면에 그리기
    st.pyplot(plt)
