import streamlit as st
from streamlit_extras.switch_page_button import switch_page

page = "생각해보기.py"
image = 'hmpgimg.png'

st.title(":video_game: 사다리타기 게임의 비밀 :face_with_finger_covering_closed_lips:")
st.image(image)
if st.button("Start"):
    switch_page("생각해보기")