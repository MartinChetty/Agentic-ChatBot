from src.langgraphagenticai.state.state import State

class ChatWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the state using the chatbot logic enhanced with tool integration.
        """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

        #simulate tool specific response handling
        tools_response = f"Tool Integration for input: {user_input}"

        return {"messages":[llm_response, tools_response]}
    
    def creat_chatbot(self, tools):
        """
        returns a chatbot node with tool integration.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returining the response.
            """
            return {"messages":[llm_with_tools.invoke(state["messages"])]}
        
        return chatbot_node


