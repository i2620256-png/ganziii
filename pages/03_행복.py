# Streamlit app for exploring population.csv by neighborhood
# Place this file at: pages/population_app.py
# Place CSV at: ../population.csv (project root, one level above pages)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO

st.set_page_config(page_title="Population Explorer", layout="wide")

st.title("동네별 인구/항목 비율 탐색기")
st.markdown("CSV 파일은 `../population.csv` (pages 폴더의 상위 폴더)에 위치해야 합니다.")

@st.cache_data
def load_csv(path='../population.csv'):
    # Try common encodings to be robust on Streamlit Cloud
    encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1']
    last_err = None
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            return df
        except Exception as e:
            last_err = e
    # final attempt without specifying encoding
    df = pd.read_csv(path, low_memory=False)
    return df

try:
    df = load_csv()
except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()

# Show basic info
with st.expander("원본 데이터 — 샘플(10행)"):
    st.dataframe(df.head(10))

st.subheader("데이터 요약")
col1, col2 = st.columns([2,1])

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
non_numeric = [c for c in df.columns if c not in numeric_cols]

with col1:
    if numeric_cols:
        st.markdown("**숫자형 컬럼 기술통계**")
        st.dataframe(df[numeric_cols].describe().T)
    else:
        st.info("숫자형 컬럼이 발견되지 않았습니다.")

with col2:
    st.markdown("**결측치 요약**")
    miss = df.isnull().sum()
    miss = miss[miss > 0].sort_values(ascending=False)
    if miss.empty:
        st.write("결측치 없음")
    else:
        st.dataframe(miss.to_frame(name='missing_count'))

# Try to detect a neighborhood column
possible_names = ["동네", "동네명", "Neighborhood", "neighborhood", "dong", "지역", "Area", "area", "동", "구", "읍면동", "neighbourhood", "지역명"]
neigh_col = None
for n in possible_names:
    if n in df.columns:
        neigh_col = n
        break

# Fallback: choose a categorical-like column
if neigh_col is None:
    candidates = [c for c in df.columns if c not in numeric_cols]
    for c in candidates:
        nunique = df[c].nunique(dropna=True)
        # pick if cardinality looks like neighborhoods (not too high, not singleton)
        if 2 <= nunique <= max(200, len(df) // 2):
            neigh_col = c
            break

if neigh_col is None:
    st.error("데이터에서 '동네'에 대응하는 컬럼을 찾지 못했습니다. 파일에 동네(지역)를 나타내는 범주형 컬럼이 필요합니다.")
    st.stop()

st.markdown(f"**탐색에 사용할 동네 컬럼:** `{neigh_col}`")

# Prepare neighborhood list
neighborhoods = sorted(df[neigh_col].dropna().unique())
selected_neighborhood = st.selectbox("동네를 선택하세요", neighborhoods)

# Compute per-neighborhood means for numeric columns
means = df.groupby(neigh_col)[numeric_cols].mean()
if selected_neighborhood not in means.index:
    st.warning("선택한 동네에 충분한 데이터가 없습니다.")
    st.stop()

# For '각 항목별 비율', compute the proportion of each numeric column's mean relative to the row sum
row = means.loc[selected_neighborhood]
row_sum = row.sum()
if row_sum == 0 or np.isnan(row_sum):
    st.warning("선택한 동네의 합계가 0이어서 비율을 계산할 수 없습니다.")
    st.stop()
proportions = (row / row_sum).sort_values(ascending=False)

# Color mapping: top = red, others gradient toward red
items = proportions.index.tolist()
values = proportions.values.astype(float)
max_idx = int(np.nanargmax(values))

# helper for gradient
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(max(0,min(255,x))) for x in rgb)

light_color = hex_to_rgb('#ffecec')
red_color = hex_to_rgb('#ff0000')

# normalize for gradient (exclude constant case)
if np.nanmax(values) - np.nanmin(values) == 0:
    norm = np.zeros_like(values)
else:
    norm = (values - np.nanmin(values)) / (np.nanmax(values) - np.nanmin(values))

colors = []
for i, v in enumerate(values):
    if i == max_idx:
        colors.append('#ff0000')
    else:
        t = float(norm[i])
        r = light_color[0] + (red_color[0] - light_color[0]) * t
        g = light_color[1] + (red_color[1] - light_color[1]) * t
        b = light_color[2] + (red_color[2] - light_color[2]) * t
        colors.append(rgb_to_hex((r,g,b)))

# Build Plotly bar chart
fig = go.Figure()
fig.add_trace(go.Bar(
    x=items,
    y=values,
    marker_color=colors,
    hovertemplate="%{x}: %{y:.2%}<extra></extra>",
))
fig.update_layout(
    title=f"{selected_neighborhood}의 항목별 비율 (합계=1)",
    xaxis_title="항목",
    yaxis_title="비율",
    template='plotly_white',
    margin=dict(t=60, l=40, r=40, b=160)
)

st.plotly_chart(fig, use_container_width=True)

# Show the numeric table too
st.subheader("선택 동네 — 항목별 평균 및 비율")
res_df = pd.DataFrame({'mean': row, 'proportion': proportions})
res_df['proportion'] = res_df['proportion'].fillna(0)
st.dataframe(res_df)

# Offer downloads
st.subheader("데이터 다운로드")
if st.button("선택 동네 비율 복사 to clipboard (CSV)"):
    csv_buf = res_df.to_csv(index=True)
    st.download_button("CSV 다운로드", data=csv_buf, file_name=f"{selected_neighborhood}_proportions.csv", mime='text/csv')

# Extra: correlation heatmap and pairwise insights
if len(numeric_cols) >= 2:
    st.subheader("숫자형 항목 상관계수 히트맵")
    corr = df[numeric_cols].corr()
    fig2 = px.imshow(corr, text_auto=True)
    fig2.update_layout(margin=dict(t=40,l=40,r=40,b=40))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("앱: Streamlit Cloud에서 작동하도록 작성되었습니다. CSV 파일은 pages 폴더 상위(프로젝트 루트)에 위치해야 합니다.")
