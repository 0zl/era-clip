import os
import sys
from pathlib import Path
import hashlib

class TranslationCache:
    _instance = None
    CACHE_FILE = "eraclip.tl"
    SEPARATOR = "<ERACLIP_SEP>"
    FIELD_SEPARATOR = "|"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranslationCache, cls).__new__(cls)
            cls._instance.cache = {}
            cls._instance.load_cache()
        return cls._instance

    def _get_cache_path(self):
        return Path(os.path.join(os.path.dirname(sys.argv[0]), self.CACHE_FILE))

    def load_cache(self):
        try:
            cache_path = self._get_cache_path()
            if cache_path.exists():
                with open(cache_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split(self.FIELD_SEPARATOR, 1)
                            if len(parts) == 2:
                                hash_key = parts[0]
                                translation = parts[1].removesuffix(self.SEPARATOR)
                                self.cache[hash_key] = translation
        except Exception as e:
            print(f"Failed to load translation cache: {e}")

    def save_cache(self):
        try:
            with open(self._get_cache_path(), 'w', encoding='utf-8') as f:
                for hash_key, translation in self.cache.items():
                    # Remove any newlines from translation and create single line entry
                    clean_translation = translation.replace('\n', ' ').strip()
                    f.write(f"{hash_key}{self.FIELD_SEPARATOR}{clean_translation}{self.SEPARATOR}\n")
        except Exception as e:
            print(f"Failed to save translation cache: {e}")

    def get_hash(self, text: str) -> str:
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def get_translation(self, text_hash: str) -> str | None:
        return self.cache.get(text_hash)

    def add_translation(self, text_hash: str, translation: str):
        self.cache[text_hash] = translation
        self.save_cache()
