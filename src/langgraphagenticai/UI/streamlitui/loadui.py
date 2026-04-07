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
                   st.warning("Please enter your GROQ API key to proceed.")
                   st.stop()

            #Use Case Selection
           self.user_controls["selected_usecase"] = st.selectbox("Select UseCases", use_case_options)
            
       return self.user_controls
    