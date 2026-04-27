from configparser import ConfigParser
from pathlib import Path

class Config:
    def __init__(self, config_file: str | None = None):
        self.config = ConfigParser()
        default_config = Path(__file__).resolve().parent / "uiconfigfile.ini"
        config_path = Path(config_file) if config_file else default_config
        self.config.read(config_path)

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
    
    
