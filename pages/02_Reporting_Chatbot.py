import streamlit as st
import pandas as pd

st.set_page_config(page_title="GDGoC Inha Streamlit Demo",
                   page_icon="👾")

st.title("Reporting Agent")

st.write("""
레포트 작성 에이전트 입니다..\n
원하는 검색을 입력하시거나 무엇이든 물어보세요.
""")

st.divider()

chat = st.chat_input("Send Your Messages")
        
