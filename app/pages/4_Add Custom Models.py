import streamlit as st
import pandas as pd
from glob import glob
from vindent_utils.analysis_pipeline import score_new_custom_model

st.set_page_config(
    page_title="Add Custom Models",
    page_icon="",
    layout="wide"
)

st.title('Add Custom Text Classification Models')

st.write('''Add custom text classification models to Vinted\'s Video Interview Analysis tool. Custom text model allows you to classify answers based on what\'s important to your company.
This means, by providing text descriptions of your company's mission, descriptions of your culture values and desired mindsets and behaviours we can then score candidates answers to let
 you easily evaluate multiple candidates on what's important to your company outside of technical skill.''')

st.write('''For the AssemblyAI Hackathon, some custom text descriptions have been prefilled based on my company's values https://www.betterup.com/en/about-us?hsLang=en, however,
 you're welcome to add any text description to score against the audio interview responses.''')

# ***Add a rescore feature here, select a campaign and just run scoring on each file csv within the directory. easy
if 'user_id' not in st.session_state:
	st.session_state.user_id = 'assemblyai'

custom_models = pd.read_csv(f"app/pages/database/{st.session_state.user_id}/custom_models_{st.session_state.user_id}.csv", index_col=0)
# Need a form, prefill it

with st.form("my_form"):
    new_custom_model_name = st.text_input(label="Custom Model Name", placeholder="Model Name")
    new_custom_model_description = st.text_area(label="Custom Model Description",
                                    placeholder='For the best results, provide a 2-3 sentence description of what you want to evaluate and compare in your candidates responses.')

   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted and new_custom_model_description:
        custom_models = pd.concat([pd.DataFrame({"custom_model_name": new_custom_model_name, "custom_model_description": new_custom_model_description}, index=[0]), custom_models])
        custom_models.reset_index(inplace=True, drop=True)
        custom_models.drop_duplicates(subset="custom_model_name", keep="first", inplace=True)
        custom_models.to_csv(f"app/pages/database/{st.session_state.user_id}/custom_models_{st.session_state.user_id}.csv")
        files_to_score = list(glob(f'app/pages/database/{st.session_state.user_id}/campaigns/*/*/question*/analysis*.csv'))
        with st.spinner('Scoring Interview with new custom model'):
            for to_score in files_to_score:
                df = pd.read_csv(to_score)
                df = score_new_custom_model(df, custom_model={new_custom_model_name: new_custom_model_description})
                df.to_csv(to_score)
    # To add: A warning if this will overwrite a current custom model


with st.expander("Your Custom Models", expanded=False):
    for model_name, model_description in custom_models.values:
        st.write(f"MODEL: **{model_name}**")
        st.write(f"{model_description}")
        st.write("-"*10)



st.write("### How do Custom Models Work?")
st.write('''VintedAi uses semantic similarity modelling to determine how similar a candidates responses
 are to the provided text descriptions for custom models. This allows us to score the text and evaluate whether
  the candidates response is similar enough to your custom model text to be under your custom model in the candidate analysis dashboard''')
st.write('''This allows us to easily provide our users that ability to customize VintedAI's audio pre-screening test to your company's needs''')

# Current limitation, can't set these AFTER having started a campaign?