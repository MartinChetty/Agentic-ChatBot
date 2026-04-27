# Agentic AI Chatbot

Agentic AI chatbot application built with LangGraph and Streamlit.

## Features
- Basic chatbot flow
- Chatbot with web search via Tavily
- AI news summarizer (daily/weekly/monthly)

## Project Structure
- `src/langgraphagenticai/graph`: graph construction and routing
- `src/langgraphagenticai/nodes`: node logic for each use case
- `src/langgraphagenticai/LLMs`: model configuration
- `src/langgraphagenticai/UI`: Streamlit UI and config

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```

## Required API Keys
- `GROQ_API_KEY` for Groq LLM models
- `TAVILY_API_KEY` for web search and AI news summarization

You can provide keys from the Streamlit sidebar at runtime.