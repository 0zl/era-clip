import unicodedata
import re
from typing import Dict, List, Tuple, Optional

class LanguageRanges:
    # Specific Japanese-only characters
    JAPANESE_EXCLUSIVE = [
        (0x3040, 0x309F),  # Hiragana
        (0x30A0, 0x30FF),  # Katakana
        (0x31F0, 0x31FF),  # Katakana Phonetic Extensions
        (0x1B000, 0x1B0FF),  # Kana Extended-A
        (0xFF65, 0xFF9F),  # Half-width katakana
    ]
    
    # Specific Chinese-only characters
    CHINESE_EXCLUSIVE = [
        (0x3100, 0x312F),   # Bopomofo
        (0x31A0, 0x31BF),   # Bopomofo Extended
        (0x2E80, 0x2EFF),   # CJK Radicals Supplement
        (0x2F00, 0x2FDF),   # Kangxi Radicals
    ]
    
    # Shared CJK characters
    SHARED_CJK = [
        (0x4E00, 0x9FFF),   # CJK Unified Ideographs
        (0x3400, 0x4DBF),   # CJK Unified Ideographs Extension A
        (0x20000, 0x2A6DF), # CJK Unified Ideographs Extension B
        (0x2A700, 0x2B73F), # CJK Unified Ideographs Extension C
        (0x2B740, 0x2B81F), # CJK Unified Ideographs Extension D
        (0x2B820, 0x2CEAF), # CJK Unified Ideographs Extension E
        (0x2CEB0, 0x2EBEF), # CJK Unified Ideographs Extension F
        (0x30000, 0x3134F), # CJK Unified Ideographs Extension G
        (0x31C0, 0x31EF),   # CJK Strokes
        (0xF900, 0xFAFF),   # CJK Compatibility Ideographs
        (0x2F800, 0x2FA1F), # CJK Compatibility Ideographs Supplement
        (0x3000, 0x303F),   # CJK Symbols and Punctuation
        (0xFE30, 0xFE4F),   # CJK Compatibility Forms
        (0xFF00, 0xFFEF),   # Halfwidth and Fullwidth Forms
    ]
    
    # Combine ranges for each language
    JAPANESE = JAPANESE_EXCLUSIVE + SHARED_CJK
    CHINESE = CHINESE_EXCLUSIVE + SHARED_CJK
    KOREAN = [
        (0xAC00, 0xD7AF),  # Hangul syllables
        (0x1100, 0x11FF),  # Hangul Jamo
        (0x3130, 0x318F),  # Hangul Compatibility Jamo
        (0xA960, 0xA97F),  # Hangul Jamo Extended-A
        (0xD7B0, 0xD7FF),  # Hangul Jamo Extended-B
        (0xFFA1, 0xFFDC),  # Half-width Hangul
    ]

class LanguageDetector:
    def __init__(self, threshold: float = 15.0):
        self.threshold = threshold
        self.language_ranges = {
            'ja': LanguageRanges.JAPANESE,
            'ko': LanguageRanges.KOREAN,
            'zh': LanguageRanges.CHINESE,
        }
        self.exclusive_ranges = {
            'ja': LanguageRanges.JAPANESE_EXCLUSIVE,
            'zh': LanguageRanges.CHINESE_EXCLUSIVE,
        }
    
    def clean_repeated_chars(self, text: str, max_repeats: int = 2) -> str:
        if not text:
            return text
            
        # Common divider characters
        divider_chars = {'-', '=', '_', '~', '•', '−', '─', '━', '।', '᱾', '⸻', '—'}
        
        result = []
        prev_char = ''
        repeat_count = 0
        
        for char in text:
            if char == prev_char:
                repeat_count += 1
                # For divider characters, only keep one instance
                if char in divider_chars:
                    continue
                # For other characters, keep up to max_repeats
                if repeat_count >= max_repeats:
                    continue
            else:
                repeat_count = 0
            
            result.append(char)
            prev_char = char
            
        return ''.join(result)

    def clean_text(self, text: str) -> str:
        text = unicodedata.normalize('NFKC', text)
        text = self.clean_repeated_chars(text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def is_language_character(self, char: str, language: str) -> bool:
        if language not in self.language_ranges:
            raise ValueError(f"Unsupported language: {language}")
            
        char_ord = ord(char)
        return any(start <= char_ord <= end 
                  for start, end in self.language_ranges[language])
    
    def get_script_details(self, text: str) -> Dict[str, float]:
        total_chars = len(text.replace(' ', ''))
        if total_chars == 0:
            return {}
        
        counts = {
            'hiragana': sum(1 for c in text if 0x3040 <= ord(c) <= 0x309F),
            'katakana': sum(1 for c in text if 0x30A0 <= ord(c) <= 0x30FF),
            'kanji': sum(1 for c in text if 0x4E00 <= ord(c) <= 0x9FFF),
            'bopomofo': sum(1 for c in text if 0x3100 <= ord(c) <= 0x312F),
        }
        
        return {k: (v / total_chars) * 100 for k, v in counts.items()}

    def detect_language(self, text: str, language: str) -> Tuple[bool, float]:
        if not text or language not in self.language_ranges:
            return False, 0.0
        
        text = self.clean_text(text)
        if not text:
            return False, 0.0
        
        total_chars = len(text.replace(' ', ''))
        target_chars = sum(1 for c in text 
                         if self.is_language_character(c, language))
        
        if total_chars == 0:
            return False, 0.0
        
        base_score = (target_chars / total_chars) * 100
        
        if language in ['ja', 'zh']:
            script_details = self.get_script_details(text)
            
            if language == 'ja':
                if script_details.get('hiragana', 0) > 0 or script_details.get('katakana', 0) > 0:
                    base_score *= 1.2
                elif script_details.get('kanji', 0) > 0:
                    base_score *= 0.8
            
            elif language == 'zh':
                if script_details.get('bopomofo', 0) > 0:
                    base_score *= 1.2
                if script_details.get('hiragana', 0) > 0 or script_details.get('katakana', 0) > 0:
                    base_score *= 0.5
        
        return base_score >= self.threshold, min(base_score, 100.0)
    
    def detect_multiple_languages(self, text: str) -> Dict[str, float]:
        results = {}
        for lang in self.language_ranges.keys():
            _, confidence = self.detect_language(text, lang)
            results[lang] = confidence
        return results
