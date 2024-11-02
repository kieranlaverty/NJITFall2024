
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent

from ai.pdf import book_engine
from ai.prompt import new_prompt, instruction_str, context

tools = [
    
    QueryEngineTool(
        query_engine=book_engine,
        metadata=ToolMetadata(
            name="Deep Learning",
            description="this gives detailed information about Deep Learning",
        ),
    ),
]

llm = Ollama(model="llama3", request_timeout=360.0)
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)
