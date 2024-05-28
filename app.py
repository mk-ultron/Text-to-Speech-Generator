import streamlit as st
import openai
from pathlib import Path

# Load the OpenAI API key from Streamlit's secrets
api_key = st.secrets["api_keys"]["openai"]

def text_to_speech(text, filename, voice="alloy"):
    # Initialize the OpenAI client with the API key
    openai.api_key = api_key
    client = openai.OpenAI(api_key=api_key)
    
    # Make a request to OpenAI's TTS API to convert text to speech
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    
    # Save the audio content to a file
    speech_file_path = Path(filename)
    response.stream_to_file(speech_file_path)
    
    return filename

# Set the title of the Streamlit app
st.title("Online Text-to-Speech Reader")
st.subheader("Copy any text to convert to speech using Open AI's TTS Audio API. You can also download the result in .mp3 format")

# Text area for user input
text = st.text_area("Enter the text you want to convert to speech:")
voice = st.selectbox("Choose a voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])

# Check if the "Convert to Speech" button is clicked
if st.button("Convert to Speech"):
    if text:
        # If text is provided, convert it to speech and save it as an mp3 file
        filename = "output.mp3"
        file_path = text_to_speech(text, filename, voice)
        # Display the audio player with the generated mp3 file
        st.audio(file_path, format='audio/mp3')
        # Provide a download button for the mp3 file
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download MP3",  # Label for the download button
                data=file,             # Data to be downloaded
                file_name=filename,    # Name of the file to be downloaded
                mime="audio/mpeg"      # MIME type for the file
            )
    else:
        # Show a warning if no text is entered
        st.warning("Please enter some text to convert.")
