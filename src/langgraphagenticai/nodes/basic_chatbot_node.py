from langchain_core.messages import SystemMessage
from ..state.state import State

SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are a helpful, knowledgeable AI assistant. "
        "Answer questions clearly and concisely. "
        "If you are unsure, say so honestly rather than guessing."
    )
)


class BasicChatbotNode:
    """
    Basic chatbot logic implementation.
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a chatbot response.
        Prepends a system prompt so the model knows its role.
        """
        messages = [SYSTEM_PROMPT] + list(state["messages"])
        return {"messages": [self.llm.invoke(messages)]}