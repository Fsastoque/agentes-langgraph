from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model
import random

llm = init_chat_model("gemini-2.5-flash",model_provider="google_genai", temperature=1)

#Estado compartido
class State(MessagesState):
    customer_name: str
    my_age: int
    #mensaje: str
    
#Nodo
def node_1(state: State):    
    new_state: State = {}
    if state.get("customer_name") is None:
        new_state["customer_name"] = "John Doe"
        #return {"customer_name": "Alice"}    #actualiza el estado compartido
    else:
        new_state["my_age"] = random.randint(20, 30)

    history = state["messages"]
    ai_message = llm.invoke(history)
    new_state["messages"] = [ai_message]
    return new_state
        #ai_msg = AIMessage(content=f"Hello {state['customer_name']}! How old are you?")
        #return {"messages": [ai_msg]}
    #return {
     #   "my_age": 30
    #}

#Nodo 2
'''def node_2(state: State):
    edad = state.get("my_age", None)
    respuesta = "You are a minor."
    if edad >= 18:        
        respuesta = "You are an adult."
    return {
        "mensaje": respuesta
    }'''

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("node_1", node_1)
#builder.add_node("node_2", node_2)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)
#builder.add_edge("node_1", "node_2")
#builder.add_edge("node_2", END)

agent = builder.compile()