import os
import time
import cohere
import numpy as np
import pandas as pd
from transcribe import transcribe
from transformers import pipeline
from scipy.spatial.distance import cosine

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

classifier = pipeline("zero-shot-classification",
                      model="valhalla/distilbart-mnli-12-1")
built_ins = ["entrepreneurship", "confidence", "Growth Mindset"]

prefilled_models = {
    "Craftpersonship": "Find meaning in what we do through crafting excellence.",
    "Playfulness": "Great ideas come from health and happiness.",
    "Grit": "Perseverance driven by determination and passion.",
    "Empathy": "Innovation starts with understanding.",
    "Zest": "What sets you apart makes us unique.",
    "Courage": "Dare often and greatly."
}

def score_BART_text(text, model_name):
    pred = classifier(text, [model_name, "not " + model_name ])
    if pred["scores"][0] > pred["scores"][1] and pred["labels"][0] == model_name:
        return 1
    elif pred["scores"][1] > pred["scores"][0] and pred["labels"][1] == model_name:
        return 1
    else:
        return 0

def score_CUSTOM_text(text_embed, custom_model_embeds):
    mean_score = np.mean([cosine(e, text_embed) for e in custom_model_embeds.embeddings])
    if len(custom_model_embeds.embeddings) < 5:
        threshold = 1.0 - len(custom_model_embeds.embeddings) / 10
    else:
        threshold = 0.5
    if mean_score > threshold:
        return 1
    else:
        return 0

def score_custom_models(texts_df, customs_models=prefilled_models):
    for model_name in custom_models:
        _, embeds_custom = create_embeds(custom_models[model_name], user_id="test")
        texts_df[model_name] = texts_df["embeddings"].apply(lambda x: score_CUSTOM_text(x, embeds_custom))
        time.sleep(10) #Throttle since we're using the free tier for cohere
    return texts_df

def audio_pipeline(audio_file, question_id="test", user_id="test"):
    paragraphs = transcribe(audio_file, question_id="test", user_id="test")
    texts = " ".join([p["text"] for p in paragraphs])
    texts, embeds = create_embeds(texts)
    texts_df = pd.DataFrame({"text":texts, "embeddings": embeds.embeddings})
    texts_df = score_custom_models(texts_df)
    for model in built_ins:
         texts_df[model] = score_BART_text(texts_df["text"].values, model)
    texts_df.to_csv(f"results/analysis_{question_id}_{user_id}.csv")
    return f"results/analysis_{question_id}_{user_id}.csv"