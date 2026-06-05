pip install -U langgraph langchain langchain-openai
pip install langchain-google-genai
pip install langgraph-cli
pip install -U "langgraph-cli[inmem]"
#inciar langgraph
langgraph dev

#Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
#iniciar uv
uv init
#Instalar dependencias
uv add langgraph langchain langchain-openai langchain-google-genai
#Instalar dependencia solo para desarrollo
uv add "langgraph-cli[inmem]" --dev
uv add ipykernel --dev
uv add grandalf --dev
#inciar langgraph con uv
uv run langgraph dev

#Instalar proyecto dev
uv pip install -e .
