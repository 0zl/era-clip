from .settings import Settings

class Translator:
    def __init__(self):
        self.settings = Settings()

    def set_provider(self, provider: str):
        self.settings.update_translator_settings(provider=provider)

    def set_api_key(self, key: str):
        self.settings.update_translator_settings(api_key=key)

    def translate(self, text: str) -> str:
        # Mock translation for now
        return f"[{self.settings.translator_provider}] {text}"
