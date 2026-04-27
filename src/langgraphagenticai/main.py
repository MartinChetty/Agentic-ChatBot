import streamlit as st
from dotenv import load_dotenv
from .UI.streamlitui.loadui import LoadStreamlitUI
from .LLMs.groqllm import GroqLLM
from .graph.graph_builder import GraphBuilder
from .UI.streamlitui.display_result import DisplayResultStreamlit

# Load API keys from .env file if present (safe no-op when file is absent)
load_dotenv()


def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph Agentic AI Streamlit application.
    Initialises the UI, routes user input to the correct graph,
    and delegates rendering to DisplayResultStreamlit.
    """

    ui = LoadStreamlitUI()
    user_inputs = ui.load_streamlit_ui()

    if not user_inputs:
        st.error("User inputs are not available. Please check the UI configuration.")
        return

    active_tab = user_inputs.get("active_tab", "Chat")
    chat_placeholder = user_inputs.get("chat_placeholder", "Enter your message here:")
    prompt_seed = st.session_state.get("prompt_seed", "").strip()

    if user_inputs.get("missing_groq_key"):
        st.warning("Groq API key is not available. Add it in sidebar or in .env to start chatting.")
    if user_inputs.get("missing_tavily_key") and active_tab in {"Chat", "News"}:
        st.warning("Tavily API key is missing for web search/news. Add it in sidebar or in .env.")

    if active_tab == "Settings":
        st.subheader("Settings")
        st.info("Configure provider, model, temperature, and API keys from the sidebar.")
        return

    # Determine user message: either from the news-fetch button or the chat input
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
        # Reset the flag immediately so subsequent reruns don't re-trigger
        st.session_state.IsFetchButtonClicked = False
    elif prompt_seed:
        user_message = prompt_seed
        st.session_state.prompt_seed = ""
    else:
        user_message = st.chat_input(chat_placeholder)

    if user_message:
        try:
            if user_inputs.get("missing_groq_key"):
                return

            usecase = user_inputs.get("selected_usecase")
            if usecase in {"Chatbot with WebSearch", "AI News Summarizer"} and user_inputs.get("missing_tavily_key"):
                return

            obj_llm_config = GroqLLM(user_controls_input=user_inputs)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("LLM model could not be initialised. Please check your configuration and API key.")
                return

            if not usecase:
                st.error("Use case selection is missing. Please select a use case from the sidebar.")
                return

            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph(usecase)
            DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()

        except Exception as e:
            st.error(f"An error occurred while processing your request: {str(e)}")

