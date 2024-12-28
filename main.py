import dearpygui.dearpygui as dpg
from src.theme import create_theme
from src.ui import create_main_window, cleanup

def main():
    dpg.create_context()
    dpg.create_viewport(title="EraClip", width=600, height=400, resizable=True)
    dpg.setup_dearpygui()

    create_main_window()
    
    theme = create_theme()
    dpg.bind_theme(theme)
    dpg.set_primary_window("main", True)

    dpg.show_viewport()
    
    try:
        dpg.start_dearpygui()
    finally:
        cleanup()
        dpg.destroy_context()

if __name__ == "__main__":
    main()
