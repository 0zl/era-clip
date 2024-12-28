import deepl
from .settings import Settings

class Translator:
    def __init__(self):
        self.settings = Settings()
        self.deepl = None

        if self.settings.translator_api_key:
            self.deepl = deepl.Translator(self.settings.translator_api_key)

    def set_provider(self, provider: str):
        self.settings.update_translator_settings(provider=provider)

    def set_api_key(self, key: str):
        if key.strip():
            self.deepl = deepl.Translator(key.strip())
        self.settings.update_translator_settings(api_key=key.strip())

    def translate(self, text: str) -> str:
        if not text:
            return ""
        
        if not self.deepl:
            return "No API key provided."

        if self.settings.translator_provider == "DeepL":
            return self.deepl.translate_text(text, target_lang='EN-US').text
        else:
            raise ValueError("Invalid provider")
