# Home streamlit page
# Hard code User=Assembly, PW=50k
# Will also be the base page
# Will contain project explanation
import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="",
)

st.write("# Welcome to VintedAi! 👋")

st.markdown(
    """
    
"""
)

# ----------------------------------
# Get authorization code after login
# ----------------------------------
def get_auth_code():
    """
    Gets auth_code state variable.

    Returns:
        Nothing.
    """
    auth_query_params = st.experimental_get_query_params()
    try:
        auth_code = dict(auth_query_params)["code"][0]
    except (KeyError, TypeError):
        auth_code = ""

    return auth_code