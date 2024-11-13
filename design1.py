import streamlit as st

st.title("알레르기 정보 관리")

# **1. 알레르기 정보 입력 섹션**
st.subheader("알레르기 정보 입력")

allergen = st.text_input("알레르기 성분을 입력하세요 (예: 땅콩, 우유)")

risk_level = st.selectbox("위험 그룹을 선택하세요", ("High Risk Group", "Risk Group", "Caution Group"))

if st.button("알레르기 정보 추가"):
    if allergen and risk_level:
        if validate_allergen(allergen):
            insert_allergy_info(allergen, risk_level)
            st.success("알레르기 정보가 추가되었습니다!")
            # 데이터 업데이트를 위해 페이지 상태 변경
            st.session_state.refresh = not st.session_state.refresh
        else:
            st.error("알레르기 성분에 유효하지 않은 문자가 포함되어 있습니다.")
    else:
        st.error("알레르기 성분과 위험 그룹을 모두 입력해주세요.")

st.markdown("---")

# **2. 저장된 알레르기 정보 표시 및 그룹별 출력**
st.subheader("저장된 알레르기 정보 목록")

# 그룹별로 알레르기 정보 가져오기
allergy_data_grouped = get_allergy_info_grouped()

# 그룹별로 테이블 및 삭제 버튼 표시
for group, data in allergy_data_grouped.items():
    # 위험도에 따른 색상 및 글자 크기 지정
    color = "red" if group == "High Risk Group" else "orange" if group == "Risk Group" else "yellow"
    
    # 그룹 헤더에 색상과 큰 글자 크기 추가
    st.markdown(f"<h3 style='color:{color}; font-size: 26px;'>{group}</h3>", unsafe_allow_html=True)
    
    if not data.empty:
        for index, row in data.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                # 알레르기 성분에 대해 큰 글자 크기 추가
                st.markdown(f"<p style='font-size: 20px;'>{row['allergen']}</p>", unsafe_allow_html=True)
            with col2:
                # 고유한 키를 생성하기 위해 그룹과 인덱스를 포함
                button_key = f"delete_{group}_{index}"
                if st.button("삭제", key=button_key):
                    delete_allergy_info(row['allergen'])
                    st.success(f"{row['allergen']} 항목이 삭제되었습니다!")
                    # 데이터 업데이트를 위해 페이지 상태 변경
                    st.session_state.refresh = not st.session_state.refresh
    else:
        st.write("해당 그룹에 저장된 알레르기 정보가 없습니다.")
