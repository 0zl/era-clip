import dearpygui.dearpygui as dpg

def create_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            # Window styling
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (22, 27, 34))         # Dark blue-grey background
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (36, 41, 51))    # Slightly lighter for active title
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (30, 35, 44))          # Title background
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 1)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 6, 6)
            
            # Tab styling
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (36, 41, 51))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (48, 54, 65))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (41, 47, 58))
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_TabBorderSize, 0)
            
            # Frame styling
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 3)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 6, 4)
            
            # Child window styling
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (26, 31, 38))          # Slightly lighter than window bg
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1)
            
            # Scrollbar styling
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (26, 31, 38))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (48, 54, 65))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (55, 62, 74))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (62, 70, 84))
            
            # Text colors
            dpg.add_theme_color(dpg.mvThemeCol_Text, (201, 209, 217))          # Light grey text
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (128, 135, 142))
            
            # Border colors
            dpg.add_theme_color(dpg.mvThemeCol_Border, (48, 54, 65))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
    
    return global_theme
