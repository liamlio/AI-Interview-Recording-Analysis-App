# Login streamlit page
# Hard code User=Assembly, PW=50k
# Will also be the base page

# Should create a new campaign with a new question
# Should generate a unique link and route the user who clicks the link to a login page
# Can I use flask purely for routing to streamlit apps and pages?

import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Add Custom Models",
    page_icon="",
    layout="wide"
)

# Don't allow non-authenticated users to see the sidebar. Make the sidebar blank on this page if non admin user
# This will be the submission page for pre-screen folk

if 'current_campaign' not in st.session_state:
	st.session_state.current_campaign = 'No Current Campaign'

if 'user_id' not in st.session_state:
	st.session_state.user_id = 'assemblyai'


with open(f"app/pages/database/{st.session_state.user_id}/current_campaign.json") as json_file:
    current_campaign = json.load(json_file)
st.header(current_campaign["name"])

for question in current_campaign["questions"]:
    with st.container():
        st.write(f"#### {question}")


