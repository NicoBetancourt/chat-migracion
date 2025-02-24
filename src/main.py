import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from graph.state import State
from graph.workflow import workflow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Asegura que `POST` esté permitido
    allow_headers=["*"],
)
load_dotenv()

# Configuración de seguridad con Bearer Token
security = HTTPBearer()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica si el token es válido."""
    if credentials.credentials != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting up on port {os.getenv('PORT', 8000)}")
    logger.info(f"Running in environment: {os.getenv('ENV', 'development')}")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat/{item_id}")
async def read_item(
    item_id: int, input: list[dict], token: str = Depends(verify_token)
):
    app = workflow()
    comment = State({"messages": input})
    response = await app.ainvoke(comment)
    return {"response": response.get("messages")[-1].content}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
