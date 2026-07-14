from langchain.agents import create_agent
from agents.support.nodes.booking.tools import tools
from agents.support.nodes.booking.prompt import prompt_template

system_prompt = """
Eres un asistente de ventas que ayuda a los clientes a encontrar los productos que necesitan y dar el clima de la ciudad

Tus tools son:
- get_products: para obtener los productos que ofreces en la tienda
- get_weather: para obtener el clima de la ciudad
"""

booking_node = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=tools,
    system_prompt=prompt_template.format(),
    #system_prompt=system_prompt,
)