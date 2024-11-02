import streamlit as st 

# Load CSS file for customization
def load_css():
    with open("UI.css") as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


st.title("\t\tStudy Buddy")
st.write("An application that can upload your textbooks and find your information\n")
st.write("I can help you study and learn in no time")


# Upload PDF file
pdf_file = st.file_uploader("Upload a PDF Files of your Textbook", type=["pdf"])



## for Text Input
# Initialize the chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar for history
st.sidebar.title("Chat History")
if st.sidebar.button("Clear History"):
    st.session_state.messages = []  # Clear history


# Display chat history in the sidebar
if st.session_state.messages:
    for message in st.session_state.messages:
        role = "Student" if message['role'] == 'user' else "Study Buddy"
        st.sidebar.write(f"{role}: {message['content']}")

# Function to generate a response (you can customize this)
def generate_response(user_input):
    # Simple keyword-based responses
    if "hello" in user_input.lower():
        return "Hi there! How can help you study today?"
    elif "help" in user_input.lower():
        return "Sure! What do you need help with?"
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I don't understand. Can you try asking differently?"

# Display the chat history
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.write(f"You: {message['content']}")
        st.markdown(f"<div class='user-message'>You: {message['content']}</div>", unsafe_allow_html=True)

    else:
        st.write(f"Study Buddy: {message['content']}")
        st.markdown(f"<div class='bot-message'>Study Buddy: {message['content']}</div>", unsafe_allow_html=True)
     


# User input
user_input = st.text_input("You:", "")
# Process user input
if st.button("Send"):
    if user_input:
        # Append user message to chat history
        st.session_state.messages.append({'role': 'user', 'content': user_input})

        # Generate a response
        bot_response = generate_response(user_input)
        # Append bot response to chat history
        st.session_state.messages.append({'role': 'bot', 'content': bot_response})

        # Clear input box
        st.experimental_rerun()



