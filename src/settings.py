import json
import os
from pathlib import Path

class Settings:
    _instance = None
    SETTINGS_FILE = "eraclip.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._init_defaults()
            cls._instance.load_settings()
        return cls._instance

    def _init_defaults(self):
        # Variable singleton 
        self.first_toggle = True

        # Parser settings
        self.japanese_enabled = True
        self.chinese_enabled = True
        self.korean_enabled = True
        self.confidence_threshold = 0.85
        self.max_characters = 350
        
        # Translator settings
        self.translator_provider = "DeepL"
        self.translator_api_key = None

    def _get_settings_path(self):
        return Path(os.path.dirname(__file__)).parent / self.SETTINGS_FILE

    def to_dict(self):
        return {
            "parser": {
                "japanese_enabled": self.japanese_enabled,
                "chinese_enabled": self.chinese_enabled,
                "korean_enabled": self.korean_enabled,
                "confidence_threshold": self.confidence_threshold,
                "max_characters": self.max_characters
            },
            "translator": {
                "provider": self.translator_provider,
                "api_key": self.translator_api_key
            }
        }

    def from_dict(self, data):
        if "parser" in data:
            parser = data["parser"]
            self.japanese_enabled = parser.get("japanese_enabled", self.japanese_enabled)
            self.chinese_enabled = parser.get("chinese_enabled", self.chinese_enabled)
            self.korean_enabled = parser.get("korean_enabled", self.korean_enabled)
            self.confidence_threshold = parser.get("confidence_threshold", self.confidence_threshold)
            self.max_characters = parser.get("max_characters", self.max_characters)

        if "translator" in data:
            translator = data["translator"]
            self.translator_provider = translator.get("provider", self.translator_provider)
            self.translator_api_key = translator.get("api_key", self.translator_api_key)

    def save_settings(self):
        try:
            with open(self._get_settings_path(), 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def load_settings(self):
        try:
            settings_path = self._get_settings_path()
            if settings_path.exists():
                with open(settings_path, 'r', encoding='utf-8') as f:
                    self.from_dict(json.load(f))
        except Exception as e:
            print(f"Failed to load settings: {e}")

    def update_parser_settings(self, ja=None, zh=None, ko=None, confidence=None, max_chars=None):
        if ja is not None:
            self.japanese_enabled = ja
        if zh is not None:
            self.chinese_enabled = zh
        if ko is not None:
            self.korean_enabled = ko
        if confidence is not None:
            self.confidence_threshold = confidence
        if max_chars is not None:
            self.max_characters = max_chars
        self.save_settings()  # Auto-save after updates

    def update_translator_settings(self, provider=None, api_key=None):
        if provider is not None:
            self.translator_provider = provider
        if api_key is not None:
            self.translator_api_key = api_key
        self.save_settings()  # Auto-save after updates
