import streamlit as st
import pandas as pd

st.set_page_config(page_title="GDGoC Inha Streamlit Demo",
                   page_icon="👾")

st.title("Data Analyst Chatbot")

st.write("""
데이터 분석 보조 챗봇입니다.\n
csv 파일을 업로드하고 데이터에 대해 물어보세요.
""")

st.divider()

with st.sidebar:
    file = st.file_uploader("CSV파일을 업로드해주세요.", type=["csv", "xlsx", "xls"])    
    if file is not None:
        try:
            # 파일 확장자 없이 바로 읽기 시도
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            st.success(f"{file.name} 로딩 완료")
        except Exception as e:
            st.error(f"파일 처리 중 오류 발생: {e}")

if file:
    chat = st.chat_input("Send Your Messages")
        
