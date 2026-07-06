from agents.support.state import State 
from langchain.chat_models import init_chat_model
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0)
llm = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 10:
        prompt = SYSTEM_PROMPT
        schema = llm.invoke([("system", prompt)] + history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state