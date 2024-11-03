"""from dotenv import load_dotenv
import os

from llama_index.llms.openai import OpenAI

from llama_index.core.tools import QueryEngineTool, ToolMetadata

from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent import ReActAgent

from ai.prompt import context
from ai.note_engine import note_engine
from ai.loading_PDF import pdf_loading_engine
from ai.pdf import book_engine


# Load environment variables from the .env file
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)



def chatting():
    
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

"""