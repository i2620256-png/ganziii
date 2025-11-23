import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# CSV 불러오기
df = pd.read_csv("/mnt/data/countriesMBTI_16types.csv")

st.title("🌍 국가별 MBTI 비율 시각화 (Plotly)")

# 국가 선택
countries = df["Country"].unique()
selected_country = st.selectbox("국가를 선택하세요!", countries)

# 선택한 국가의 데이터 가져오기
data = df[df["Country"] == selected_country].iloc[0]

mbti_types = df.columns[1:]   # MBTI 16개 타입
values = data[1:].astype(float).values

# 정렬 후 1등 찾기
sorted_idx = np.argsort(values)[::-1]
top_idx = sorted_idx[0]

# 색상: 1등 파란색, 나머지 그라데이션
colors = []
for i in range(len(values)):
    if i == top_idx:
        colors.append("rgba(0, 102, 255, 1)")  # 파란색
    else:
        brightness = 0.3 + (i / len(values)) * 0.5
        colors.append(f"rgba(50, 50, {int(brightness * 255)}, 0.8)")

# Plotly 막대그래프
fig = go.Figure(
    data=[
        go.Bar(
            x=mbti_types,
            y=values,
            marker_color=colors
        )
    ]
)

fig.update_layout(
    title=f"{selected_country} MBTI 비율",
    xaxis_title="MBTI",
    yaxis_title="비율 (%)",
    template="simple_white"
)

st.plotly_chart(fig)
