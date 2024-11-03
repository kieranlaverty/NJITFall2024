"""import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
from UI import index

mypdf = index
book_pdf = PDFReader().load_data(file="data\{}".format(mypdf))
book_index = index(book_pdf, "Deep")
book_engine = book_index.as_query_engine(similarity_top_k=3)
"""