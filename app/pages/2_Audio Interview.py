import json
import time
import streamlit as st
import pandas as pd
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

with open(Path(f"app/pages/database/{st.session_state.user_id}/current_campaign.json")) as json_file:
    current_campaign = json.load(json_file)
st.header(current_campaign["name"])

# with st.form("first_lastname"):
user_name = st.text_input("First and Last name", placeholder="Jane Doe")

#### IF audio component is what's slowing everything down, remove it and replace with upload file
#### Then just link users to an online audio recorders to get the files from
## ADD INSTRUCTIONS HERE!!!
st.write("### Instructions")
st.write("1. For each question below, record your answer using [https://online-voice-recorder.com/](https://online-voice-recorder.com/).")
st.write("2. Once you're happy with your recording, upload the recording for each respective question below.")
st.write("3. Click Submit once finished and wait for all the recordings to be uploaded and processed before closing this tab")

st.write("Please limit all responses to less then 3 minutes in audio length.")
for i, question in enumerate(current_campaign["questions"]):
    with st.container():
        st.write(f"#### {question}")
        val = st.file_uploader("Submit Response", type=["mp3"], key=f"question_{i}")
        if val is not None:
            st.audio(val)

submitted = st.button("Submit Interview")
if submitted:
    custom_models = pd.read_csv(Path(f"app/pages/database/{st.session_state.user_id}/custom_models_{st.session_state.user_id}.csv"), index_col=0)
    custom_models = {model_name:model_desc for model_name, model_desc in custom_models.values}
    st.write("Please don't close your browser yet")
    st.write("Uploading and Processing Audio Recordings...")
    st.write("(This can take a few minutes)")
    user_path = Path(f"app/pages/database/{st.session_state.user_id}/campaigns/{current_campaign['name']}/{user_name}")
    Path(user_path).mkdir(parents=True, exist_ok=True)
    for i in range(len(current_campaign["questions"])):
        val = st.session_state[f"question_{i}"]
        if val is None:
            st.error(f"Please submit question {i+1}")
            break
        dest_file = open(user_path / f'question_{i}.mp3', 'wb+')
        dest_file.write(val.getbuffer())
        dest_file.close()
        texts_df = audio_pipeline(user_path / f'question_{i}.mp3', custom_models=custom_models)
        texts_df.to_csv(user_path / f'analysis_question_{i}.csv')
        st.write(f"Question {i+1} Successfully Uploaded and Processed")
        time.sleep(5)
    st.write("Successfully Uploaded and Processed all Recordings. Thank you!")

