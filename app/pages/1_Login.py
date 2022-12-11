# Login streamlit page
# Hard code User=Assembly, PW=50k
# Will also be the base page

# Login page using amazon cognito
# https://aws.amazon.com/blogs/opensource/using-streamlit-to-build-an-interactive-dashboard-for-data-analysis-on-aws/
import streamlit as st
import vindent_utils.authenticate as authenticate
# Check authentication when user lands on the page.
st.set_page_config(
    page_title="Add Custom Models",
    page_icon="",
    layout="wide"
)

authenticate.set_st_state_vars()
# Add login/logout buttons
if st.session_state["authenticated"]:
    authenticate.button_logout()
else:
    authenticate.button_login()

if st.session_state["authenticated"] and "Candidate" in st.session_state["user_cognito_groups"] or "Admin" in st.session_state["user_cognito_groups"]:
    # Show the page content
    # Contents of page 1
    st.write(
        """This demo illustrates a combination of plotting!..."""
    )
# ...
else:
    if st.session_state["authenticated"]:
        st.write("You do not have access. Please contact the administrator.")
    else:
        st.write("Please login!")

st.write("### This page serves as a dummy login page, I setup login through AWS Cognito, but since this url is not SSL Certified I can't properly setup user authentication. Since SSL Certification can take time, I will leave this feature unfinished within the webapp.")