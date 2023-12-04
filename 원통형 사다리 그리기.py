import streamlit as st
from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import time
import base64
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import networkx as nx

import os
import matplotlib.font_manager as fm

font_dirs = [os.getcwd() + '/customFonts']
font_files = fm.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    fm.fontManager.addfont(font_file)
fm._load_fontmanager(try_read_cache=False)
plt.rc('font', family='NanumSquareRound')
mpl.rcParams['axes.unicode_minus'] = False

st.header("누가 꽝:smiling_imp:일까?!",divider="rainbow")
content1='어느 위치를 선택해야 꽝에 걸리지 않을까?'
st.markdown(content1,help="사다리타기 게임에서 어느 위치를 선택하든 :blue[꽝에 걸릴 확률]은 :red[모두 같을까?!]")

image_placeholder = st.empty()
image = 'lose.png'
image_placeholder.image(image) 

def ladder(participants, results):
    global bridges
    result_dict = {p: r for p, r in zip(participants, results)}
    
    bridges = [[0 for _ in range(len(participants))] for _ in range(7)]
    for i in range(len(bridges)):
        last_bridge = -1
        for j in range(len(participants)):
            if i == 0 or last_bridge == (j - 1) % len(participants):
                continue
            bridges[i][j] = random.randint(0, 1)
            if bridges[i][j] == 1:
                last_bridge = j

    paths = [i for i in range(len(participants))]

    for bridge in bridges:
        for i in range(len(paths)):
            if bridge[i % len(participants)]:
                paths[i % len(participants)], paths[(i + 1) % len(participants)] = paths[(i + 1) % len(participants)], paths[i % len(participants)]
    
    return {p: result_dict[participants[idx]] for p, idx in zip(participants, paths)}

def draw_ladder(participants, bridges, fail_position):
    fig, ax = plt.subplots()

    for i in range(len(participants)):
        ax.plot([i, i], [0, len(bridges)], 'k')

    for i, bridge in enumerate(bridges):
        for j, b in enumerate(bridge):
            if b:
                ax.plot([j % len(participants), (j + 1) % len(participants)], [len(bridges) - i, len(bridges) - i], 'k')

    for i, participant in enumerate(participants):
        ax.text(i, -0.5, participant, ha='center')
        if i == int(fail_position) - 1:
            ax.text(i, len(bridges) + 0.7, "꽝", ha='center')  

    ax.set_xticks([])
    ax.set_yticks([])
    plt.gca().invert_yaxis()
    return fig

participants = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
results = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

fail_position = st.radio('꽝의 위치를 선택하세요.', options=[str(i) for i in range(1, 11)])

start_game = st.button('게임 결과 보기')
if start_game:
    image_placeholder.empty()
    if "count_dict" not in st.session_state or st.session_state.last_fail_position != fail_position:
        st.session_state.count_dict = {participant: 0 for participant in participants}
        st.session_state.last_fail_position = fail_position

    results = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    results[int(fail_position) - 1] = '꽝'
    
    ladder_result = ladder(participants, results)
    for participant, result in ladder_result.items():
        if result == '꽝':
            st.session_state.count_dict[participant] += 1

    fig = draw_ladder(participants, bridges, fail_position)
    st.pyplot(fig)
    
    df = pd.DataFrame.from_dict(st.session_state.count_dict, orient='index', columns=['꽝에 걸린 횟수'])
    df = df.transpose()
    st.dataframe(df.style.highlight_max(axis=1))

st.write("")    
st.divider()
st.write("")

st.write("꽝의 위치가 공개되었을 때, 어느 위치를 선택하든 공평하게 꽝에 걸릴 것인가에 대한 본인의 생각을 작성해보자.")
user_input = st.text_area("",value="여기에 본인의 생각을 작성하세요.")
submit_button = st.button("제출")
if submit_button:
    st.write("제출 완료되었습니다. Next 버튼을 누르세요.")

page = "생각해보기_그래프.py"
if st.button("Next"):
    switch_page("생각해보기_그래프")