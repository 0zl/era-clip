class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._init_defaults()
        return cls._instance

    def _init_defaults(self):
        # Parser settings
        self.japanese_enabled = True
        self.chinese_enabled = True
        self.korean_enabled = True
        self.confidence_threshold = 0.85
        self.max_characters = 350
        
        # Translator settings
        self.translator_provider = "Google Translate"
        self.translator_api_key = None

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

    def update_translator_settings(self, provider=None, api_key=None):
        if provider is not None:
            self.translator_provider = provider
        if api_key is not None:
            self.translator_api_key = api_key
