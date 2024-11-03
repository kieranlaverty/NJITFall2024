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


#pdf_path = os.path.join("data","DeepDiveIntoDeepLearning.pdf")
book_pdf = PDFReader().load_data(file="data\DeepDiveIntoDeepLearning.pdf")
book_index = index(book_pdf, "Deep")

book_pdf = PDFReader().load_data(file="data\DSM-5.pdf")
book_index = index(book_pdf, "Deep")
book_engine = book_index.as_query_engine(similarity_top_k=3)
