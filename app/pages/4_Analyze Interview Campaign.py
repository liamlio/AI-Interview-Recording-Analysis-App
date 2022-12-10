import streamlit as st
import pandas as pd
import os

from vindent_utils.analysis_pipeline import COHERE_API_KEY

st.set_page_config(
    page_title="VintedAI Interview Analysis Dashboard",
    page_icon="",
)

st.title('Analyze Interview Campaigns Dashboard')

# Column to display models + model colours
# Small st.color_picker widget to change color
# Use st.empty to pop up a color_picker
# Use session_state to keep colour the same across sessions
# need a random colour first
left, right = st.columns([9, 1])
with right:
    "cheese"
st.color_picker("cheese") # SWEET???
# Need a drop down to first select the current campaign, based on os file directory LOL


# Then a drop down for submitted audio files

# Analysis tool - base one includes everyone in the campaign

# Plots to compare? Bar graphs for average scores

# Text checking and audio checking
# Use tabs for this***
# Where you can look and listen to specific responses
# st.audio to display a play audio button!!
# This where I can have little boxes to say yes or no for what models to check on the side column
