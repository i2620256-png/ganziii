import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천 (아저씨 스타일)", layout="centered")

st.title("👴 MBTI로 보는 진로 추천 — 친근한 아저씨 스타일")
st.markdown("어르신, 반갑습니다~ 편안하게 MBTI 하나 골라보시게요.")

MBTI_LIST = [
    'ISTJ','ISFJ','INFJ','INTJ',
    'ISTP','ISFP','INFP','INTP',
    'ESTP','ESFP','ENFP','ENTP',
    'ESTJ','ESFJ','ENFJ','ENTJ'
]

recommendations = {
    'ISTJ': [
        {'career': '공무원(행정)', 'majors': '행정학, 정치외교, 법학', 'personality': '성실하고 규칙을 잘 지키는 분에게 적합합니다.', 'emoji': '📜'},
        {'career': '회계사/세무사', 'majors': '회계학, 경영학', 'personality': '섬세하고 책임감 강한 분에게 잘 맞습니다.', 'emoji': '🧾'},
    ],
    'ISFJ': [
        {'career': '간호사/복지직', 'majors': '간호학, 사회복지학', 'personality': '배려심 많고 꾸준한 성격이면 좋아요.', 'emoji': '🩺'},
        {'career': '초등교사', 'majors': '유아교육, 초등교육', 'personality': '아이들을 잘 돌보는 따뜻한 분에게 맞습니다.', 'emoji': '📚'},
    ],
    'INFJ': [
        {'career': '상담사/임상심리사', 'majors': '심리학, 상담학', 'personality': '사람 깊게 이해하는 성향이면 적합합니다.', 'emoji': '🧠'},
        {'career': '작가/콘텐츠 제작', 'majors': '문예창작, 국어국문', 'personality': '내면 표현을 좋아하는 분께 어울립니다.', 'emoji': '✍️'},
    ],
    'INTJ': [
        {'career': '연구원(이공계)', 'majors': '물리/화학/전산학/공학', 'personality': '계획적이고 분석적인 스타일에 잘 맞습니다.', 'emoji': '🔬'},
        {'career': '전략기획자', 'majors': '경영학, 경제학', 'personality': '장기적 관점에서 생각하는 분에게 추천합니다.', 'emoji': '📈'},
    ],
    'ISTP': [
        {'career': '현장 기술자/기계정비', 'majors': '기계공학, 전기공학', 'personality': '손재주 있고 문제 해결을 즐기면 좋아요.', 'emoji': '🔧'},
        {'career': '파일럿/운송직', 'majors': '항공운항, 교통공학', 'personality': '실전 감각이 뛰어난 분에게 적합합니다.', 'emoji': '✈️'},
    ],
    'ISFP': [
        {'career': '디자이너(시각/제품)', 'majors': '디자인학, 산업디자인', 'personality': '감각적이고 미적 감각이 뛰어나면 좋아요.', 'emoji': '🎨'},
        {'career': '정원사/원예사', 'majors': '원예학, 조경학', 'personality': '자연을 좋아하고 손으로 만드는 걸 즐기면 적합합니다.', 'emoji': '🌿'},
    ],
    'INFP': [
        {'career': '작가/편집자', 'majors': '문예창작, 국어국문', 'personality': '상상력이 풍부하고 가치지향적이면 좋아요.', 'emoji': '📖'},
        {'career': 'NGO 활동가/사회복지', 'majors': '사회복지학, 국제학', 'personality': '이상과 가치를 위해 일하길 좋아하는 분에게 추천합니다.', 'emoji': '🤝'},
    ],
    'INTP': [
        {'career': '소프트웨어 개발자', 'majors': '컴퓨터공학, 소프트웨어학', 'personality': '이론적 호기심 많고 문제 해결을 즐기는 타입입니다.', 'emoji': '💻'},
        {'career': '연구원(이론)', 'majors': '수학, 물리, 컴퓨터', 'personality': '복잡한 개념을 다루는 데 흥미가 있으면 어울립니다.', 'emoji': '🧩'},
    ],
    'ESTP': [
        {'career': '영업/세일즈', 'majors': '경영학, 마케팅', 'personality': '활달하고 설득력 있는 분에게 적합합니다.', 'emoji': '🤝'},
        {'career': '응급구조/소방관', 'majors': '소방학, 응급구조학', 'personality': '긴박한 상황에서 잘 대응하는 실전형에게 좋아요.', 'emoji': '🚒'},
    ],
    'ESFP': [
        {'career': '연예/무대(퍼포먼스)', 'majors': '연극영화, 공연예술', 'personality': '사교적이고 무대 체질이면 즐겁게 할 수 있습니다.', 'emoji': '🎤'},
        {'career': '관광/호스피탈리티', 'majors': '관광학, 호텔경영', 'personality': '사람을 대하는 걸 즐기는 분께 잘 맞습니다.', 'emoji': '🏨'},
    ],
    'ENFP': [
        {'career': '창업가/스타트업', 'majors': '경영학, 디자인씽킹', 'personality': '아이디어가 많고 사람을 이끄는 걸 좋아하면 적합합니다.', 'emoji': '💡'},
        {'career': '마케팅/브랜딩', 'majors': '광고홍보, 경영', 'personality': '창의적이며 사람 마음을 파악하는 데 능합니다.', 'emoji': '📣'},
    ],
    'ENTP': [
        {'career': '기술 영업/컨설턴트', 'majors': '경영, 공학', 'personality': '토론을 즐기고 새로운 기회를 찾는 분에게 좋아요.', 'emoji': '🗣️'},
        {'career': '제품매니저(PM)', 'majors': '컴퓨터공학, 경영학', 'personality': '아이디어를 실용화하는 데 흥미가 있는 분께 추천합니다.', 'emoji': '🎯'},
    ],
    'ESTJ': [
        {'career': '관리자/운영팀장', 'majors': '경영학, 산업공학', 'personality': '체계적이고 리더십 있는 분에게 적합합니다.', 'emoji': '🧭'},
        {'career': '법조계(판사/검사)', 'majors': '법학', 'personality': '원칙과 절차를 중시하는 분께 잘 맞습니다.', 'emoji': '⚖️'},
    ],
    'ESFJ': [
        {'career': '간호행정/복지시설 관리', 'majors': '사회복지, 보건행정', 'personality': '사람 돌보는 걸 좋아하고 조직에 기여하길 원하면 좋아요.', 'emoji': '🏥'},
        {'career': '초중고 교사', 'majors': '교육학, 유아교육', 'personality': '협력적이고 안정감을 주는 분에게 적합합니다.', 'emoji': '📝'},
    ],
    'ENFJ': [
        {'career': 'HR/조직개발', 'majors': '경영학, 심리학', 'personality': '사람을 이끄는 데 능하고 동기 부여를 잘합니다.', 'emoji': '🤝'},
        {'career': '정치/행정 리더', 'majors': '정치외교, 행정학', 'personality': '비전 제시하고 타인을 설득하는 데 강점이 있습니다.', 'emoji': '🎖️'},
    ],
    'ENTJ': [
        {'career': 'CEO/임원', 'majors': '경영학, 경제학', 'personality': '목표지향적이고 결단력 있는 분에게 추천합니다.', 'emoji': '🏢'},
        {'career': '전략 컨설턴트', 'majors': '경영, 경제', 'personality': '문제를 빠르게 분석하고 해결하는 데 강합니다.', 'emoji': '📊'},
    ],
}

choice = st.selectbox('MBTI를 골라보세요', MBTI_LIST)

if choice:
    st.markdown('---')
    st.header(f"선택: {choice}  {recommendations[choice][0]['emoji']}")
    st.write('어르신 눈높이에 맞춰 친절히 설명해 드립니다요~')

    for idx, rec in enumerate(recommendations[choice], start=1):
        st.subheader(f"{idx}. {rec['career']} {rec['emoji']}")
        st.write(f"- 어울리는 학과: {rec['majors']}")
        st.write(f"- 어떤 성격에 적합한가요?: {rec['personality']}")
        st.write('')

    st.markdown('---')
    st.info('참고: 추천은 일반적인 성향에 따른 제안입니다. 자네의 경험과 흥미가 가장 중요하니 마음에 드는 길 있으면 도전해 보시게요!')
    st.caption('앱 제작: 친절한 아저씨 스타일 안내')
