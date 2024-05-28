import streamlit as st
import openai
import requests

# Load the OpenAI API key from Streamlit's secrets
openai.api_key = st.secrets["api_keys"]["openai"]

def text_to_speech(text, filename):
    # Make a request to OpenAI's TTS API to convert text to speech
    response = openai.Audio.create(
        model="text-to-speech",
        prompt=text,
        response_format="url"  # Specify the response format
    )
    
    # Extract the audio URL from the response
    audio_url = response['data'][0]['url']
    
    # Download the audio file from the response URL
    audio_content = requests.get(audio_url).content
    
    # Save the audio content to a file
    with open(filename, 'wb') as audio_file:
        audio_file.write(audio_content)
    
    return filename

# Set the title of the Streamlit app
st.title("Convert & Download Text to Speech in .mp3")

# Text area for user input
text = st.text_area("Enter the text you want to convert to speech:")

# Check if the "Convert to Speech" button is clicked
if st.button("Convert to Speech"):
    if text:
        # If text is provided, convert it to speech and save it as an mp3 file
        filename = "output.mp3"
        file_path = text_to_speech(text, filename)
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
