import streamlit as st
import PyPDF2
import os
from transformers import pipeline
from llama_index.core.tools import FunctionTool
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.core import Document
from ai.note_engine import note_engine
from ai.prompt import context
import shutil

# Load environment variables
load_dotenv()

# Load CSS file for customization
def load_css():
    with open("UI.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to process PDF from a file path
def process_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"  
    return text

# Function to index the PDF
def index(pdf_text, index_name):
    if not os.path.exists(index_name):
        print("Creating index:", index_name)
        # Create documents using the Document class
        documents = [Document(text=pdf_text)]  # Use the Document class for each text
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(StorageContext.from_defaults(persist_dir=index_name))
    return index

# Function to display notes in the sidebar
def display_notes():
    notes_file = os.path.join("data", "notes.txt")
    st.sidebar.header("Notes:")
    
    if os.path.exists(notes_file):
        with open(notes_file, "r") as f:
            notes = f.readlines()

        for note in notes:
            st.sidebar.write(note.strip())

        with open(notes_file, "rb") as f:
            st.sidebar.download_button("Download Notes", f, file_name="notes.txt", mime="text/plain")
    else:
        st.sidebar.write("No notes available.")


# Function to display chat messages
def display_chat_history():
    if st.session_state.messages:
        for message in st.session_state.messages:
            role = "You" if message['role'] == 'user' else "Study Buddy"
            st.markdown(f"<div class='{message['role']}-message'>{role}: {message['content']}</div>", unsafe_allow_html=True)

# Main app function
def main():
    load_css()
    st.title("TextBook Study Buddy")
    st.write("An application that can upload your textbooks and find your information.")
    st.write("I can help you study and learn in no time.")

    os.makedirs("data", exist_ok=True)


    # Sidebar for notes and clear history button
    st.sidebar.header("Clear History")
    if st.sidebar.button("Clear History"):
        st.session_state.clear()  
        st.session_state.pdf_ready = False 
        
        # Remove the uploaded PDF file
        for file in os.listdir("data"):
            file_path = os.path.join("data", file)
            os.remove(file_path)
        # Delete jason parsing 
        index_dir = "Deep"
        if os.path.exists(index_dir):
            shutil.rmtree(index_dir)
        
        st.experimental_rerun() 
 

    pdf_file = st.file_uploader("Upload a PDF File of your Textbook (up to 5 GB)", type=["pdf"])

    # Check if a PDF file has been uploaded
    if pdf_file is not None:
        saved_pdf_path = os.path.join("data", pdf_file.name)
        with open(saved_pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        st.write(f"Uploaded File Name: {pdf_file.name}")

        with st.spinner("Processing..."):
            pdf_text = process_pdf(saved_pdf_path)
            book_index = index(pdf_text, "Deep")
            book_engine = book_index.as_query_engine(similarity_top_k=3)
            llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")
            tools = [
                note_engine,
                QueryEngineTool(
                    query_engine=book_engine,
                    metadata=ToolMetadata(
                        name="tool",
                        description="This gives detailed information about Deep Learning",
                    ),
                ),
            ]
            agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

            st.session_state.agent = agent
            st.session_state.pdf_ready = True  

        # Check if the PDF has been processed
    if st.session_state.get("pdf_ready", False):
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        user_input = st.text_input("Ask a question about your textbook:", "", key="user_input")  # Use a key for session state
        submit_button = st.button("Submit")  # Add a submit button

        # Check if the submit button is clicked or user pressed Enter
        if submit_button or st.session_state.user_input:
            if user_input:  # Only process if user input is not empty
                st.session_state.messages.append({'role': 'user', 'content': user_input})
                bot_response = st.session_state.agent.query(user_input)
                st.session_state.messages.append({'role': 'bot', 'content': bot_response})

                # Display the bot's response immediately
                display_chat_history()

                # Save the note using the note_engine and update the notes display
                summary_text = f"Q: {user_input}\nA: {bot_response}"
                note_engine.call(summary_text)  
                display_notes() 

    else:
        st.warning("Please upload a PDF file to enable the chat feature and view the content.")

# Run the app
main()