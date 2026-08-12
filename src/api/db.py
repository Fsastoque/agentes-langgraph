import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Depends
from typing import Annotated

from langgraph.checkpoint.postgres import PostgresSaver

# DB_URI = os.getenv("DB_URI")
DB_URI = os.getenv("DB_URI")
if not DB_URI:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("DB_HOST", os.getenv("POSTGRES_HOST", "localhost"))
    port = os.getenv("DB_PORT", "5433")
    dbname = os.getenv("POSTGRES_DB", "my_course_agent")
    DB_URI = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Global checkpointer instance
_checkpointer: PostgresSaver | None = None

@asynccontextmanager
#Asigna el checkpointer a la variable global _checkpointer y lo inicializa con la conexión a la base de datos PostgreSQL. Luego, se asegura de que el checkpointer esté configurado antes de ceder el control al contexto del lifespan.
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

#Persistencia de memoria en base de datos PostgreSQL