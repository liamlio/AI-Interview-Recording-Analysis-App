import os
import vindent_utils.utils as utils
import time
import requests

AAI_API_KEY = os.getenv("AAI_API_KEY")
AAI_API_KEY = ""

def transcribe(audio_file):
    if AAI_API_KEY is None:
        raise RuntimeError("AAI_API_KEY environment variable not set. Try setting it now.")

    # Create header with authorization along with content-type
    header = {
        'authorization': AAI_API_KEY,
        'content-type': 'application/json'
    }

    upload_url = utils.upload_file(audio_file, header)

    # Request a transcription
    transcript_response = utils.request_transcript(upload_url, header)

    # Create a polling endpoint that will let us check when the transcription is complete
    polling_endpoint = utils.make_polling_endpoint(transcript_response)

    # Wait until the transcription is complete
    while True:
        polling_response = requests.get(polling_endpoint, headers=header)
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)
    paragraphs = utils.get_paragraphs(polling_endpoint, header)

    # Save and print transcript
    # with open('transcript.json', 'w') as f:
    #     f = json.dumps(polling_response)
    
    # with open(f'transcript_{question_id}_{user_id}.txt', 'w') as f:
    #     for para in paragraphs:
    #         f.write(para['text'] + '\n')
    return paragraphs
