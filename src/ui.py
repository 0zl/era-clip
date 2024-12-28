import dearpygui.dearpygui as dpg
from .window_utils import set_always_top, set_window_transparency
from .translator import Translator
from .clipboard_monitor import ClipboardMonitor
from .parser import LanguageDetector
from .settings import Settings

translator = Translator()
clipboard_monitor = None
settings = Settings()

def on_clipboard_change(content: str):
    lang_score = language_detector.detect_multiple_languages(content)
    lang_id, highest_score = max(lang_score.items(), key=lambda x: x[1])
    print(f"Detected language: {lang_id} with confidence: {highest_score}")

    translated_text = translator.translate(content)
    dpg.set_value("translation_output", translated_text)

def on_provider_change(sender, value):
    dpg.configure_item("deepl_api_container", show=(value == "DeepL"))
    settings.update_translator_settings(provider=value)
    translator.set_provider(value)

def on_api_key_change(sender, value):
    settings.update_translator_settings(api_key=value)
    translator.set_api_key(value)

def on_always_on_top(sender, value):
    set_always_top(value)

def on_transparency_change(sender, value):
    set_window_transparency(value)

def toggle_translator(sender, value):
    if clipboard_monitor.is_running:
        clipboard_monitor.stop()
        dpg.configure_item("toggle_button", label="Start Translator")
        dpg.bind_item_theme("toggle_button", "stopped_theme")
    else:
        clipboard_monitor.start()
        dpg.configure_item("toggle_button", label="Stop Translator")
        dpg.bind_item_theme("toggle_button", "running_theme")

def create_button_themes():
    # Theme for running state
    with dpg.theme(tag="running_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (35, 134, 54))        # Green
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (46, 160, 67))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (28, 110, 44))
    
    # Theme for stopped state
    with dpg.theme(tag="stopped_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (164, 14, 38))       # Red
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (185, 24, 49))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (139, 14, 35))

def on_parser_setting_change(sender, value):
    if sender == "japanese_parser":
        settings.update_parser_settings(ja=value)
    elif sender == "chinese_parser":
        settings.update_parser_settings(zh=value)
    elif sender == "korean_parser":
        settings.update_parser_settings(ko=value)
    elif sender == "confidence_parser":
        settings.update_parser_settings(confidence=value)
    elif sender == "max_chars_parser":
        settings.update_parser_settings(max_chars=value)

def create_main_window():
    global clipboard_monitor
    global language_detector
    
    create_button_themes()
    clipboard_monitor = ClipboardMonitor(on_clipboard_change)
    language_detector = LanguageDetector()

    with dpg.window(label="Main Window", tag="main"):
        with dpg.tab_bar(tag="tab_bar", reorderable=False):
            with dpg.tab(label="Translator"):
                with dpg.group():
                    with dpg.child_window(border=True, width=-1, height=-25):
                        dpg.add_text(
                            default_value="Translation results will appear here...",
                            wrap=0,
                            tag="translation_output"
                        )
                    with dpg.child_window(border=False, width=-1, height=-1):
                        dpg.add_button(
                            label="Start Translator",
                            callback=toggle_translator,
                            tag="toggle_button",
                            width=-1
                        )
                
            with dpg.tab(label="Settings"):
                with dpg.group():
                    with dpg.child_window(height=55, border=True, width=-1):
                        dpg.add_text("Provider", color=(200, 200, 200))
                        dpg.add_radio_button(
                            items=["Google Translate", "DeepL"],
                            default_value=settings.translator_provider,
                            horizontal=True,
                            tag="provider_radio",
                            callback=on_provider_change
                        )
                    
                    with dpg.child_window(height=55, border=True, width=-1, show=False, tag="deepl_api_container"):
                        dpg.add_text("DeepL API Key", color=(200, 200, 200))
                        dpg.add_input_text(
                            width=-1,
                            password=True,
                            tag="deepl_api_key",
                            default_value=settings.translator_api_key or "",
                            callback=on_api_key_change
                        )
                    
                    with dpg.child_window(height=80, border=True, width=-1):
                        dpg.add_text("Window Settings", color=(200, 200, 200))
                        dpg.add_checkbox(
                            label="Always On Top",
                            callback=on_always_on_top,
                            tag="always_on_top"
                        )
                        dpg.add_slider_float(
                            label="Transparency",
                            default_value=1.0,
                            min_value=0.3,
                            max_value=1.0,
                            callback=on_transparency_change,
                            tag="transparency_slider"
                        )
                    
                    with dpg.child_window(height=150, border=True, width=-1):
                        dpg.add_text("Parser Settings", color=(200, 200, 200))
                        dpg.add_checkbox(
                            label="Japanese",
                            default_value=settings.japanese_enabled,
                            callback=on_parser_setting_change,
                            tag="japanese_parser"
                        )
                        dpg.add_checkbox(
                            label="Chinese",
                            default_value=settings.chinese_enabled,
                            callback=on_parser_setting_change,
                            tag="chinese_parser"
                        )
                        dpg.add_checkbox(
                            label="Korean",
                            default_value=settings.korean_enabled,
                            callback=on_parser_setting_change,
                            tag="korean_parser"
                        )
                        dpg.add_slider_float(
                            label="Confidence Parser",
                            default_value=settings.confidence_threshold,
                            min_value=0.1,
                            max_value=1.0,
                            callback=on_parser_setting_change,
                            tag="confidence_parser"
                        )
                        dpg.add_slider_int(
                            label="Max Characters",
                            default_value=settings.max_characters,
                            min_value=0,
                            max_value=1000,
                            callback=on_parser_setting_change,
                            tag="max_chars_parser"
                        )

            with dpg.tab(label="About"):
                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_text("EraClip", color=(200, 200, 200))
                        dpg.add_text("A real-time translator for playing untranslated Era games.")
                        dpg.add_spacer(height=5)
                        dpg.add_text("Thanks: /hgg/, /egg/")
                        dpg.add_spacer(height=5)
                        dpg.add_text("https://github.com/0zl/era-clip")

    dpg.bind_item_theme("toggle_button", "stopped_theme")

def cleanup():
    if clipboard_monitor:
        clipboard_monitor.stop()
