import os
import json
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import numpy as np
from io import BytesIO
from pathlib import Path
from vindent_utils.analysis_pipeline import audio_pipeline

st.set_page_config(
    page_title="Add Custom Models",
    page_icon="",
    layout="wide"
)

st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
    unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
    unsafe_allow_html=True)  # lightmode
# This will be the submission page for pre-screening Candidates
if 'user_id' not in st.session_state:
	st.session_state.user_id = 'assemblyai'

# User needs to submit their name

with open(f"app/pages/database/{st.session_state.user_id}/current_campaign.json") as json_file:
    current_campaign = json.load(json_file)
st.header(current_campaign["name"])

# with st.form("first_lastname"):
user_name = st.text_input("First and Last name", placeholder="Jane Doe")

#### IF audio component is what's slowing everything down, remove it and replace with upload file
#### Then just link users to an online audio recorders to get the files from

st.write("Please limit all responses to less then 3 minutes in audio length.")
for i, question in enumerate(current_campaign["questions"]):
    with st.container():
        st.write(f"#### {question}")
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        # Custom REACT-based component for recording client audio in browser
        build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
        # specify directory and initialize st_audiorec object functionality
        st_audiorec = components.declare_component("st_audiorec", path=build_dir)

        # STREAMLIT AUDIO RECORDER Instance
        val = st_audiorec(key=f"question_{i}")
        # web component returns arraybuffer from WAV-blob


submitted = st.button("Submit Interview")
submitted
if submitted:
    st.write("Uploading and Processing Audio Recordings...")
    user_path = f"app/pages/database/{st.session_state.user_id}/campaigns/{current_campaign['name']}/{user_name}"
    Path(user_path).mkdir(parents=True, exist_ok=True)
    for i in range(len(current_campaign["questions"])):
        val = st.session_state[f"question_{i}"]
        if isinstance(val, dict):  # retrieve audio data
            ind, val = zip(*val['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            val = np.array(val)             # convert to np array
            sorted_ints = val[ind]
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            wav_bytes = stream.read()
            with open(user_path + f'/question_{i}.wav', mode='bx') as f:
                f.write(wav_bytes)
            texts_df = audio_pipeline(user_path + f'/question_{i}.wav')
            texts_df.to_csv(user_path + f'/question_{i}.csv')



