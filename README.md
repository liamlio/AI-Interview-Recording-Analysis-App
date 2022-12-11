# AI-Interview-Recording-Analysis-App

A pre-screening interview tool powered by AI to allow customers to screen more candidates at the top of their hiring funnel

## Get Started

If you'd like to test this app locally, please follow these steps:

1. Ensure you have `make` installed

The most simple choice is using Chocolatey. First you need to install this package manager. Once installed you simlpy need to install make (you may need to run it in an elevated/admin command prompt) :

`choco install make`  
Other recommended option is installing a Windows Subsystem for Linux (WSL/WSL2), so you'll have a Linux distribution of your choice embedded in Windows 10 where you'll be able to install make, gccand all the tools you need to build C programs.

2. This installation guide assumes you have miniconda installed for virtual environments, if you do not, you can manually create a virtual env and skip to step 4.
3. run `make env` to create a new conda environment
4. run `make install` to install all required dependencies of the app
5. Add an API Key for both [AssemblyAI](https://app.assemblyai.com/) and [CoHere](https://cohere.ai/) to these two files:

- https://github.com/liamlio/AI-Interview-Recording-Analysis-App/blob/main/vindent_utils/vindent_utils/analysis_pipeline.py
- https://github.com/liamlio/AI-Interview-Recording-Analysis-App/blob/main/vindent_utils/vindent_utils/transcribe.py

6. Finally, run `streamlit run app/_Home.py` from the command line to start the streamlit app locally.

7. Read more about the functionality of each app page in the devpost content below

## Devpost Post

Below is the content taken directly from the hackathon devpost.
