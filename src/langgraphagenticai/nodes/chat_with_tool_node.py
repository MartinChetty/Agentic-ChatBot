from langchain_core.messages import SystemMessage
from ..state.state import State

SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are a helpful AI assistant with access to web search. "
        "Use search to answer questions that require current or factual information. "
        "Always cite your sources when using search results."
    )
)


class ChatWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """

    def __init__(self, model):
        self.llm = model

    def create_chatbot(self, tools):
        """
        returns a chatbot node with tool integration.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot node that prepends a system prompt before invoking the LLM.
            """
            messages = [SYSTEM_PROMPT] + list(state["messages"])
            return {"messages": [llm_with_tools.invoke(messages)]}

        return chatbot_node


