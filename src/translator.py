class Translator:
    def __init__(self):
        self.provider = "Google Translate"
        self.api_key = None

    def set_provider(self, provider: str):
        self.provider = provider

    def set_api_key(self, key: str):
        self.api_key = key

    def translate(self, text: str) -> str:
        # Mock translation for now
        return f"[{self.provider}] {text}"
