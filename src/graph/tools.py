from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from db.mongo import MongoRepository


def tavilyTool():
    return TavilySearchResults(
        max_results=5,
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        # search_depth="advanced",
        # include_domains = []
        # exclude_domains = []
    )


class Resolucion(BaseModel):
    nie: str = Field(description="Número de Identificación de Extranjero")
    expediente: int = Field(description="Número de expediente")
    tipo_archivo: str = Field(description="Tipo de archivo")
    Num_resolucion: int = Field(description="Número de resolución del BOE")
    fecha_resolucion: str = Field(description="Fecha de resolución")
    pagina: int = Field(description="Página de la resolución")


def tools():
    mongo = MongoRepository()

    @tool
    async def search_tool(query: str):
        """Find similar documents in the database, according to the query."""
        return await mongo.buscar_similares(query)

    @tool
    async def search_aggregation_tool(aggregation_query: str):
        """
        Find information in a database for users who are currently in an asylum process.
        Uses a NoSQL query to search for documents in the database. Use this structure:
        - nie: Número de Identificación de Extranjero (string).
        - expediente: Número de expediente (integer).
        - tipo_archivo: Tipo de archivo (string).
        - Num_resolucion: Número de resolución del BOE (integer).
        - fecha_resolucion: Fecha de resolución (string).
        - pagina: Página de la resolución (integer).
        """
        return await mongo.buscar_no_sql(aggregation_query)

    return [search_tool, search_aggregation_tool]
