import streamlit  as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
import altair as alt
import numpy as np
import os

import streamlit as st
from PIL import Image
import requests

# 페이지 기본 설정
st.set_page_config(
    page_title="Donguk Dashboard",  # 페이지 타이틀
    page_icon="🌭",  # 페이지 아이콘
    layout="wide",  # 페이지 레이아웃 ('wide', 'centered' 가능)
    initial_sidebar_state="expanded"  # 사이드바 기본 설정 ('expanded', 'collapsed' 가능)
)

# 1. 제목 및 설명
st.title("📊 Streamlit Dashboard")
st.subheader("Welcome to my Streamlit Analysis Dashboard!")
st.markdown("""
이 대시보드는 이미지 처리 시스템의 요청/처리 결과를 나타냅니다.
왼쪽 사이드바를 통해 다양한 분석과 분석 항목을 확인할 수 있습니다.
""")
