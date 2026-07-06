from agents.support.state import State 
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT
from langchain_core.messages import AIMessage

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")

llm = init_chat_model("gemini-2.5-flash",model_provider="google_genai", temperature=0)
#llm = llm.with_structured_output(schema=ContactInfo)

def conversation(state: State):
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1]
    customer_name = state.get("customer_name", 'John Doe')
    prompt = SYSTEM_PROMPT
    print('*'*100)
    print(getattr(last_message, "content", last_message))
    ai_message = llm.invoke([("system", prompt), ("user", getattr(last_message, "content", last_message))])
    new_state["messages"] = [ai_message]
    return new_state