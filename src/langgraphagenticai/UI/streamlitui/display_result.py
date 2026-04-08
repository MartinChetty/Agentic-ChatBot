import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages':("user", user_message)}):
                print(event.values())
                for value in event.values():
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value['messages'].content)

        elif usecase == "Chatbot with WebSearch":
            #prepare state and invoke the graph
            initial_state = {"messages":[user_message]}
            res=graph.invoke(initial_state)
            for message in res["messages"]:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool call started...")
                        st.write(message.content)
                        st.write("Tool call ended.")
                elif type(message) == AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)

        elif usecase == "AI News Summarizer":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news articles..."):
                result = graph.invoke({"messages":[frequency]})
                try:
                    #Read the markdown file content
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as f:
                        markdown_content = f.read() 

                    #Display the markdown content in Streamlit
                    st.markdown(markdown_content,unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News not generated or File not found: {AI_NEWS_PATH}.")
                except Exception as e:
                    st.error(f"An error occurred while loading the news summary: {str(e)}")
                    
