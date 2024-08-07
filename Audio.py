# app.py
import streamlit as st
import requests
from pvrecorder import PvRecorder
import numpy as np
import tempfile
import os

# Define recording parameters
SAMPLE_RATE = 16000
RECORD_SECONDS = 5  # Duration to record

def record_audio():
    st.write("Press the button to start recording...")
    
    if st.button('Record'):
        st.write("Recording...")
        recorder = PvRecorder(sample_rate=SAMPLE_RATE, frame_length=1024)
        recorder.start()
        
        # Record for the specified duration
        audio_data = []
        for _ in range(int(SAMPLE_RATE / 1024 * RECORD_SECONDS)):
            audio_chunk = recorder.record()
            audio_data.append(audio_chunk)
        
        recorder.stop()
        st.write("Recording complete.")
        
        # Save the recorded audio to a temporary file
        audio_data = np.concatenate(audio_data)
        temp_file_path = tempfile.mktemp(suffix=".wav")
        with open(temp_file_path, "wb") as f:
            f.write(audio_data)
        
        return temp_file_path
    
    return None

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        response = requests.post("http://localhost:8000/transcribe/", files={"file": audio_file})
    return response.json()

def convert_text_to_speech(text):
    response = requests.post("http://localhost:8000/convert/", json={"text": text})
    return response.content

# Main Streamlit app
st.title("Speech-to-Text and Text-to-Speech Application")

audio_file_path = record_audio()

if audio_file_path:
    st.write("Processing your audio file...")
    
    # Transcribe the audio
    transcription_result = transcribe_audio(audio_file_path)
    st.write("Transcription result:")
    st.write(transcription_result["text"])
    
    # Convert text to speech
    audio_content = convert_text_to_speech(transcription_result["text"])
    
    st.write("Playing synthesized speech:")
    st.audio(audio_content, format="audio/mpeg")
    
    # Clean up temporary file
    os.remove(audio_file_path)

###########################################################################################################################
pip install fastapi uvicorn streamlit openai gtts requests pvrecorder
uvicorn main:app --reload
streamlit run app.py

# app.py
import streamlit as st
import requests
from io import BytesIO

st.title("Speech-to-Text and Text-to-Speech Application")

def record_audio():
    st.write("Recording audio...")
    audio_file = st.file_uploader("Upload your audio file", type=["wav"])
    if audio_file is not None:
        return audio_file
    return None

def transcribe_audio(audio_file):
    response = requests.post("http://localhost:8000/transcribe/", files={"file": audio_file})
    return response.json()

def convert_text_to_speech(text):
    response = requests.post("http://localhost:8000/convert/", json={"text": text})
    return response.content

audio_file = record_audio()
if audio_file:
    st.write("Processing your audio file...")
    # Transcribe the audio
    transcription_result = transcribe_audio(audio_file)
    st.write("Transcription result:")
    st.write(transcription_result["text"])

    # Convert text to speech
    audio_content = convert_text_to_speech(transcription_result["text"])

    st.write("Playing synthesized speech:")
    st.audio(BytesIO(audio_content), format="audio/mpeg")
