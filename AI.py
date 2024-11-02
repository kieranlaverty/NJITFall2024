from dotenv import load_dotenv
import os

from llama_index.llms.openai import OpenAI

from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent

from ai.pdf import book_engine
from ai.prompt import new_prompt, instruction_str, context

# Load environment variables from the .env file
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

tools = [
    
    QueryEngineTool(
        query_engine=book_engine,
        metadata=ToolMetadata(
            name="Deep Dive Into Deep Learning",
            description="this gives detailed information about Deep Learning",
        ),
    ),
]

llm =  OpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-3.5-turbo")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)
