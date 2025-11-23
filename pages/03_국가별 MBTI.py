import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# 데이터 불러오기
# -----------------------
df = pd.read_csv("/mnt/data/countriesMBTI_16types.csv")

st.title("🌍 국가별 MBTI 비율 시각화")

# 국가 선택
countries = df['Country'].unique()
selected_country = st.selectbox("국가를 선택하세요", countries)

# 선택된 국가 데이터 필터링
country_df = df[df["Country"] == selected_country]

# MBTI 퍼센트 컬럼만 추출
mbti_cols = [col for col in df.columns if col != "Country"]
country_df = country_df[mbti_cols].T.reset_index()
country_df.columns = ["MBTI", "Percentage"]

# -----------------------
# 색상 설정: 1등 파란색, 나머지는 그라데이션
# -----------------------
country_df = country_df.sort_values("Percentage", ascending=False)

top_color = "rgba(0, 80, 255, 1)"   # 1등 진파란색
gradient_colors = [
    f"rgba(0, 80, 255, {0.15 + 0.7*(i/len(country_df))})"
    for i in range(len(cou
