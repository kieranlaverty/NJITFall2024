import os
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

def index(data, name):
    index = None
    if not os.path.exists(name):
        print("creating index", name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=name)

    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=name)
        )

    return index

pdf_path = os.path.join("data","DeepDiveIntoDeepLearning.pdf")
book_pdf = PDFReader().load_data(file="NJITFall2024\data\DeepDiveIntoDeepLearning.pdf")
book_index = index(book_pdf, "Deep Dive Into Deep Learning")
book_engine = book_index.as_query_engine()