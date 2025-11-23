# pages/축제_분석.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="축제별 방문객 분석", page_icon="📊")

st.title("📊 축제별 방문객 구성 (현지 / 외지 / 외국)")
st.write("CSV 파일은 페이지 파일 기준 **상위 폴더**에 있어야 합니다. (예: `../충청북도_축제별 관광객 통계 정보_20191104.csv`)")

# --- 데이터 로드 ---
csv_path = Path(__file__).resolve().parents[1] / "충청북도_축제별 관광객 통계 정보_20191104.csv"
if not csv_path.exists():
    st.error(f"CSV 파일을 찾지 못했어요. 경로를 확인해주세요: {csv_path}")
    st.stop()

# 읽기: 다양한 인코딩 문제가 있을 수 있으니 안전하게 시도
encodings = ["utf-8","cp949","euc-kr","latin1"]
df = None
for e in encodings:
    try:
        df = pd.read_csv(csv_path, encoding=e, engine='python')
        break
    except Exception:
        df = None
if df is None:
    st.error("CSV 파싱 실패: 지원되는 인코딩(utf-8, cp949, euc-kr, latin1)으로도 읽을 수 없습니다.")
    st.stop()

st.sidebar.header("데이터 요약")
st.sidebar.write(f"- 행: {df.shape[0]:,}, 열: {df.shape[1]}")
st.sidebar.write("- 주요 컬럼 예시: " + ", ".join(list(df.columns[:8])))

# --- 전처리: 방문객 관련 컬럼 집계 ---
# 방문객 관련 컬럼 찾기 (현지 / 외지 / 외국)
visitor_cols = [c for c in df.columns if any(k in c for k in ['현지인','외지인','외국인','외국'])]
# 안전하게 숫자 변환
for c in visitor_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

# 각각 집계 컬럼 생성 (존재하는 컬럼들에 대해 합산)
df['현지_total'] = df[[c for c in visitor_cols if '현지' in c]].sum(axis=1) if any('현지' in c for c in visitor_cols) else 0
df['외지_total'] = df[[c for c in visitor_cols if '외지' in c]].sum(axis=1) if any('외지' in c for c in visitor_cols) else 0
df['외국_total'] = df[[c for c in visitor_cols if '외국' in c or '외국인' in c]].sum(axis=1) if any(('외국' in c or '외국인' in c) for c in visitor_cols) else 0

# 축제명 컬럼 선택 (일반적으로 '축제 명' 사용)
name_col = next((c for c in df.columns if '축제' in c and '명' in c), df.columns[0])

# 축제별 집계
agg = df.groupby(name_col)[['현지_total','외지_total','외국_total']].sum().reset_index()
agg['전체합계'] = agg[['현지_total','외지_total','외국_total']].sum(axis=1)
agg = agg.sort_values('전체합계', ascending=False).reset_index(drop=True)

st.subheader("데이터 샘플 & 상위 축제")
st.write("원본 데이터에서 추정한 주요 컬럼과 상위 축제(방문객 합계 기준)")
st.dataframe(agg.head(10).style.format({ '현지_total':'{:,}', '외지_total':'{:,}', '외국_total':'{:,}', '전체합계':'{:,}'}), height=300)

# --- 인터랙티브: 축제 선택과 막대 그래프 ---
festival_list = agg[name_col].tolist()
sel = st.selectbox("축제명을 선택하세요", festival_list, index=0)

row = agg[agg[name_col] == sel].iloc[0]
values = [float(row['현지_total']), float(row['외지_total']), float(row['외국_total'])]
labels = ['현지인', '외지인', '외국인']

# 색상: 1등(최대) = 빨간색, 나머지는 그라데이션 느낌
max_idx = int(np.argmax(values))

# 그라데이션 색상 배열(파란계열)에서 적당히 픽
blues = px.colors.sequential.Blues
colors = []
for i in range(len(values)):
    if i == max_idx:
        colors.append('#ff4d4d')  # 빨강
    else:
        # pick gradient colors by index but avoid out-of-range
        idx = 3 + i*2
        idx = min(idx, len(blues)-1)
        colors.append(blues[idx])

# Plotly 막대그래프 (각 카테고리를 별도 trace로 추가해 색상 제어)
fig = go.Figure()
for lab, val, col in zip(labels, values, colors):
    fig.add_trace(go.Bar(x=[lab], y=[val], name=lab, marker_color=col, text=[int(val)], textposition='auto'))

fig.update_layout(
    title=f"{sel} — 방문객 구성",
    xaxis_title="방문객 유형",
    yaxis_title="방문객 수 (명)",
    showlegend=False,
    template="simple_white"
)

st.plotly_chart(fig, use_container_width=True)

# --- 비율(%) 표시 ---
total = sum(values)
if total > 0:
    pct = [v/total*100 for v in values]
    st.write("비율(%)")
    st.table(pd.DataFrame({'구분': labels, '명수': [int(v) for v in values], '비율(%)': [f"{p:.2f}%" for p in pct]}))
else:
    st.info("선택한 축제에 대한 방문객 수가 0이거나 데이터가 없습니다.")

st.markdown("---")
st.caption("참고: 원본 데이터에 결측치가 있을 수 있습니다. 앱은 결측을 0으로 취급해 합계·비율을 계산합니다.")

