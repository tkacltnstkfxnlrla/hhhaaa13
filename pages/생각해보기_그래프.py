import streamlit as st
from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import time
import base64
from streamlit_extras.switch_page_button import switch_page

import os
import matplotlib.font_manager as fm

font_dirs = [os.getcwd() + '/customFonts']
font_files = fm.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    fm.fontManager.addfont(font_file)
fm._load_fontmanager(try_read_cache=False)
plt.rc('font', family='NanumSquareRound')
mpl.rcParams['axes.unicode_minus'] = False

st.header("누가 꽝:smiling_imp:일까?!_그래프",divider="rainbow")
content1='꽝의 위치를 선택하고, 시행 횟수를 늘려가면서 각 위치에 따라 꽝에 걸린 횟수가 어떻게 나타나는지 확인해보자.'
st.markdown(content1,help="이전 활동에서 :blue[추측한 내용]을 바탕으로 :red[확인]해보자!")

image = 'lose.png'
st.image(image)

def ladder(participants, results):
    global bridges
    result_dict = {p: r for p, r in zip(participants, results)}
    
    bridges = [[0 for _ in range(len(participants) - 1)] for _ in range(7)]
    for i in range(len(bridges)):
        for j in range(len(participants) - 1):
            if i == 0 or (j > 0 and bridges[i][j-1] == 1):  
                continue
            bridges[i][j] = random.randint(0, 1)

    paths = [i for i in range(len(participants))]

    for bridge in bridges:
        for i in range(len(paths) - 1):
            if bridge[i]:
                paths[i], paths[i + 1] = paths[i + 1], paths[i]
    
    return {p: result_dict[participants[idx]] for p, idx in zip(participants, paths)}

participants = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
results = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

fail_position_for_graph = st.radio('꽝의 위치를 선택하세요.', options=[str(i) for i in range(1, 11)])
trial_num = st.slider('시행 횟수를 선택하세요.', min_value=1, max_value=10000, value=1, step=1)

results_for_graph = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
results_for_graph[int(fail_position_for_graph) - 1] = '꽝'
count_dict_for_graph = {participant: 0 for participant in participants}

for _ in range(trial_num):
    ladder_result = ladder(participants, results_for_graph)
    for participant, result in ladder_result.items():
        if result == '꽝':
            count_dict_for_graph[participant] += 1

fig, ax = plt.subplots()
ax.bar(count_dict_for_graph.keys(), count_dict_for_graph.values())
plt.xlabel('위치', fontsize=15)
plt.ylabel('꽝에 걸린 횟수', fontsize=15)
plt.title('사다리타기 게임에서 꽝에 걸린 횟수', fontsize=18)
st.pyplot(fig)

st.write("")    
st.divider()
st.write("")

st.write("사다리타기 게임에서 꽝에 걸릴 가능성이 최대한 공평하기 위한 방법을 생각해보자.")
user_input = st.text_area("",value="여기에 본인의 생각을 작성하세요.")
submit_button = st.button("제출")
if submit_button:
    st.write("제출 완료되었습니다. Next 버튼을 누르세요.")

page = "생각해보기_정리.py"
if st.button("Next"):
    switch_page("생각해보기_정리")