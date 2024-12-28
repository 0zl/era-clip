import deepl
from .settings import Settings
from .translation_cache import TranslationCache

class Translator:
    def __init__(self):
        self.settings = Settings()
        self.deepl = None
        self.cache = TranslationCache()

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

        # Check cache first
        text_hash = self.cache.get_hash(text)
        cached_translation = self.cache.get_translation(text_hash)
        if cached_translation:
            return cached_translation

        # Translate if not in cache
        if self.settings.translator_provider == "DeepL":
            translation = self.deepl.translate_text(text, target_lang='EN-US').text
            # Add to cache
            self.cache.add_translation(text_hash, translation)
            return translation
        else:
            raise ValueError("Invalid provider")
