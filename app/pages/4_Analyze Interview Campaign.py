import streamlit as st
import pandas as pd
import os
import plotly.express as px
import matplotlib as mlp

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
                    f = open(campaign_path.replace("\\", "/") + f"/{candidate}/question_{i}/question_0.txt", "r")
                    lines = "\n".join(f.readlines())

                    fig = px.bar(text=lines)
                    fig.update_layout(yaxis_title="Score",
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)'
                                )
                    fig.update_xaxes(visible=False)
                    fig.update_yaxes(visible=False)
                    st.plotly_chart(fig, use_container_width=True)




# Analysis tool - base one includes everyone in the campaign

# Plots to compare? Bar graphs for average scores

# Text checking and audio checking
# Use tabs for this***
# Where you can look and listen to specific responses
# st.audio to display a play audio button!!
# This where I can have little boxes to say yes or no for what models to check on the side column
