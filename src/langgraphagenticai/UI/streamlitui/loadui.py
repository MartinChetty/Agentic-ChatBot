import streamlit as st
import os
from src.langgraphagenticai.UI.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
       st.set_page_config(page_icon=self.config.get_page_icon(), page_title=self.config.get_page_title(), layout="wide")
       st.header(self.config.get_page_title())

       with st.sidebar:
           llm_options = self.config.get_llm_options()
           use_case_options = self.config.get_use_case_options()

           #LLM Selection
           self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
           if self.user_controls["selected_llm"] == "Groq":
               #Model Selection for Groq
               model_options = self.config.get_groq_model_options()
               self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options) 
               self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")

               #validate API key presence
               if not self.user_controls["GROQ_API_KEY"]:
                   st.warning("Please enter your GROQ API key to proceed. Don't have one? Get it from https://console.groq.com/keys and paste it here.")
                   st.stop()

            #Use Case Selection
           self.user_controls["selected_usecase"] = st.selectbox("Select UseCases", use_case_options)

           if self.user_controls["selected_usecase"] == "Chatbot with WebSearch":
               os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Tavily API Key for Web Search", type="password")

               #validate API key presence
               if not self.user_controls["TAVILY_API_KEY"]:
                   st.warning("Please enter your Tavily API key to proceed. Don't have one? Get it from https://app.tavily.com/home and paste it here.")
                   st.stop()
            
       return self.user_controls
    