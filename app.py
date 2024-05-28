import streamlit as st
import openai
from pathlib import Path

# Load the OpenAI API key from Streamlit's secrets
api_key = st.secrets["api_keys"]["openai"]

# Function to convert text to speech
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

# HTML Template for the stories
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fast AI Fiction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(to bottom right, #ffffff, #ffcccc, #ccffcc, #ccccff);
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #333;
        }
        #stories {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            padding: 20px;
        }
        .story {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            width: 300px;
            margin: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease-in-out;
            overflow: hidden;
        }
        .story img {
            width: 100%;
            height: auto;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
        }
        .story h2 {
            font-size: 1.5em;
            margin: 10px 0;
        }
        .story p {
            font-size: 1em;
            color: #555;
            text-align: left;
        }
        .story button {
            background-color: #6eb363;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
        }
        .story button:hover {
            background: linear-gradient(to bottom right, #ffffff, #ffcccc, #ccffcc, #ccccff);
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        p.summary {
            min-height: 12vh;
        }
        .full-text {
            display: none;
            margin-top: 10px;
            text-align: left;
            max-height: calc(100vh - 120px);
            overflow-y: auto;
        }
        .story.expanded {
            display: flex;
            flex-direction: column;
            width: 80%;
            max-width: 800px;
            height: auto;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1000;
            overflow: hidden;
            background-color: #fff;
            padding: 20px;
        }
        .story.expanded img {
            width: 300px;
            height: auto;
            border-radius: 8px;
            cursor: pointer;
        }
        .story.expanded .content {
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            margin-top: 20px;
        }
        .story.expanded .content .text {
            margin-left: 20px;
            flex-grow: 1;
        }
        .story.expanded .summary,
        .story.expanded button:not(.close-btn) {
            display: none;
        }
        .close-btn {
            display: none;
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
        }
        .close-btn:hover {
            background-color: #3c3c3c;
        }
        .story.expanded .close-btn {
            display: inline-block;
        }
        .expanded-view {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            max-width: 800px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-height: 90vh;
            overflow-y: scroll;
            overflow-x: hidden;
            z-index: 1000;
            padding: 20px;
            transition: opacity 0.3s ease-in-out;
            flex-direction: column;
            align-items: center;
        }
        .expanded-view img {
            width: 300px;
            height: auto;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .expanded-view h2 {
            text-align: center;
        }
        .expanded-view .content {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
            width: 100%;
        }
        .expanded-view .content .text {
            margin-top: 20px;
            max-height: calc(100vh - 220px);
            overflow-y: auto;
            width: 100%;
            text-align: left;
        }
        .close-btn {
            display: block;
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            margin: 20px 0 0;
            cursor: pointer;
        }
        .close-btn:hover {
            background-color: #d32f2f;
        }
        .title {
            text-align: center;
            margin: 20px 0;
            font-size: 2.5em;
            color: #333;
        }
    </style>
</head>
<body>
    <h1 class="title">Fast AI Fiction</h1>
    <div id="stories">
        <!-- Stories will be inserted here by Streamlit -->
    </div>
    <div id="expanded-view" class="expanded-view"></div>
    <script>
        function toggleStory(storyId) {
            var storyElement = document.getElementById(storyId);
            if (storyElement) {
                var fullText = storyElement.querySelector('.full-text').innerHTML;
                var imageSrc = storyElement.querySelector('img').src;
                var title = storyElement.querySelector('h2').innerText;
                var audioSrc = storyElement.querySelector('audio').src;

                var expandedView = document.getElementById('expanded-view');
                expandedView.innerHTML = `
                    <img src="${imageSrc}" alt="Thumbnail for ${title}">
                    <h2>${title}</h2>
                    <div class="content">
                        <div class="text">${fullText}</div>
                    </div>
                    <audio controls src="${audioSrc}"></audio>
                    <button class="close-btn" onclick="closeExpandedView()">Close</button>
                `;

                expandedView.style.display = 'flex';
                setTimeout(() => {
                    expandedView.style.opacity = '1';
                }, 0);
            } else {
                console.error('Story element not found:', storyId);
            }
        }

        function closeExpandedView() {
            var expandedView = document.getElementById('expanded-view');
            expandedView.style.opacity = '0';
            setTimeout(() => {
                expandedView.style.display = 'none';
            }, 300);
        }

        function togglePlayPause(storyId) {
            var audioElement = document.getElementById('audio-' + storyId);
            var button = document.getElementById('listen-btn-' + storyId);
            if (audioElement) {
                if (audioElement.paused) {
                    audioElement.play();
                    button.textContent = 'Pause';
                } else {
                    audioElement.pause();
                    button.textContent = 'Play';
                }
            } else {
                console.error('Audio element not found:', storyId);
            }
        }

        function updateButtonText(storyId) {
            var audioElement = document.getElementById('audio-' + storyId);
            var button = document.getElementById('listen-btn-' + storyId);
            if (audioElement.paused) {
                button.textContent = 'Play';
            } else {
                button.textContent = 'Pause';
            }
        }

        function resetButtonText(storyId) {
            var audioElement = document.getElementById('audio-' + storyId);
            var button = document.getElementById('listen-btn-' + storyId);
            if (audioElement.paused) {
                button.textContent = 'Play';
            } else {
                button.textContent = 'Pause';
            }
        }

        function downloadAudio(storyId) {
            var audioSrc = document.getElementById('audio-' + storyId).src;
            var link = document.createElement('a');
            link.href = audioSrc;
            link.download = storyId + '.mp3';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
"""

# Function to render stories in HTML
def render_stories():
    stories = [
        {
            "id": "story1",
            "title": "The Unlikely Hero",
            "summary": "In a galaxy torn apart by war, a humble mechanic named Kira discovers a dying prince and a secret that could unite the warring factions against an ancient, unstoppable force. Embark on an interstellar journey of courage and hope as Kira rises to become the hero the galaxy never expected.",
            "full_text": """
                <p>The galaxy was at war. Starfleets clashed in the cold void, planets burned, and alliances crumbled. Amidst this chaos, Kira, a lowly mechanic on the barren moon of Kestris, found herself thrust into the heart of the conflict. She had always believed her life would be spent repairing starships and dreaming of adventure, but fate had other plans.</p>
                <p>One fateful day, while scavenging for parts, Kira stumbled upon a crashed escape pod. Inside was a gravely injured alien who identified himself as Prince Thallan, heir to the Throne of Arion, a planet key to the balance of power in the galaxy. The prince carried a message of a greater threat—an ancient, malevolent force from beyond the stars, known as the Voidbringers, poised to conquer and consume all in their path.</p>
                <p>With his dying breath, Prince Thallan entrusted Kira with a data crystal containing vital information that could unite the warring factions against the Voidbringers. Kira, never one to shirk from a challenge, vowed to honor the prince's last wish. She repaired a derelict starfighter, took the crystal, and embarked on a perilous journey.</p>
                <p>Her path was fraught with danger—she faced hostile patrols, treacherous smugglers, and the ever-looming threat of the Voidbringers. Along the way, she forged unlikely alliances with rebels, outlaws, and soldiers from enemy planets. Kira's courage and determination inspired those she met, and her mission quickly became a beacon of hope.</p>
                <p>In the climactic battle, as the Voidbringers descended upon the galaxy, Kira's ragtag fleet, now united, launched a desperate defense. With the help of the data crystal, they discovered the Voidbringers' weakness and struck a decisive blow. The galaxy, though scarred by war, was saved.</p>
                <p>Kira, the mechanic turned hero, had done the impossible. She had united the galaxy and defeated the greatest threat it had ever faced. The war ended, and peace, though fragile, began to bloom. Kira returned to Kestris, but her name would forever be remembered among the stars.</p>
            """
        },
        # Define other stories here with the same structure
    ]

    stories_html = ""
    for story in stories:
        audio_content = text_to_speech(story["summary"])
        audio_file = f"{story['id']}.mp3"
        with open(audio_file, "wb") as file:
            file.write(audio_content)
        
        story_html = f"""
        <div class="story" id="{story['id']}">
            <img src="story-image1.png" alt="Thumbnail for {story['title']}" onclick="toggleStory('{story['id']}')">
            <h2>{story['title']}</h2>
            <p class="summary">{story['summary']}</p>
            <button onclick="toggleStory('{story['id']}')">Read</button>
            <div class="full-text">{story['full_text']}</div>
            <audio id="audio-{story['id']}" src="{audio_file}"></audio>
            <button id="listen-btn-{story['id']}" onclick="togglePlayPause('{story['id']}')" onmouseover="updateButtonText('{story['id']}')" onmouseout="resetButtonText('{story['id']}')">Play</button>
            <button onclick="downloadAudio('{story['id']}')">Download</button>
        </div>
        """
        stories_html += story_html
    
    return stories_html

st.title("Fast AI Fiction")
st.markdown(html_template, unsafe_allow_html=True)
stories_html = render_stories()
st.markdown(stories_html, unsafe_allow_html=True)
