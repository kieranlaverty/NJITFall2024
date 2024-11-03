
import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader


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

def pdf_loading_engine(pdf_address, title):
    book_index = index(pdf_address, title)
    engine = book_index.as_query_engine(similarity_top_k=3)

    return engine