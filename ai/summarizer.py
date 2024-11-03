from transformers import pipeline
from llama_index.core.tools import FunctionTool


def summary(text):
    summarizer = pipeline("summarization", model="microsoft/phi-3.5-mini-instruct")
    summary = summarizer(text)
    return summary[0]['summary_text']

summary_engine = FunctionTool.from_defaults(
fn=summary,
name="summarizer",
description="this tool can summaizer text",
)