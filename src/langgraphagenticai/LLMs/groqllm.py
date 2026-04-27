import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get("GROQ_API_KEY", "").strip()
            selected_groq_model = self.user_controls_input["selected_groq_model"]
            temperature = float(self.user_controls_input.get("temperature", 0.7))

            env_key = os.getenv("GROQ_API_KEY", "").strip()
            if not groq_api_key:
                groq_api_key = env_key

            if not groq_api_key:
                st.error("GROQ API key is missing. Please provide it in the sidebar.")
                raise ValueError("Missing GROQ API key")

            llm = ChatGroq(
                model=selected_groq_model,
                api_key=groq_api_key,
                temperature=temperature,
            )

        except Exception as e:
            raise ValueError(f"Error initializing GROQ LLM: {str(e)}")
        return llm