import dearpygui.dearpygui as dpg
from .window_utils import set_always_top, set_window_transparency
from .translator import Translator
from .clipboard_monitor import ClipboardMonitor

translator = Translator()
clipboard_monitor = None

def on_clipboard_change(content: str):
    # print the original first, then translated text.
    translated_text = translator.translate(content)
    dpg.set_value("translation_output", translated_text)

def on_provider_change(sender, value):
    dpg.configure_item("deepl_api_container", show=(value == "DeepL"))
    translator.set_provider(value)

def on_api_key_change(sender, value):
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

def create_main_window():
    global clipboard_monitor
    
    create_button_themes()
    clipboard_monitor = ClipboardMonitor(on_clipboard_change)

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
                            default_value="Google Translate",
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
                    
                    with dpg.child_window(height=125, border=True, width=-1):
                        dpg.add_text("Parser Settings", color=(200, 200, 200))
                        dpg.add_checkbox(label="Japanese", default_value=True, tag="japanese_parser")
                        dpg.add_checkbox(label="Chinese", default_value=True, tag="chinese_parser")
                        dpg.add_checkbox(label="Korean", default_value=True, tag="korean_parser")
                        dpg.add_slider_float(
                            label="Confidence Parser",
                            default_value=0.85,
                            min_value=0.1,
                            max_value=1.0,
                            tag="confidence_parser"
                        )

            with dpg.tab(label="About"):
                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_text("EraClip", color=(200, 200, 200))
                        dpg.add_text("A real-time translator for playing untranslated Era games.")
                        dpg.add_spacer(height=5)
                        dpg.add_text("Thanks: /hgg, /egg")
                        dpg.add_spacer(height=5)
                        dpg.add_text("https://github.com/0zl/era-clip")

    dpg.bind_item_theme("toggle_button", "stopped_theme")

def cleanup():
    if clipboard_monitor:
        clipboard_monitor.stop()
