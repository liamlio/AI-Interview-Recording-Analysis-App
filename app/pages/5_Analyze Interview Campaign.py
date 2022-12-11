import streamlit as st
import pandas as pd
import os
import plotly.express as px
import matplotlib as mlp
from annotated_text import annotated_text, annotation
from vindent_utils.analysis_pipeline import BUILT_IN_MODELS

st.set_page_config(
    page_title="VintedAI Interview Analysis Dashboard",
    page_icon="",
    layout="wide"
)

if 'user_id' not in st.session_state:
	st.session_state.user_id = 'assemblyai'

st.title('Analyze Interview Campaigns Dashboard')

# Column to display models + model colours
# Small st.color_picker widget to change color
# Use st.empty to pop up a color_picker
# Use session_state to keep colour the same across sessions
# need a random colour first

left, right= st.columns([4, 1])
custom_models = pd.read_csv(f"app\pages\database\{st.session_state.user_id}\custom_models_{st.session_state.user_id}.csv", index_col=0)
custom_model_names = custom_models["custom_model_name"].values.tolist()
right.write("**VincentAI Models**")
for model in BUILT_IN_MODELS:
    right.checkbox(model, value=True, key=model)
right.write("")
right.write("**Custom Models**")
for custom_model in custom_model_names:
    right.checkbox(custom_model, value=True, key=custom_model)

# Set random colours
models = BUILT_IN_MODELS + custom_model_names
chosen_models =[]
for model in models:
    if st.session_state[model]:
        chosen_models.append(model)
models = chosen_models
cmap = mlp.cm.get_cmap('tab20', len(models))    # PiYG
cmap_hex = []
for i in range(cmap.N):
    rgba = cmap(i)
    # rgb2hex accepts rgb or rgba
    cmap_hex.append(mlp.colors.rgb2hex(rgba))

for i,model in enumerate(models):
    st.session_state[model+"_color"] = cmap_hex[i]
with left:
    with st.expander("Change Model Colours"):
        for model in models:
            st.session_state[model+"_color"] = st.color_picker(model, value=st.session_state[model+"_color"])
    
# Need a drop down to first select the current campaign, based on os file directory LOL
    interview_campaign = st.selectbox("Select Interview Campaign", options=os.listdir(f"app\pages\database\{st.session_state.user_id}\campaigns"),
                key="interview_campaign")
    campaign_path = f"app\pages\database\{st.session_state.user_id}\campaigns\{interview_campaign}"
    list_candidates = os.listdir(campaign_path)
    list_candidates.remove("questions")
    if interview_campaign:
         candidates = st.multiselect(
        "Select Candidate Responses",
        list_candidates,
        default=list_candidates,
        key="selected_candidates"
    )
    else:
        candidates = st.multiselect("Select Candidate Responses", [], disabled=True)
    
    if interview_campaign:
        st.write("## Audio Interview Response Analysis")
        questions = pd.read_json(campaign_path + f"\questions\questions.json", orient="records")
        for i, q in enumerate(questions["question"].values):
            st.write(f"### {q}")
            question_df = pd.DataFrame()
            for candidate in candidates:
                question_candidate_df = pd.read_csv(campaign_path + f"\{candidate}\question_{i}\\" + f"analysis_question_{i}.csv", index_col=0)
                text = "".join(question_candidate_df["text"].values.tolist())
                question_candidate_dict = question_candidate_df[models].mean(axis=0)
                question_candidate_dict["Candidate"] = candidate
                question_candidate_dict["Response"] = text
                question_candidate_dict["Response Length"] = len(question_candidate_df.values.tolist())
                question_df = question_df.append(question_candidate_dict.transpose(), ignore_index=True)
                del question_candidate_df
            del question_candidate_dict
            fig = px.bar(question_df, y=models, x="Candidate", barmode='group',
                        labels={'variable': 'Model'},
                        color_discrete_map={
                            model:st.session_state[model+"_color"] for model in models
                        })
            fig.update_layout(yaxis_title="Score")
            st.plotly_chart(fig, use_container_width=True)
            tabs = st.tabs(candidates)
            for j, candidate in enumerate(candidates):
                with tabs[j]:
                    text_models = st.multiselect(
                        "By Default, highlighted text is the highest scoring model, but some text could be classified under multiple models. To view alternative classification for the text you can disable some of the models below",
                        models,
                        default=models,
                        key=f"multiselect_text_models_{candidate}"
                     )
                    st.audio(campaign_path + f"\{candidate}\question_{i}\\" + f"question_{i}.mp3")
                    question_candidate_df = pd.read_csv(campaign_path + f"\{candidate}\question_{i}\\" + f"analysis_question_{i}.csv", index_col=0)
                    question_candidate_df["top_model"] = question_candidate_df[text_models].idxmax(axis=1)
                    question_candidate_df.drop("embeddings", axis=1, inplace=True)
                    question_candidate_df
                    to_annotated = []
                    for k, row in question_candidate_df.iterrows():
                        if k%5 == 0 and k != 0:
                            st.markdown(annotated_text(*tuple(to_annotated)), unsafe_allow_html=True)
                            to_annotated = []
                        if row[text_models].sum() > 0:
                            to_annotated.append((" " + row.text, st.session_state[row.top_model+"_color"]))
                        else:
                            to_annotated.append(" " + row.text)
                    if to_annotated:
                        st.markdown(annotated_text(*tuple(to_annotated)), unsafe_allow_html=True)
