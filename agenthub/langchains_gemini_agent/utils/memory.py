import os
from . import json

import chromadb

from llama_index.core import Document
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class LongTermMemory:
    def __init__(self):
        db = chromadb.Client()
        self.collection = db.get_or_create_collection(name="memories")
        vector_store = ChromaVectorStore(chroma_collection=self.collection)
        embed_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.index = VectorStoreIndex.from_vector_store(
            vector_store, embed_model=embed_model
        )
        self.thought_idx = 0

    def add_event(self, event):
        print("adding event to long term memory")
        doc = Document(
            text=json.dumps(event),
            doc_id=str(self.thought_idx),
            extra_info={
                "type": event["action"],
                "idx": self.thought_idx,
            },
        )
        print("doc created")
        self.thought_idx += 1
        print("inserting doc...")
        self.index.insert(doc)
        print("doc inserted")

    def search(self, query, k=10):
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=k,
        )
        results = retriever.retrieve(query)
        return [r.get_text() for r in results]
