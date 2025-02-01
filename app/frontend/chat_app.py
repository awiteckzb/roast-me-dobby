import streamlit as st
from PIL import Image
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


from app.services.vision.feature_extractor import FeatureExtractor

from app.core.agent import ChatAgent
from app.prompts import *
import io


@st.cache_resource
def init_feature_extractor():
    return FeatureExtractor()


class Message:
    def __init__(self, content, role="user", image=None):
        self.content = content
        self.role = role  # "user" or "assistant"
        self.image = image


class ChatInterface:
    def __init__(self):
        self.setup_streamlit()
        self.initialize_session_state()
        self.feature_extractor = init_feature_extractor()

    def setup_streamlit(self):
        st.set_page_config(
            page_title="Roast me Dobby 😩", page_icon="🔥", layout="wide"
        )

        st.markdown(
            """
            <style>
            .chat-message {
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                margin-left: 2rem;
                margin-right: 2rem;
            }
            .user-message {
                background-color: #e6f3ff;
                margin-right: 4rem;
            }
            .assistant-message {
                background-color: #f0f2f6;
                margin-left: 4rem;
            }
            .message-content {
                margin: 0;
            }
            .message-image {
                max-width: 200px;
                margin-bottom: 0.5rem;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

    def initialize_session_state(self):
        # Add mode to the default state
        default_state = {
            "messages": [],
            "chat_agent": None,
            "initial_roast_done": False,
            "mode": "roast",  # default to roast mode
        }

        for key, default_value in default_state.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    def display_message(self, message):
        # print(f"Displaying message: {message.content} for role: {message.role}")
        message_class = (
            "assistant-message" if message.role == "assistant" else "user-message"
        )

        with st.container():
            col1, col2, col3 = st.columns([1, 10, 1])
            with col2:
                with st.container():
                    # Handle the uploads photo message differently
                    if message.content == "*uploads photo*":
                        content = "<i>uploads photo</i>"
                    else:
                        # For all other messages, use streamlit's markdown
                        content = message.content

                    message_html = f"""
                        <div class="chat-message {message_class}">
                            <div class="message-content">{content}</div>
                        </div>
                    """

                    if message.image is not None:
                        st.image(message.image, width=200)

                    st.markdown(message_html, unsafe_allow_html=True)

    def process_initial_upload(self, uploaded_file):
        try:
            # print("Processing initial upload")
            image = Image.open(uploaded_file)

            with st.spinner(
                f"Dobby's looking at your {'ugly' if st.session_state.mode=='roast' else 'cute'} ass"
            ):
                # print("Extracting features")
                features = self.feature_extractor.extract_features(image)
                st.session_state.chat_agent = ChatAgent(features, st.session_state.mode)

                initial_prompt = (
                    "annihilate me papa.."
                    if st.session_state.mode == "roast"
                    else "smother me in love papa"
                )

                print("Got features, generating response")

                response = st.session_state.chat_agent.generate_response(initial_prompt)
                st.session_state.messages.append(
                    Message("*uploads photo*", "user", image)
                )
                st.session_state.messages.append(Message(response, "assistant"))
                st.session_state.initial_roast_done = True

            return True
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return False

    def process_chat_input(self, user_input):
        try:
            st.session_state.messages.append(Message(user_input, "user"))

            with st.spinner("Dobby is cookin.."):
                ai_response = st.session_state.chat_agent.generate_response(user_input)
                st.session_state.messages.append(Message(ai_response, "assistant"))

            return True
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return False

    def run(self):
        st.title("Roast me Dobby 😩")

        mode = st.toggle("Nice Mode", help="Toggle between roasting and complimenting")
        st.session_state.mode = "nice" if mode else "roast"

        # Show current mode with some flair
        if st.session_state.mode == "roast":
            st.markdown("*😈 Roast mode activated - Dobby chooses violence*")
        else:
            st.markdown("*❤️ Nice mode activated - Dobby spreads love*")

        # Initial image upload if chat hasn't started
        if not st.session_state.initial_roast_done:
            uploaded_file = st.file_uploader(
                "Upload your photo to start", type=["jpg", "jpeg", "png"]
            )

            if uploaded_file and self.process_initial_upload(uploaded_file):
                st.rerun()

        # Display chat history
        for message in st.session_state.messages:
            self.display_message(message)

        # Chat input if roast has started
        if st.session_state.initial_roast_done:
            user_input = st.chat_input("Your response...")

            if user_input and self.process_chat_input(user_input):
                st.rerun()


if __name__ == "__main__":
    chat_interface = ChatInterface()
    chat_interface.run()
