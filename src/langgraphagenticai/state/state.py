from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain_core.messages import AnyMessage

class State(TypedDict):
    """
    Represents the structure of the state in the graph.
    """
    messages: Annotated[list[AnyMessage], add_messages]