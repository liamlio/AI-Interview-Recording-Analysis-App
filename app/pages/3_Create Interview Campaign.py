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

# Campaign name submit
new_campaign_name = st.text_input(label="New Campaign Name", placeholder="ex: Senior Manager", key="new_campaign_name")

# Questions



st.write("Could do this by having a separate streamlit app that is create through an aws service when the button is clicked here, data is saved in a specific spot that is fetched in the dashboard")
# current_campaigns = pd.read_csv("current_campaigns.csv")
