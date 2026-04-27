import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk, ToolMessage


def _stream_graph_tokens(graph, messages: list):
    """Yield text tokens from a LangGraph graph for real-time streaming display."""
    for msg_chunk, _ in graph.stream(
        {"messages": messages}, stream_mode="messages"
    ):
        if (
            isinstance(msg_chunk, AIMessageChunk)
            and msg_chunk.content
        ):
            if isinstance(msg_chunk.content, str):
                yield msg_chunk.content
            elif isinstance(msg_chunk.content, list):
                for item in msg_chunk.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text = item.get("text", "")
                        if text:
                            yield text


class DisplayResultStreamlit:
    def __init__(self, usecase: str, graph, user_message: str):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def _render_chat_history(self):
        """Render all previously accumulated messages from session state."""
        for msg in st.session_state.get("chat_history", []):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                ts = msg.get("timestamp")
                if ts:
                    st.caption(ts)

    def _append_history(self, role: str, content: str):
        st.session_state.chat_history.append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    def _typing_indicator(self):
        return st.markdown(
            """
            <div class="typing-wrap">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _build_message_history(self) -> list:
        """Convert session-state chat history to LangChain message objects."""
        messages = []
        for msg in st.session_state.get("chat_history", []):
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        return messages

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # Reset history when the active use case changes
        if st.session_state.get("active_usecase") != usecase:
            st.session_state.chat_history = []
            st.session_state.active_usecase = usecase

        st.session_state.setdefault("chat_history", [])

        if usecase == "Basic Chatbot":
            self._render_chat_history()

            # Pass full conversation history so the LLM has context
            history = self._build_message_history()
            history.append(HumanMessage(content=user_message))

            with st.chat_message("user"):
                st.markdown(user_message)
                st.caption(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            with st.chat_message("assistant"):
                # Stream tokens in real time for a typewriter effect
                typing_placeholder = st.empty()
                with typing_placeholder:
                    self._typing_indicator()
                full_response = st.write_stream(_stream_graph_tokens(graph, history))
                typing_placeholder.empty()

            self._append_history("user", user_message)
            self._append_history("assistant", full_response or "")

        elif usecase == "Chatbot with WebSearch":
            self._render_chat_history()

            history = self._build_message_history()
            history.append(HumanMessage(content=user_message))
            history_len = len(history)

            with st.chat_message("user"):
                st.markdown(user_message)
                st.caption(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            with st.spinner("Searching the web..."):
                res = graph.invoke({"messages": history})

            ai_response = ""
            new_messages = res["messages"][history_len:]
            for message in new_messages:
                if isinstance(message, ToolMessage):
                    with st.expander("🔍 Web search results", expanded=False):
                        st.markdown(message.content)
                elif isinstance(message, AIMessage) and message.content:
                    ai_response = message.content
                    with st.chat_message("assistant"):
                        typing_placeholder = st.empty()
                        with typing_placeholder:
                            self._typing_indicator()
                        st.markdown(message.content)
                        typing_placeholder.empty()
                        st.caption(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            self._append_history("user", user_message)
            if ai_response:
                self._append_history("assistant", ai_response)

        elif usecase == "AI News Summarizer":
            frequency = user_message
            with st.spinner("Fetching and summarizing news articles..."):
                graph.invoke({"messages": [frequency]})

            try:
                ai_news_path = f"./AINews/{frequency.lower()}_summary.md"
                with open(ai_news_path, "r", encoding="utf-8") as f:
                    markdown_content = f.read()

                st.success(f"{frequency.title()} AI news summary generated successfully.")
                st.download_button(
                    label="Download Summary",
                    data=markdown_content,
                    file_name=f"ai_news_{frequency.lower()}_summary.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
                st.markdown(markdown_content, unsafe_allow_html=True)
            except FileNotFoundError:
                st.error(f"News summary not found: {ai_news_path}")
            except Exception as e:
                st.error(f"An error occurred loading the news summary: {str(e)}")
                    
