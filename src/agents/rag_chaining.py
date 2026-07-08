from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model
from google import genai
from google.genai import types
import random


llm = init_chat_model("gemini-2.5-flash",model_provider="google_genai", temperature=0)
client = genai.Client()
archivo_pdf = client.files.upload(
    file="/home/fsastoque/desarrollo/langgraph/agentes-langgraph/Mobile_Site_Speed_Playbook.pdf",    
)

class State(MessagesState):
    customer_name: str
    phone: str
    my_age: str


from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")

#llm_with_structured_output = init_chat_model("anthropic:claude-3-5-sonnet-20240620", temperature=0)
llm_with_structured_output = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 10:
        schema = llm_with_structured_output.invoke(history)
        new_state["customer_name"] = schema.name        
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state

def conversation(state: State):
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1]
    customer_name = state.get("customer_name", 'John Doe')
    system_message = f"You are a helpful assistant that can answer questions about the customer {customer_name}"
    ai_message = llm.invoke([("system", system_message), ("user", last_message.text)])
    new_state["messages"] = [ai_message]
    return new_state

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, 'extractor')
builder.add_edge('extractor', 'conversation')
builder.add_edge('conversation', END)

agent = builder.compile()