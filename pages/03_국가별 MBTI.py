import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV 불러오기
df = pd.read_csv("/mnt/data/countriesMBTI_16types.csv")

st.title("🌍 국가별 MBTI 비율 시각화")

# 국가 목록 만들기
countries = df["Country"].unique()
selected_country = st.selectbox("국가를 선택하세요!", countries)

# 선택한 국가 데이터 필터링
country_data = df[df["Country"] == selected_country].iloc[0]

# MBTI와 비율만 추출
mbti_types = df.columns[1:]  # Country 제외 16개 타입
values = country_data[1:].astype(float).values

# 정렬해서 1등 찾기
sorted_idx = np.argsort(values)[::-1]
top_idx = sorted_idx[0]

# 색깔 지정: 1등은 파란색, 나머지는 그라데이션
colors = []
for i in range(len(values)):
    if i == top_idx:
        colors.append("blue")
    else:
        # 0.3~0.8 사이 밝기 그라데이션
        brightness = 0.3 + (i / len(values)) * 0.5
        colors.append((0.2, 0.2, brightness))

# 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(mbti_types, values, color=colors)
ax.set_ylabel("비율 (%)")
ax.set_title(f"{selected_country} MBTI 비율")
plt.xticks(rotation=45)

st.pyplot(fig)
