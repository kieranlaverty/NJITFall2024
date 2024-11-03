import streamlit as st
import PyPDF2
import os
import time
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.core import Document
from ai.note_engine import note_engine
from ai.prompt import context

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
            text += page.extract_text() + "\n"  # Append each page's text
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

# Chatting function to get responses from the AI model
def chatting(agent, user_input):
    response = agent.query(user_input)
    return response

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

    # Ensure 'data' directory exists
    os.makedirs("data", exist_ok=True)

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF File of your Textbook (up to 5 GB)", type=["pdf"])

    if pdf_file is not None:
        # Save the uploaded PDF file to the 'data' directory
        saved_pdf_path = os.path.join("data", pdf_file.name)
        with open(saved_pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())  # Save the uploaded file to the path

        st.write(f"Uploaded File Name: {pdf_file.name}")

        # Process the PDF and display a loading message
        with st.spinner("Processing and indexing PDF..."):
            pdf_text = process_pdf(saved_pdf_path)  # Process the PDF from the saved path
            book_index = index(pdf_text, "Deep")  # Index the PDF text
            book_engine = book_index.as_query_engine(similarity_top_k=3)  # Create query engine
            llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")
            tools = [
                note_engine,
                QueryEngineTool(
                    query_engine=book_engine,
                    metadata=ToolMetadata(
                        name="Deep",
                        description="This gives detailed information about Deep Learning",
                    ),
                ),
            ]
            agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

            st.session_state.agent = agent  # Store agent in session state
            st.session_state.pdf_ready = True  # Set to True after indexing completes
            
            # Success message
            success_placeholder = st.empty()
            success_placeholder.success("PDF processed and indexed successfully!")
            time.sleep(5)  # Show the message for a short time
            success_placeholder.empty()

    # Only allow chat if the PDF has been processed
    if st.session_state.get("pdf_ready", False):
        # Initialize chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # User input for chat
        user_input = st.text_input("Ask a question about your textbook:", "")
        if st.button("Submit"):
            if user_input:
                st.session_state.messages.append({'role': 'user', 'content': user_input})
                bot_response = agent.query(user_input) 
                st.session_state.messages.append({'role': 'bot', 'content': bot_response})

        # Display chat history
        display_chat_history()

    else:
        st.warning("Please upload a PDF file to enable the chat feature and view the content.")

# Run the app
main()
