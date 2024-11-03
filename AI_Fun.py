from dotenv import load_dotenv
import os

from llama_index.llms.openai import OpenAI

from llama_index.core.tools import QueryEngineTool, ToolMetadata

from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent import ReActAgent

from ai.prompt import context
from ai.note_engine import note_engine
from ai.loading_PDF import pdf_loading_engine


# Load environment variables from the .env file
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# takes in a list
#source item = [[path, name, description]]
def tools(source, title, description):
    tools = [
        note_engine,
    ]
    for s in (source):
        tools.append(
            QueryEngineTool(
            query_engine=pdf_loading_engine(s, title),
            metadata=ToolMetadata(
                name=title,
                description=description
            ),
            )
        )




def chatting(source, title, description):
    llm =  OpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-3.5-turbo")

    agent = ReActAgent.from_tools(tools(source, title, description), llm=llm, verbose=True, context=context)

    while (prompt := input("Enter a prompt (q to quit): ")) != "q":
        result = agent.query(prompt)
        yield(result)
    
    

for i in chatting(source= ["data\DeepDiveIntoDeepLearning.pdf"], title = "Deep", description = "This gives detailed information about Deep Learning"]):
    print(i)
