from transformers import pipeline
from llama_index.core.tools import FunctionTool


def summary(text):
    summarizer = pipeline("summarization", model="microsoft/phi-3.5-mini-instruct")
    summary = summarizer(text)
    return summary[0]['summary_text']

x= summary("A Transformer is an architecture that has been extensively used in different domains like natural language processing and computer vision. It is composed of an encoder-decoder structure that enables the effective processing of sequential data. Transformers have been pretrained on large text datasets and have demonstrated effectiveness in tasks such as machine translation and text generation. Moreover, the development of vision Transformers has broadened the scope of Transformers to include computer vision applications, leading to impressive performance in tasks like image classification and visual recognition.")
print(x)