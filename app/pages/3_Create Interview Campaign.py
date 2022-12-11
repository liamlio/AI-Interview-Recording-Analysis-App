# Login streamlit page
# Hard code User=Assembly, PW=50k
# Will also be the base page

# Should create a new campaign with a new question
# Should generate a unique link and route the user who clicks the link to a login page
# Can I use flask purely for routing to streamlit apps and pages?

import streamlit as st
import os
import json

st.write("# Create a new Interview Campaign")
if 'user_id' not in st.session_state:
	st.session_state.user_id = 'assemblyai'
# Campaign name submit
new_campaign_name = st.text_input(label="New Campaign Name", placeholder="ex: Senior Manager", key="new_campaign_name")
number_of_questions = st.slider("Number of Questions (we recommend 3-5)", min_value=1, max_value=5, value=3)
questions = []
for n in range(number_of_questions):
    questions.append(st.text_input(label="Add Pre-Screen Question", placeholder="Why do you want to join Vindent AI?", key=f"question_{n}"))

# Questions
if new_campaign_name:
    st.write("### New Campaign information")
    st.write(f"Campaign Name: **{new_campaign_name}**")
for question in questions:
    st.write(question)

if st.button("Submit"):
    current_campaign = {
        "name": new_campaign_name,
        "questions": questions
    }
    with open(f"app/pages/database/{st.session_state.user_id}/current_campaign.json", "w") as write_file:
        json.dump(current_campaign, write_file, indent=4)

