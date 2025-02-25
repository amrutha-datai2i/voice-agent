import streamlit as st
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
import threading

# Initialize ElevenLabs client
API_KEY = "sk_856f6a1b42a4520697bd34d11149a8d1e42e27d98d72bdc9"  # Replace with your API key
AGENT_ID = "iji8JJCS4OTz3KU6XBq5"
client = ElevenLabs(api_key=API_KEY)

# Placeholder for the conversation instance
conversation = None
conversation_running = False

def initialize_conversation():
    global conversation, conversation_running

    try:
        # Initialize the conversation
        conversation = Conversation(
            client=client,
            agent_id=AGENT_ID,
            requires_auth=bool(API_KEY),
            audio_interface=DefaultAudioInterface(),
            callback_agent_response=lambda response: st.write(f"**Agent**: {response}"),
            callback_agent_response_correction=lambda original, corrected: st.write(f"**Correction**: {original} → {corrected}"),
            callback_user_transcript=lambda transcript: st.write(f"**You**: {transcript}"),
            callback_latency_measurement=lambda latency: st.write(f"**Latency**: {latency}ms"),
        )

        # Start the conversation in a background thread
        conversation_running = True
        threading.Thread(target=run_conversation, daemon=True).start()

    except Exception as e:
        st.error(f"An error occurred while initializing the conversation: {e}")

def run_conversation():
    global conversation_running

    try:
        # Start the conversation session
        conversation.start_session()
        conversation_id = conversation.wait_for_session_end()
        st.success(f"Conversation ended. Conversation ID: {conversation_id}")
    except Exception as e:
        st.error(f"An error occurred during the conversation: {e}")
    finally:
        conversation_running = False

# Streamlit UI
st.title("TATA AIG Voice Assistant")
st.image(
    "https://www.tataaig.com/logo-min.png",
    caption="Tata AIG Insurance",
    use_container_width=False,
    width=200
)

st.write("Press the button below to start a voice conversation. The microphone will be activated, and you can talk to the AI in real time.")

if st.button("Start Voice Conversation"):
    if conversation_running:
        st.warning("Conversation is already running. Please wait until it ends.")
    else:
        st.info("Initializing the voice assistant...")
        initialize_conversation()

# Display status of the conversation
if conversation_running:
    st.info("Voice assistant is running...")
else:
    st.success("Voice assistant is not running.")
