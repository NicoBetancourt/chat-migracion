import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from graph.state import State
from graph.workflow import workflow

app = FastAPI()
load_dotenv()

# Configuración de seguridad con Bearer Token
security = HTTPBearer()
TOKEN = os.getenv("TOKEN")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica si el token es válido."""
    if credentials.credentials != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


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
