import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지 TOP 10", page_icon="🗺️", layout="wide")

st.title("🗺️ 외국인들이 좋아하는 서울 관광지 TOP 10")
st.write("서울을 찾는 외국인들이 가장 많이 방문하는 인기 명소들을 지도로 확인해보세요! 🇰🇷")

# 서울 주요 관광지 TOP 10 (임의의 대표 좌표 포함)
tourist_spots = [
    {"name": "경복궁 (Gyeongbokgung Palace)", "lat": 37.579617, "lon": 126.977041, "desc": "조선시대의 대표 궁궐"},
    {"name": "명동 (Myeongdong)", "lat": 37.563757, "lon": 126.982661, "desc": "쇼핑과 길거리 음식의 천국"},
    {"name": "남산타워 (Namsan Seoul Tower)", "lat": 37.551169, "lon": 126.988227, "desc": "서울의 전망을 한눈에!"},
    {"name": "홍대 (Hongdae)", "lat": 37.556332, "lon": 126.922651, "desc": "젊음과 예술의 거리"},
    {"name": "북촌한옥마을 (Bukchon Hanok Village)", "lat": 37.582604, "lon": 126.983998, "desc": "전통 한옥이 모여있는 마을"},
    {"name": "인사동 (Insadong)", "lat": 37.574011, "lon": 126.985829, "desc": "한국 전통문화의 중심"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.566478, "lon": 127.009041, "desc": "미래적인 건축물과 야시장"},
    {"name": "롯데월드타워 (Lotte World Tower)", "lat": 37.513068, "lon": 127.102538, "desc": "세계 5위 초고층 건물"},
    {"name": "이태원 (Itaewon)", "lat": 37.534556, "lon": 126.994963, "desc": "다문화의 거리, 글로벌 맛집 천국"},
    {"name": "청계천 (Cheonggyecheon Stream)", "lat": 37.569008, "lon": 126.978828, "desc": "도심 속 힐링 산책로"},
]

# 지도 중심 설정 (서울시청 기준)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 관광지 마커 표시
for spot in tourist_spots:
    folium.Marker(
        [spot["lat"], spot["lon"]],
        popup=f"<b>{spot['name']}</b><br>{spot['desc']}",
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 표시
st_data = st_folium(m, width=800, height=600)
