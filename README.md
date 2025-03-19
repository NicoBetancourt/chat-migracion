# LLM Agent for Migration and Political

## Project Overview

This project is a proof of concept for an intelligent chat system based on Large Language Models (LLMs) specialized in providing accurate and up-to-date information about migration processes to Spain and political asylum applications. The system leverages advanced Retrieval Augmented Generation (RAG) techniques to access official sources and legal documentation.

![image](https://github.com/user-attachments/assets/d479358e-5c52-4d8b-b6fa-c2e16e624d08)

## Technical Architecture

### Information Sources
- **Vectorized Documents**: Collection of official documents on migration and political asylum
- **Structured Database**: Results and resolutions from the BOE (Official State Bulletin) regarding asylum applications

### Processing Engine
- **LLM**: Currently using OpenAI API (GPT-4 or similar)
- **Planned Migration**: Azure OpenAI or Amazon Bedrock for GDPR and ISO 27001 compliance

### RAG System (Retrieval Augmented Generation)
- **Embeddings Engine**: OpenAI "text-embedding-3-small"
- **Query Tools**:
  - Tool for structured queries to the BOE
  - Tool for vector search in documents

## Data Processing

### Embeddings Generation
Embeddings are numerical representations (vectors) of texts that capture their semantic meaning. They allow:
- Converting documents into a format the system can "understand"
- Performing searches by semantic similarity, not just by keywords
- Finding relevant information even when different vocabulary is used

The project uses OpenAI's "text-embedding-3-small" model, which transforms texts into high-dimensional vectors, enabling precise searches in the document base.

### Data Storage
- **Vector Base**: Documents indexed using embeddings
- **Structured Base**: BOE data organized for specific queries

## Operation Flow
1. User makes a query about migration or political asylum
2. System analyzes the query and determines which tools to use
3. RAG activates the appropriate tools:
   - Vector search in relevant documents
   - Structured query to BOE data if necessary
4. LLM generates response based on retrieved information
5. System presents response to user

## Implementation

The project is implemented in Python with two interface options:
- **Web UI**: Built with Streamlit
- **API**: Implemented with FastAPI

## Getting Started

### Prerequisites
- Python 3.8+
- pip


### Running the Application

#### Streamlit Web Interface
```bash
streamlit run src/app.py
```
The web interface will be available at http://localhost:8501

#### FastAPI Service
```bash
uvicorn src.api:app --reload
```
The API documentation will be available at http://localhost:8000/docs


## Acknowledgments
- Spanish official migration and asylum documentation
- OpenAI for providing the LLM and embedding models
