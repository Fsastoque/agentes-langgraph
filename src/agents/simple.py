from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage

#Estado compartido
class State(MessagesState):
    customer_name: str
    my_age: int
    #mensaje: str
    
#Nodo
def node_1(state: State):
    if state.get("customer_name") is None:
        return {"customer_name": "Alice"}    #actualiza el estado compartido
    else:
        ai_msg = AIMessage(content=f"Hello {state['customer_name']}! How old are you?")
        return {"messages": [ai_msg]}
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
#builder.add_node("node_2", node_2)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)
#builder.add_edge("node_1", "node_2")
#builder.add_edge("node_2", END)

agent = builder.compile()