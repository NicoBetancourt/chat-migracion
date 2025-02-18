import json
import os

from langchain_core.documents import Document
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoRepository:
    def __init__(
        self,
        db_name="migracion",
        collection_name="documentos",
        collection_resoluciones="resoluciones",
    ):
        mongo_uri = os.getenv("CLIENT_URL")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]
        self.collection_resoluciones: Collection = self.db[collection_resoluciones]

        # Inicializar embeddings de OpenAI
        self.openai_client = OpenAI()
        self.embeddings = OpenAIEmbeddings()

        # Inicializar el almacén vectorial
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.collection,
            embedding=self.embeddings,
            index_name="vector_index",
        )

    async def agregar_documento(self, texts: list[Document]):
        """Agrega un documento con embeddings generados a la base de datos."""
        for text in texts:
            embedding = self._generate_embeddings(text.page_content)
            self.collection.insert_one(
                {
                    "text": text.page_content,
                    "embedding": embedding,
                    "metadata": text.metadata,
                }
            )

    async def buscar_similares(self, query, k=7):
        """Busca documentos similares en la base de datos."""
        docs = self.vector_store.similarity_search(query, k)

        print("\n🔍 Resultados de la búsqueda:")
        for i, doc in enumerate(docs):
            print(f"🔹 {i + 1}. {doc.page_content}")

        return docs

    async def buscar_no_sql(self, query: str):
        """Busca documentos similares en la base de datos."""
        query_dict = json.loads(query)
        docs = self.collection_resoluciones.find(query_dict)
        documents = []
        for i, doc in enumerate(docs):
            documents.append(doc)
            print(f"🔹 {i + 1}. {doc}")
        return documents

    def _generate_embeddings(self, text: str) -> list[float]:
        embeddings_name = "text-embedding-3-small"
        response = self.openai_client.embeddings.create(
            input=text, model=embeddings_name
        )
        return response.data[0].embedding
