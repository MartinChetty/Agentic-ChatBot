import streamlit as st
from src.langgraphagenticai.UI.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.UI.streamlitui.display_result import DisplayResultStreamlit



def load_langgraph_agenticai_app():
    """
    Loads and runs the Langgraph Agentic AI Streamlit application with Strreamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while implementing
    exception handling for robustness.

    """

    #Load UI and get user inputs
    ui=LoadStreamlitUI()
    user_inputs = ui.load_streamlit_ui()

    if not user_inputs:
        st.error("User inputs are not available. Please check the UI configuration.")
        return
    
    user_message = st.chat_input("Enter your message here:")

    if user_message:
        try:
            #configure the LLM's based on user selection
            obj_llm_config = GroqLLM(user_controls_input=user_inputs)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("LLM model could not be initialized. Please check your configuration and API key.")
                return
            
            #intitialize and set up the graph based on user selection
            usecase = user_inputs.get("selected_usecase")
            if not usecase:
                st.error("Use case selection is missing. Please select a use case from the sidebar.")
                return
            
            # Graph building and execution
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error setting up the graph for the selected use case: {str(e)}")
                return


        except Exception as e:
            st.error(f"An error occurred while configuring the LLM or setting up the graph: {str(e)}")
            return
    
