from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START, END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition,ToolNode
from src.langgraphagenticai.nodes.chat_with_tool_node import ChatWithToolNode


class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbots graph using LangGraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph structure. The chatbot node is set as both the
        entry and exit point of the graph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_websearch_build_graph(self):
        """
        Builds a chatbot with web search capabilities graph using LangGraph.
        This method initializes the necessary nodes for both chatbot and web search functionalities,
        and integrates them into the graph structure. The chatbot node is set as the entry point,
        while the web search node is connected to the chatbot node and serves as the exit point of the graph.
        """
        #Deine the tool and tool node for web search
        tools = get_tools()
        tool_node = create_tool_node(tools)

        #Define the LLM
        llm=self.llm

        #Define the chatbot node with the LLM and tool node
        obj_chatbot_with_node = ChatWithToolNode(llm)
        chatbot_node=obj_chatbot_with_node.creat_chatbot(tools)


        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)

        #Define the edges between the nodes
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
            {
                "tools": "tools",
                END: END
            }
            
            )
        self.graph_builder.add_edge("tools","chatbot")

    def setup_graph(self,usecase: str):
        """
        Sets up the graph based on the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with WebSearch":
            self.chatbot_with_websearch_build_graph()
        
        return self.graph_builder.compile()