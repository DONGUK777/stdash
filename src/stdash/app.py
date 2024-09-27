import streamlit  as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
import altair as alt
import numpy as np
import os


st.title('CNN JOB MON')
st.header('왼쪽의 버튼을 클릭하세요')
st.header('목차')
st.subheader('First')
st.subheader('Second')

# 탭 생성 : 첫번째 탭의 이름은 Tab A 로, Tab B로 표시합니다. 
tab1, tab2,= st.tabs(['시간 당 요청 수', '시간 당 요청 및 처리 건수'])
tab3, tab4 = st.tabs(['요청 및 처리의 차이', 'USER별 불균형 확인'])
def load_data():
    DB = os.getenv('DB')
    DB_PORT =os.getenv('DB_PORT')
    url = f'http://{DB}:{DB_PORT}/all'
    r = requests.get(url)
    d = r.json()
    return d

st.sidebar.title('🐵DONGUK777 Analysis🤖')

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

def step1():
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

if st.sidebar.button('First'):
    step1()        

def step2():
    with tab3:
        
        # 요청 시간과 처리 시간을 합쳐서 계산할 데이터프레임 생성
        all_times = sorted(list(set(df_req.index).union(df_pre.index)))  # 모든 시간대를 포함하는 정렬된 리스트 생성
        df_dif = pd.DataFrame(index=all_times)  # 정렬된 시간 리스트를 인덱스로 사용
        df_dif['num_of_requests'] = df_req['num']
        df_dif['num_of_predictions'] = df_pre['num']

        # NaN 값을 0으로 대체 (데이터가 없는 시간은 0으로 처리)
        df_dif.fillna(0, inplace=True)

        # 요청과 처리 차이 계산
        df_dif['difference'] = df_dif['num_of_requests'] - df_dif['num_of_predictions']

        # 누락된 주체 확인
        # 요청수가 더 많으면 red, 처리수가 더 많으면 bule
        colors = ['orange' if x > 0 else 'steelblue' for x in df_dif['difference']]

        conditions = [
            df_dif['difference'] > 0,  # 과다 요청
            df_dif['difference'] < 0   # 처리 누락
        ]
        choices = ['과다 요청', '처리 누락']
        
        # 불균형 정보 데이터프레임 출력
        st.write(df_dif[['num_of_requests', 'num_of_predictions', 'difference', 'missing_info']])
        
        df_dif['missing_info'] = np.select(conditions, choices, '정상 처리')
        plt.figure(figsize=(10, 6))
        plt.bar(df_dif.index, df_dif['difference'], color=colors)
        plt.axhline(0, color='black', linewidth=1, linestyle='-')  # 검은색 점선
        plt.title("Count of Difference")
        plt.xlabel('DateTime')
        plt.ylabel('Count')
        plt.xticks(rotation = 45)
        
        st.pyplot(plt)


    with tab4:
        
        # prediction_model이 n으로 시작하는 것들만 추출
        plt.figure(figsize=(10, 6)) # 여기에서 새로운 그림 생성
        df['prediction_model'] = df['prediction_model'].astype(dtype='str')

        def func(x):
            if x[0] == 'n':
                return x
        df2 = df['prediction_model'].map(func).to_frame()

        # prediction 유저 수
        pre_usr = df2.value_counts()
        # request 유저 수
        req_usr = df[['request_user']].value_counts()

        df_usr = pd.concat([req_usr, pre_usr], axis = 1)
        df_usr.columns = ['req_count', 'pre_count']
        df_usr = df_usr.reset_index()
        df_usr = df_usr.set_index('level_0')
        df_usr = df_usr.fillna(0)    
        
        w = 0.25
        ind = np.arange(len(df_usr))
        plt.bar(ind - w, df_usr['req_count'], width = w+0.1, label = 'request count', color = 'orange')
        plt.bar(ind + w, df_usr['pre_count'], width = w+0.1, label = 'predict count', color = 'steelblue')
        plt.xticks(ind, labels = df_usr.index)
        plt.xlabel('User')
        plt.ylabel('Count')
        plt.legend()
        st.pyplot(plt)

if st.sidebar.button('Second'):
    step2()
