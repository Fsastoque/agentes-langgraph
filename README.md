## Instalar Depedencias
* pip install -U langgraph langchain langchain-openai
* pip install langchain-google-genai
* pip install langgraph-cli
* pip install -U "langgraph-cli[inmem]"
## Iniciar langgraph

* langgraph dev
## Instalar `uv` gestor e instalador de paquetes

* curl -LsSf https://astral.sh/uv/install.sh | sh
* source ~/.bashrc
## Iniciar `uv`
* uv init
## Instalar dependencias con `uv`
* uv add langgraph langchain langchain-openai langchain-google-genai
* uv add langchain-google-vertexai    
## Instalar dependencias solo para desarrollo
* uv add "langgraph-cli[inmem]" --dev
* uv add ipykernel --dev
* uv add grandalf --dev
## Iniciar langgraph con `uv`
* uv run langgraph dev

## Instalar proyecto dev
* uv pip install -e .

## Levantar Docker
* docker compose up -d

### Fast API Checkpoint

<details>
<summary>Template</summary>

```py
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Depends
from typing import Annotated

from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = os.getenv("DB_URI")

# Global checkpointer instance
_checkpointer: PostgresSaver | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _checkpointer
    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        _checkpointer = checkpointer
        _checkpointer.setup()
        yield

def get_checkpointer() -> PostgresSaver:
    if _checkpointer is None:
        raise RuntimeError("Checkpointer not initialized. Make sure lifespan is running.")
    return _checkpointer

CheckpointerDep = Annotated[PostgresSaver, Depends(get_checkpointer)]
```
</details>