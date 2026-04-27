import json
import os
from datetime import datetime

import streamlit as st

from ..uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def _inject_custom_css(self):
        st.markdown(
            """
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700&family=Plus+Jakarta+Sans:wght@500;700&display=swap');

                .stApp {
                    background:
                        radial-gradient(1100px 650px at 8% -15%, rgba(30, 202, 173, 0.20), transparent 60%),
                        linear-gradient(180deg, #081211 0%, #0a1918 55%, #0d201e 100%);
                    color: #e9f8f4;
                    font-family: 'Manrope', sans-serif;
                }

                h1, h2, h3 {
                    color: #f3fffc;
                    font-family: 'Plus Jakarta Sans', sans-serif;
                    letter-spacing: -0.02em;
                }

                .app-shell {
                    border: 1px solid #224a44;
                    border-radius: 18px;
                    padding: 1rem 1.2rem;
                    background: rgba(10, 29, 26, 0.74);
                    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.28);
                    margin-bottom: 0.8rem;
                }

                .app-title {
                    margin: 0;
                    font-weight: 700;
                    font-size: 1.3rem;
                    color: #f5fffc;
                }

                .app-subtitle {
                    margin: 0.3rem 0 0;
                    color: #a7d7cb;
                    font-size: 0.92rem;
                }

                .mini-pill {
                    display: inline-block;
                    border: 1px solid #2b6359;
                    border-radius: 999px;
                    background: #123a34;
                    color: #caf0e6;
                    font-size: 0.76rem;
                    padding: 0.2rem 0.55rem;
                    margin-top: 0.48rem;
                    margin-right: 0.32rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _resolve_api_key(self, key_name: str, sidebar_value: str) -> str:
        incoming = (sidebar_value or "").strip()
        env_value = os.getenv(key_name, "").strip()
        final_value = incoming or env_value
        if final_value:
            os.environ[key_name] = final_value
        return final_value

    def _render_header(self):
        selected_model = self.user_controls.get("selected_groq_model", "-")
        selected_usecase = self.user_controls.get("selected_usecase", "-")
        st.markdown(
            f"""
            <div class="app-shell">
                <p class="app-title">AI Co-Pilot</p>
                <p class="app-subtitle">A clean, production-ready assistant for chat, web-grounded answers, and AI news summaries.</p>
                <span class="mini-pill">{selected_usecase}</span>
                <span class="mini-pill">{selected_model}</span>
                <span class="mini-pill">{datetime.now().strftime('%b %d, %Y')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _render_export_actions(self):
        history = st.session_state.get("chat_history", [])
        if not history:
            st.caption("No messages yet. Export options appear after your first conversation.")
            return

        export_json = json.dumps(history, indent=2, ensure_ascii=False)

        md_lines = ["# Conversation Export", ""]
        for msg in history:
            ts = msg.get("timestamp", "")
            role = msg.get("role", "assistant")
            content = msg.get("content", "")
            md_lines.append(f"## {role.title()} ({ts})")
            md_lines.append(content)
            md_lines.append("")
        export_md = "\n".join(md_lines)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            "Export JSON",
            data=export_json,
            file_name=f"conversation_{stamp}.json",
            mime="application/json",
            use_container_width=True,
        )
        st.download_button(
            "Export Markdown",
            data=export_md,
            file_name=f"conversation_{stamp}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    def _render_compact_prompt_tools(self):
        usecase = self.user_controls.get("selected_usecase")
        st.subheader("Quick Start")

        template_map = {
            "Basic Chatbot": [
                "Explain agentic AI simply for a beginner.",
                "Create a 7-day LangGraph learning roadmap.",
                "Give 5 AI startup ideas for 2026.",
            ],
            "Chatbot with WebSearch": [
                "What are the latest open-source LLM updates this week?",
                "Compare Groq and other inference providers with sources.",
                "Show recent AI policy updates in India and EU.",
            ],
            "AI News Summarizer": [
                "daily",
                "weekly",
                "monthly",
            ],
        }

        options = template_map.get(usecase, [])
        if not options:
            return

        selected_template = st.selectbox("Suggested prompt", options)
        if st.button("Use Suggested Prompt", use_container_width=True):
            st.session_state["prompt_seed"] = selected_template

    def load_streamlit_ui(self):
        st.set_page_config(
            page_icon=self.config.get_page_icon(),
            page_title=self.config.get_page_title(),
            layout="wide",
        )

        self._inject_custom_css()
        st.title(self.config.get_page_title())

        st.session_state.setdefault("timeframe", "")
        st.session_state.setdefault("IsFetchButtonClicked", False)
        st.session_state.setdefault("chat_history", [])
        st.session_state.setdefault("prompt_seed", "")
        st.session_state.setdefault("active_usecase", None)

        with st.sidebar:
            st.markdown("## Navigation")
            self.user_controls["active_tab"] = st.radio(
                "",
                ["Chat", "News", "Settings"],
                label_visibility="collapsed",
            )

            st.divider()
            st.markdown("## Model")
            llm_options = self.config.get_llm_options()
            self.user_controls["selected_llm"] = st.selectbox("Provider", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Model", model_options)

            self.user_controls["temperature"] = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=0.7,
                step=0.05,
            )

            st.divider()
            st.markdown("## Keys")
            with st.expander("Update API Keys (optional)", expanded=False):
                groq_input = st.text_input("Groq API Key", type="password")
                self.user_controls["GROQ_API_KEY"] = self._resolve_api_key("GROQ_API_KEY", groq_input)

                tavily_input = st.text_input("Tavily API Key", type="password")
                self.user_controls["TAVILY_API_KEY"] = self._resolve_api_key("TAVILY_API_KEY", tavily_input)

            st.caption(
                "Groq: "
                + ("Connected" if self.user_controls.get("GROQ_API_KEY") else "Missing")
                + " | Tavily: "
                + ("Connected" if self.user_controls.get("TAVILY_API_KEY") else "Missing")
            )

            st.divider()
            st.markdown("## Conversation")
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.active_usecase = None
                st.session_state.prompt_seed = ""
            with st.expander("Export Conversation", expanded=False):
                self._render_export_actions()

            st.divider()
            active_tab = self.user_controls["active_tab"]
            if active_tab == "Chat":
                self.user_controls["selected_usecase"] = st.selectbox(
                    "Chat Mode",
                    ["Basic Chatbot", "Chatbot with WebSearch"],
                )
            elif active_tab == "News":
                self.user_controls["selected_usecase"] = "AI News Summarizer"
                time_frame = st.selectbox("News Timeframe", ["Daily", "Weekly", "Monthly"], index=0)
                if st.button("Generate News Summary", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame.lower()
            else:
                self.user_controls["selected_usecase"] = "Basic Chatbot"

            placeholder_map = {
                "Basic Chatbot": "Ask your question...",
                "Chatbot with WebSearch": "Ask and I will search the web when needed...",
                "AI News Summarizer": "Generate AI news summary for selected timeframe...",
            }
            self.user_controls["chat_placeholder"] = placeholder_map.get(
                self.user_controls["selected_usecase"],
                "Enter your prompt...",
            )

        self.user_controls["missing_groq_key"] = not bool(self.user_controls.get("GROQ_API_KEY"))
        self.user_controls["missing_tavily_key"] = (
            self.user_controls["selected_usecase"] in {"Chatbot with WebSearch", "AI News Summarizer"}
            and not bool(self.user_controls.get("TAVILY_API_KEY"))
        )

        self._render_header()
        if self.user_controls["active_tab"] in {"Chat", "News"}:
            self._render_compact_prompt_tools()
        else:
            st.info("Use the left sidebar to manage model settings and API connectivity.")

        return self.user_controls
