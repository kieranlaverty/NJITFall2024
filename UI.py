import streamlit as st
import PyPDF2
import os
from gtts import gTTS
import tempfile
import openai
#from AI_Fun import chatting, load_dotenv

# Load CSS file for customization
def load_css():
    with open("UI.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to process PDF
def process_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"  # Append each page's text
    return text

# Function to display chat messages
def display_chat_history():
    if st.session_state.messages:
        for message in st.session_state.messages:
            role = "You" if message['role'] == 'user' else "Study Buddy"
            st.markdown(f"<div class='{message['role']}-message'>{role}: {message['content']}</div>", unsafe_allow_html=True)

# Function to generate a bot response
def generate_response(user_input):
    if "hello" in user_input.lower():
        return "Hi there! How can I help you study today? \nPlease upload your textbook and we can get started"
    elif "help" in user_input.lower():
        return "Sure! What do you need help with?"
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I don't understand. Can you try asking differently?"

def text_to_speech(Text):
    tts = gTTS(text=Text, lang='en')
    # Use a temporary file to save the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
        tts.save(temp_audio_file.name)
        return temp_audio_file.name
    


# Main app function
def main():
    load_css( )

    st.title("TextBook Study Buddy")
    st.write("An application that can upload your textbooks and find your information.")
    st.write("I can help you study and learn in no time.")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF File of your Textbook (up to 5 GB)", type=["pdf"])

    if pdf_file is not None:
        with st.spinner("Processing PDF..."):
            pdf_text = process_pdf(pdf_file)
            print(pdf_text)
            st.success("PDF processed successfully!")
            # Display or process the extracted text as needed
            st.text_area("Extracted Text", pdf_text, height=300)


    # Initialize chat history and PDF readiness flag
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.pdf_ready = False 

    # Sidebar for history
    st.sidebar.title("Chat History")
    if st.sidebar.button("Clear History"):
        st.session_state.messages = []  # Clear history

    # User input for chat
    if st.session_state.pdf_ready:
        user_input = st.text_input("Student:", "")
        if st.button("Submit"):
            if user_input:
                st.session_state.messages.append({'role': 'user', 'content': user_input})
                bot_response = generate_response(user_input)
                st.session_state.messages.append({'role': 'bot', 'content': bot_response})
                
                # Convert bot response to speech
                audio_file_path = text_to_speech(bot_response)
                st.audio(audio_file_path)
    else:
        st.warning("Please upload a PDF file to enable the chat feature.")

    # Function to display chat messages
    def display_chat_history():
        if st.session_state.messages:
            for message in st.session_state.messages:
                role = "You" if message['role'] == 'user' else "Study Buddy"
                st.markdown(f"<div class='{message['role']}-message'>{role}: {message['content']}</div>", unsafe_allow_html=True)

    # Display chat history
    display_chat_history()

main()