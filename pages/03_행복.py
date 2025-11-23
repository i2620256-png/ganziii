# Streamlit app for exploring Happiness.csv
# Place this file under the repository path: pages/happiness_app.py
# Place the CSV file in the parent folder of pages: ../Happiness.csv

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO

st.set_page_config(page_title="Happiness Explorer", layout="wide")

st.title("Happiness 데이터 탐색기")
st.markdown(
    "CSV 파일: `../Happiness.csv` — 이 파일이 pages 폴더의 상위 폴더에 있어야 합니다.")

@st.cache_data
def load_data(path="../Happiness.csv"):
    df = pd.read_csv(path)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()

# 기본 정보 출력
with st.expander("원본 데이터 보기 / 기본 정보"):
    st.subheader("원본 샘플")
    st.dataframe(df.head(50))

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
non_numeric = [c for c in df.columns if c not in numeric_cols]

st.subheader("요약 통계 및 결측치")
col1, col2 = st.columns([2,1])
with col1:
    if numeric_cols:
        desc = df[numeric_cols].describe().T
        st.dataframe(desc)
    else:
        st.info("숫자형 컬럼이 없습니다.")
with col2:
    st.write("결측치 합계")
    miss = df.isnull().sum()
    st.dataframe(miss[miss>0])

# country selection
country_col = None
for candidate in ["Country", "country", "country_name", "Location"]:
    if candidate in df.columns:
        country_col = candidate
        break

if country_col is None:
    st.error("데이터에 'Country' 컬럼이 없습니다. 국가별 집계를 위해 'Country' 컬럼이 필요합니다.")
    st.stop()

countries = sorted(df[country_col].dropna().unique())
selected_country = st.selectbox("국가 선택", countries)

# compute per-country means (for numeric columns)
country_means = df.groupby(country_col)[numeric_cols].mean()
if selected_country not in country_means.index:
    st.warning("선택한 국가에 충분한 데이터가 없습니다.")
    st.stop()

selected_means = country_means.loc[selected_country]

# build bar chart with special coloring: top=red, others gradient
items = selected_means.index.tolist()
values = selected_means.values.astype(float)

# find index of max
max_idx = int(np.nanargmax(values))

# helper: i
