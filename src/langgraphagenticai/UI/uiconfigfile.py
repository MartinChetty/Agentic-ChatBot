from configparser import ConfigParser

class Config:
    def __init__(self, config_file='src/langgraphagenticai/UI/uiconfigfile.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    
    def get_use_case_options(self):
        return self.config["DEFAULT"].get("USE_CASE_OPTIONS").split(", ")
    
    def get_groq_model_options(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")
    
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
    
    def get_page_icon(self):
        return self.config["DEFAULT"].get("PAGE_ICON")
    
    
