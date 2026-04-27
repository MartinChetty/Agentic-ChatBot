from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

class AINewsNode:
    def __init__(self,llm):
        """
        Initializes the AI News Node with API keys for Tavily and GROQ.
        """
        self.tavily = TavilyClient()
        self.llm=llm

        #this is used to capture variious steps in this file so that later can be used for step shown.
        self.state = {}
    
    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI News based on the specified frequency (daily, weekly, monthly) using the Tavily API.

        Args:
            state (dict): The state dictionary containing 'frequency'.

        Returns:
            dict: Update state with 'news_data' key containing the fetched news.
        """

        raw_frequency = state.get("messages", [""])[0]
        frequency = (getattr(raw_frequency, "content", raw_frequency) or "").lower()
        self.state['frequency'] = frequency  # Store frequency in state for later use
        time_range_map = {'daily' : 'd', 'weekly' : 'w', 'monthly' : 'm', 'yearly' : 'y'}
        days_map = {'daily' : 1, 'weekly' : 7, 'monthly' : 30, 'yearly' : 366}

        if frequency not in time_range_map:
            raise ValueError("Invalid frequency. Choose one of: daily, weekly, monthly, yearly.")

        response = self.tavily.search(
            query="Top Artificial Intelligence(AI) technology news India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
            #include_domains=["techcrunch.com", "thenextweb.com", "wired.com", "theverge.com", ...] #Uncomment and add more domains as needed
        )

        self.state['news_data'] = response.get('results', [])
        return {"messages": state.get("messages", [])}
    
    def summarize_news(self, state: dict) -> dict:
        """
        Summarizes the fetched news articles using the specified LLM.

        Args:
            state (dict): The state dictionary containing 'news_data' and 'frequency'.

        Returns:
            dict: Update state with 'summary' key containing the summarized news.
        """

        news_items = self.state.get('news_data', [])
        prompt_template = ChatPromptTemplate.from_messages([
            ("system","""Summarize AI news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles: \n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content','')}\nURL: {item.get('url','')}\nDate: {item.get('published_at',"")}"
            for item in news_items
        ])

        if not news_items:
            self.state['summary'] = "No AI news items were found for the selected timeframe."
            return {"messages": state.get("messages", [])}

        response = self.llm.invoke(prompt_template.format_prompt(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']  # Store summary in state for later use
        return {"messages": state.get("messages", [])}
    
    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        output_dir = Path("./AINews")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"{frequency}_summary.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# AI News Summary - {frequency.capitalize()}\n\n")
            f.write(summary)
        self.state['filename'] = str(filename)
        return {"messages": state.get("messages", [])}