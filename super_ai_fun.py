from dotenv import load_dotenv
import os

from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
from llama_index.llms.openai import OpenAI

from llama_index.core.tools import QueryEngineTool, ToolMetadata

from llama_index.core.agent import ReActAgent

from ai.prompt import context
from ai.note_engine import note_engine




# Load environment variables from the .env file
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)



def index(data, name):

    index = None
    if not os.path.exists(name):
        print("creating index", name)
        index = VectorStoreIndex.from_documents( data, show_progress=True)
        index.storage_context.persist(persist_dir=name)

    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=name)
        )

    return index

def chatting():

    file = input("filePath:  ")
    book_pdf = PDFReader().load_data(file=file)
    file_name = input("name:  ")
    book_index = index(book_pdf, file_name)
    book_engine = book_index.as_query_engine(similarity_top_k=3)

    desc = input("file description:  ")
    tools = [
        note_engine,
        QueryEngineTool(
            query_engine=book_engine,
            metadata=ToolMetadata(
                name=file_name,
                description= desc,
            ),
        ),

    ]

    llm =  OpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model="gpt-3.5-turbo")


    agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

    
    while True:
        prompt = input("Enter a prompt (q to quit): ")
        if prompt == "q":
            break
        result = agent.query(prompt)
        yield result
    return


for i in chatting():
    print(i)