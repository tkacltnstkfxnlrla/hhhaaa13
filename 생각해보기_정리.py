import streamlit as st
from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import time
import base64

import os
import matplotlib.font_manager as fm

font_dirs = [os.getcwd() + '/customFonts']
font_files = fm.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    fm.fontManager.addfont(font_file)
fm._load_fontmanager(try_read_cache=False)
plt.rc('font', family='NanumSquareRound')
mpl.rcParams['axes.unicode_minus'] = False

st.header(":thinking_face:사다리타기 게임이 원통형:oil_drum:이라면?!",divider="rainbow")
content1='첫번째 줄과 마지막 줄이 연결되는 가로선도 있는 사다리타기 게임이라면 결과가 어떻게 될까?'
st.markdown(content1,help="그림과 같은 :blue[원기둥 모양]의 :red[사다리타기 게임]을 생각해보자.![Alt Text](https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F75v5r%2FbtrbXhDhQEq%2FD0sw39NFLLKFxdtFsSqec1%2Fimg.png)")

image = 'lose.png'
st.image(image)

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

st.write("다음 영상을 보면서 이번 활동에 대한 소감을 작성해보자.")
video_link = 'https://www.youtube.com/embed/BRaNXWYKDuo'

st.components.v1.html(
    f'<iframe width="560" height="315" src="{video_link}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', 
    height=320)
user_input = st.text_area("",value="여기에 소감을 작성하세요.")
submit_button = st.button("제출")
if submit_button:
    st.write("제출 완료되었습니다. 활동 끝!")