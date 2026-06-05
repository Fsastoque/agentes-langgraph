#Estado compartido
class State:
    customer_name: str
    my_age: int
    
state: State = {}
customer_name = state.get("customer_name", None)
print(f"Hello {customer_name}!")

#Nodo
def node_1(state: State):
    if state.get("customer_name") is None:
        return {"customer_name": "Alice"}    #actualiza el estado compartido
    return {
        "my_age": 30
    }

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()