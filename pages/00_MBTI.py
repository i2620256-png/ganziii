import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천", page_icon="🎯", layout="centered")

st.title("MBTI 기반 진로 추천 🎓✨")
st.caption("MBTI 하나 골라서 너한테 딱 맞는 진로 2개 추천해줄게 — 간단하고 친절하게!")

MBTIS = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ",
]

# 각 유형에 대해 2개 진로 제안 및 설명
MBTI_TO_CAREERS = {
    "ISTJ": [
        {"career":"행정/공무원📋","departments":"행정학, 법학, 경영학","personality":"체계적이고 책임감 강한 사람에게 추천. 규칙과 절차를 잘 따름."},
        {"career":"회계/감사💼","departments":"회계학, 경영학","personality":"정밀하고 꼼꼼한 성격에 잘 맞음. 숫자와 자료 정리에 강점이 있어."},
    ],
    "ISFJ": [
        {"career":"간호/보건의료🩺","departments":"간호학, 보건학","personality":"타인을 돌보고 세심한 배려를 자연스럽게 함. 안정적인 환경에서 빛남."},
        {"career":"사회복지/상담🤝","departments":"사회복지학, 상담심리학","personality":"사람을 도와주는 걸 좋아하고 신뢰감 있는 성격에 적합."},
    ],
    "INFJ": [
        {"career":"임상심리/상담💬","departments":"심리학, 상담학","personality":"깊이 있는 공감 능력과 통찰력을 가지고 있어, 개인 맞춤형 도움에 강함."},
        {"career":"교육/진로지도📚","departments":"교육학, 상담심리","personality":"사람의 성장에 관심 많은 유형. 장기적 관계에서 힘을 발휘함."},
    ],
    "INTJ": [
        {"career":"연구개발/R&D🔬","departments":"자연과학, 공학, 컴퓨터공학","personality":"전략적이고 분석적인 사고를 바탕으로 복잡한 문제 해결에 강함."},
        {"career":"데이터 과학/AI📊","departments":"통계학, 컴퓨터공학, 산업공학","personality":"논리적이고 호기심 많음. 데이터에서 패턴을 찾는 일에 적합."},
    ],
    "ISTP": [
        {"career":"기계/설계 엔지니어🔧","departments":"기계공학, 산업공학","personality":"실용적이고 문제 해결을 즉시 실행에 옮기는 타입. 현장 적응력 좋음."},
        {"career":"IT 개발자(프론트/백엔드)💻","departments":"컴퓨터공학, 소프트웨어학","personality":"손으로 직접 만들어보는 걸 좋아하고 논리적 판단이 빠름."},
    ],
    "ISFP": [
        {"career":"디자인/시각예술🎨","departments":"시각디자인, 산업디자인, 예술학","personality":"감성적이고 미적 감각이 뛰어남. 창의적 표현에서 빛남."},
        {"career":"촬영/콘텐츠 크리에이터📷","departments":"영상학, 미디어학","personality":"현장에서 직관적으로 분위기를 잡아내고 감각적인 결과물을 만듦."},
    ],
    "INFP": [
        {"career":"문학/창작 작가✍️","departments":"국문학, 문예창작","personality":"내면 세계가 풍부하고 독창적 아이디어를 글로 표현하는 걸 좋아함."},
        {"career":"사회적 기업/NGO 활동🌱","departments":"사회복지학, 국제학","personality":"가치 지향적이며 세상을 더 나은 방향으로 바꾸는 데 관심이 많음."},
    ],
    "INTP": [
        {"career":"소프트웨어 연구/개발🧠","departments":"컴퓨터공학, 정보통신","personality":"논리적 분석과 추상적 사고에 강함. 개념 설계에 재능이 있음."},
        {"career":"학술/연구(이론)📘","departments":"수학, 물리, 철학","personality":"호기심 많고 깊게 파고드는 걸 즐김. 혼자서도 잘해냄."},
    ],
    "ESTP": [
        {"career":"영업/마케팅(현장)🚀","departments":"경영학, 광고홍보","personality":"사교적이고 즉흥적 판단이 빠름. 사람 만나서 성과 내는 일을 좋아함."},
        {"career":"응급구조/소방관🚒","departments":"응급구조학, 소방안전학","personality":"위기 상황에서 침착하게 행동하고 실전 감각이 뛰어남."},
    ],
    "ESFP": [
        {"career":"무대·연예/퍼포먼스🎤","departments":"연기/무용, 공연예술","personality":"사람들 앞에서 에너지 발산하는 걸 즐기며 즉흥적 재능이 있음."},
        {"career":"이벤트/관광 서비스🏖️","departments":"관광경영, 호텔경영","personality":"사교적이고 사람 기분 좋게 만드는 데 재능이 있음."},
    ],
    "ENFP": [
        {"career":"창업/스타트업 창업가🌟","departments":"경영학, 창업학, 디자인씽킹","personality":"아이디어 뿜뿜! 사람들을 모으고 영감을 주는 역할에 잘 맞음."},
        {"career":"콘텐츠 기획/마케팅📣","departments":"미디어학, 광고홍보","personality":"창의적이고 사람 심리를 잘 읽음. 트렌드 감각도 좋음."},
    ],
    "ENTP": [
        {"career":"전략 컨설팅🧩","departments":"경영학, 경제학","personality":"논쟁을 즐기고 빠르게 아이디어 전환이 가능. 문제 재해석에 능함."},
        {"career":"벤처 투자/스타트업 분석📈","departments":"금융학, 경영학","personality":"기회를 발견하고 리스크를 계산하는 데 흥미를 느낌."},
    ],
    "ESTJ": [
        {"career":"경영/관리(팀장)🏢","departments":"경영학, 산업경영","personality":"실행력 있고 조직을 이끄는 데 적합. 규율과 목표지향적."},
        {"career":"법조(검사/판사 등)⚖️","departments":"법학","personality":"공정성과 질서를 중시하며 원칙을 지키는 역할에 잘 맞음."},
    ],
    "ESFJ": [
        {"career":"교육/교사👩‍🏫","departments":"교육학, 유아교육","personality":"사람을 돌보고 분위기 조성 잘 함. 협력과 책임감이 강함."},
        {"career":"의료 행정/병원 운영🏥","departments":"보건행정, 경영학","personality":"사람 중심적이고 조직 내에서 조율 역할을 잘 수행함."},
    ],
    "ENFJ": [
        {"career":"HR/인재개발🌱","departments":"경영학, 심리학","personality":"사람의 성장에 관심 많고 리더십으로 팀을 이끄는 데 능함."},
        {"career":"공공외교/국제기구🌍","departments":"국제학, 정치학","personality":"사교성과 공감 능력으로 다양한 사람과 협업하기 좋음."},
    ],
    "ENTJ": [
        {"career":"경영진/CEO💼","departments":"경영학, 경제학","personality":"전략적이고 목표 달성에 강함. 리더로 성장하기 좋은 타입."},
        {"career":"사업 개발/프로젝트 매니저📌","departments":"산업공학, 경영학","personality":"체계적으로 큰 그림을 그려 실행시키는 데 능함."},
    ],
}

st.markdown("---")

selected = st.selectbox("너의 MBTI를 골라줘 😎", MBTIS, index=0)

st.write(f"### {selected}님에게 어울리는 진로 추천 💡")

careers = MBTI_TO_CAREERS.get(selected, [])

col1, col2 = st.columns(2)

if careers:
    for i, c in enumerate(careers):
        target_col = col1 if i == 0 else col2
        with target_col:
            st.subheader(f"{c['career']}")
            st.write(f"**어울리는 학과:** {c['departments']}")
            st.write(f"**어울리는 성격:** {c['personality']}")
            st.write("\n")
            with st.expander("왜 이 진로가 어울릴까? 🔍"):
                st.write(
                    "이 진로는 너의 성향을 바탕으로 실제로 잘 맞을 가능성이 높은 일들을 골라봤어.\n"
                    "학교 전공도 참고해서 적어놨으니까, 관심 가는 건 수업을 들어보고 경험해보는 걸 추천해!"
                )
else:
    st.write("추천 정보를 찾을 수 없네... 다른 유형 골라볼래?")

st.markdown("---")

st.info("Tip: MBTI는 성향을 알려주는 도구일 뿐이야. 같은 MBTI더라도 개인차가 크니까, 다양한 경험을 통해 직접 판단해봐! 😊")

st.caption("만들기: 너의 친절한 진로 도우미 — 복사해서 Streamlit Cloud에 붙여넣으면 바로 작동해요.")
