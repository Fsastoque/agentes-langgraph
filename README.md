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
## Instalar dependencias solo para desarrollo
* uv add "langgraph-cli[inmem]" --dev
* uv add ipykernel --dev
* uv add grandalf --dev
## Iniciar langgraph con `uv`
* uv run langgraph dev

## Instalar proyecto dev
* uv pip install -e .
