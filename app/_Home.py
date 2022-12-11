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

st.write(
    """
    ## Inspiration
Over the last 5 years, I applied to hundreds of internships during my time as a co-op student at the University of Waterloo. For most software-related roles, I was required to complete coding pre-screen tests to evaluate my technical skills. In the years before I became a machine learning engineer, I worked in multiple wet-lab environments focused on material development. In contrast to software-related roles, pre-screening tests were never once required for positions related to wet-lab work.
 
This contrast in the hiring pipeline became significantly more apparent once I entered my first full-time role after university. Most notably, I realized that companies now look for candidates with certain sets of soft skills that align with work-culture values, as well as technical ability. So why is there only a technical pre-screening test? Why not a pre-screen to evaluate culture fit to screen candidates for soft skills like growth mindsets and creativity? At the company I work at, we often reject candidates for lacking our work-culture values even when their technical skill meets our expectations. Furthermore, according to criteria pre-employment testing, up to 78% of resumes are misleading, with up to 46% containing actual lies. Therefore, without tools to find qualities in our employees outside of their technical skills, we are very likely wasting resources on interviewing the wrong people.
 
Ultimately, when I was sourcing candidates for some of our open roles, I realized that many organizations are wasting several hours each month interviewing candidates that would not make it through our hiring pipeline due lack of mission alignment to our company, lack of culture fit, or for other reasons beyond technical skill. Because of this, I investigated whether any existing software could evaluate soft skills as one of the first steps of our hiring pipelines. I discovered that a handful of companies were doing pre-screening recorded video interviews with candidates. Companies like [Willo](https://www.willo.video) do recorded video interviews, but interviews lack analysis tools that can evaluate responses in a quantitative manner. Other software tools like [HireVue](https://www.hirevue.com/platform) create pre-screening assessments that use AI to facilitate quantitative comparison between candidates. However, neither of these popular platforms integrates AI to analyze recorded video or audio interviews, where candidates have the best chance to provide long-form responses to open-ended interview questions.
 
With pre-employment software representing an [8 billion dollar market](https://dataintelo.com/report/discount-link-pre-employment-testing-software-market/), but recorded video interviewing software only [representing a market size of 250 million](https://www.theinsightpartners.com/reports/video-interviewing-software-market), there is a significant opportunity to create a pre-screening product based on AI technology to change the interview process across hundreds of industries. Comparing this to the [market size of technical pre-screens of 300 million](https://www.blueweaveconsulting.com/report/technical-skills-screening-software-market-report) (which is only applicable to technical roles like software engineers), there is clearly significant room for growth in pre-screening software for non-technical roles like Sales, Marketing and Management that all heavily rely on interpersonal skills and other non-technical factors to perform well. Therefore, I believe this could be a potential Blue Ocean in bringing a similar experience of a technical screen to the non-technical market through AI-powered recorded interviews. This would share similar benefits as current recorded video pre-screening software by saving hundreds of hours on interviews per year for recruiters. In turn, this saves money, but also allows recruiters to screen more candidates than with existing software products since our AI models would allow for quantitative comparison without the need to watch hundreds of video submissions. With the ability to screen and evaluate more candidates based on non-technical skills, this software will enable companies to dedicate live interviews to candidates that are more likely to be hired. This will result in an accelerated and more successful interview process compared to the traditional method of selecting a dozen candidates for live interviews after only reviewing resumes.
 
 
## What it does
For this MVP I have built all the basic functionality you would need to get started sending pre-screening questions, with the exception of user authentication (details on why this was not possible in the timeframe are outlined in the Challenges section). The functionality created:
 
[Create a new audio-only interview campaign](http://35.85.66.222:8501/Create_Interview_Campaign)
Users can create a set of 3-5 questions that will then populate a separate page that they can send to potential candidates to submit audio recordings for each question. These results would then be scored against our AI Models and aggregated in a dashboard for viewing and comparison.
[Custom Models](http://35.85.66.222:8501/Add_Custom_Models)
From working in HR software companies in the past, custom models to score for attributes of interest at a particular company are one of the most used features for any HR software that looks at open-ended questions from surveys. In this case, we allow users to create a custom model by describing what they are trying to measure in a few sentences and scoring this against the transcribed audio submissions using CoHere embeddings and cosine similarity scores. This allows the MVP to easily integrate new custom text classification models so users can score candidates for their mission alignment to the company or for company-specific culture values. For the demo, I prefilled some custom models based on [my company’s values](https://www.betterup.com/en/about-us).
[Analysis Dashboard](http://35.85.66.222:8501/Analyze_Interview_Campaign)
Next, I implemented a dashboard where users can see the transcribed audio of all the candidate responses for a campaign, as well as the scores associated with each answer to each question as scored by the built-in models from Vinted AI and custom model scores.
[Candidate Audio Submission](http://35.85.66.222:8501/Audio_Interview)
The final MVP functionality is the page where users can submit audio files recorded from 3rd party software (more on why this choice was made in the Challenges section). These audio files are then transcribed using AssemblyAI, scored against the custom models using Cohere, and scored by VintedAI built-in models.
 
## How we built it
The entire webapp is built in Python and then hosted in an AWS EC2 instance to be accessible online, anywhere. The fronted and UI are all created through the streamlit library and streamlit components I have modified for this project. The transcription of audio files is done through the Assembly AI API. Custom model scoring is done through CoHere Embeddings and vector similarity scoring. Finally, all VintedAI built-in models for the MVP use zero-shot-classification through the [BART model](https://huggingface.co/valhalla/distilbart-mnli-12-1) to classify the text within the transcribed audio submissions.
 
## Challenges we ran into
There were two main challenges that limited some of the features developed for this MVP:
 
Log-in authentication with AWS Cognito issue with SSL Certificate
Record Audio in the app was too bulky and caused the app to crash. This was removed for the MVP version where the users have to now record their own audio with a 3rd party service instead.
 
For a complete MVP, I wanted the app to be deployed and accessible, while having user authentication implemented so only admin users could see the interview analysis dashboard. However, after creating an AWS Cognito group for user login and identifying the required authentication functions I could use to implement user authentication in my streamlit app, I realized I could not properly implement it due to a limitation on my EC2 Instance. AWS Cognito creates a login page for me but requires a callback link to send users back to my app after logging in. The issue here is that this callback link must be an HTTPS website, but at the moment, my EC2 instance is not. The solution to this is to get an SSL certificate and add it to the EC2 instance; however, due to the time constraint of the hackathon and that SSL certificates can take time to even request, I decided to leave this feature unfinished.
 
Originally, I implemented in-app audio recording so users could record their audio per question within the webapp; however, the implementation of the component I was using would lag and subsequently crash the entire app. Therefore, in the spirit of creating an MVP, I switched the built-in recording feature to a file upload system where users are asked to make their audio recording in a 3rd party software and then upload it to the app.
 
## Accomplishments that we are proud of
 
I am thrilled with how far I got with this project in just ~2 days, especially given that I barely knew streamlit when I started Friday night. I wanted to leverage this hackathon to give myself a deadline for this project so I could make a working version as fast as possible, and I definitely was able to accomplish that. Beyond personal satisfaction, I am also proud that I was able to get a working demo online that anyone can access and submit audio answers to be analyzed. This is enough functionality to have an alpha test with a real recruiter. With this version of the software, I can also test my business plan hypothesis to assess whether this application could be useful to recruiters by saving them time and enabling them to screen more candidates for non-technical roles.
 
## What we learned
 
Throughout this hackathon these were my main learnings:
 
How to use the Assembly AI API
How to use the Cohere API
How to use streamlit to create an MVP
That when creating an MVP, it's best to time constrain yourself to avoid creating needless features.
How to deploy an EC2 instance.
 
## What's next for VintedAI
 
After I have finished implementing user authentication after the hackathon and replace the IP4 domain with a custom domain, I want to interview recruiters to determine whether this product would be valuable to them and accrue interest into a proper paid Alpha test.
 
Once it is confirmed that this product is useful, I would then take the time to implement more robust models, a proper webapp in React, and a proper backend using databases instead of the volume of the virtual machine (MVP!).
 
"""
)
