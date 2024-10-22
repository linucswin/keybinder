import dearpygui.dearpygui as dpg
import keyboard
import time
import os
import configparser
import pyperclip
import pygame
import webbrowser

pygame.mixer.init()

on_sound = pygame.mixer.Sound(os.path.join('assets/on.mp3'))
off_sound = pygame.mixer.Sound(os.path.join('assets/off.mp3'))
error_sound = pygame.mixer.Sound(os.path.join('assets/error.mp3'))
success_sound = pygame.mixer.Sound(os.path.join('assets/success.mp3'))

def play_success_sound():
    success_sound.play()

def play_error_sound():
    error_sound.play()

def play_on_sound():
    on_sound.play()

def play_off_sound():
    off_sound.play()

def save_config():
    config = configparser.ConfigParser()
    duplicate_hotkeys = set()

    for i in range(1, 11):
        key_value = str(dpg.get_value(f"line{i}_key"))
        command_value = str(dpg.get_value(f"line{i}_command"))

        if key_value in duplicate_hotkeys:
            print(f"Error: Duplicate hotkey '{key_value}' found in line {i}. Please use a unique key.")
            error_sound.play()
            return

        if key_value:
            duplicate_hotkeys.add(key_value)

        config[f"line{i}"] = {'key': key_value, 'command': command_value}
    
    config_folder = os.path.expanduser("~/Documents/linux keybinder")
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    config_file = os.path.join(config_folder, "config.ini")
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    success_sound.play()

def load_config():
    config_folder = os.path.expanduser("~/Documents/linux keybinder")
    config_file = os.path.join(config_folder, "config.ini")
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        for section_name in config.sections():
            line_config = config[section_name]
            dpg.set_value(section_name + "_key", line_config['key'])
            dpg.set_value(section_name + "_command", line_config['command'])
    else:
        print("cfg not found")

def perform_action(action):
    global script_enabled
    if not script_enabled:
        return
    
    keyboard.press_and_release('T')
    time.sleep(0.02) 
    pyperclip.copy(action)
    keyboard.press_and_release('ctrl+v')
    keyboard.press_and_release('enter')
    time.sleep(0.05)

def listen_hotkeys():
    for key in allowed_keys:
        keyboard.add_hotkey(key, hotkey_pressed, args=(key,))

def hotkey_pressed(key):
    if not script_enabled:
        return

    for i in range(1, 11):
        hotkey = str(dpg.get_value(f"line{i}_key"))
        command = str(dpg.get_value(f"line{i}_command"))

        if key == hotkey:
            perform_action(command)
            break

def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[36, 173, 149])
    with dpg.tooltip(t):
        dpg.add_text(message)

script_enabled = False

def toggle_script():
    global script_enabled
    script_enabled = not script_enabled
    if script_enabled:
        on_sound.play()
        dpg.set_value("checkbox_onoff", True)
    else:
        off_sound.play()
        dpg.set_value("checkbox_onoff", False)

def listen_hotkey_toggle_script():
    keyboard.add_hotkey('f2', toggle_script)

allowed_keys = ['Z', 'X', 'C', 'B', 'N', 'L', 'K', 'J', 'H', 'P', 'O', 'I', 'U', 'Y', 'Q']

dpg.create_context()
dpg.create_viewport(title="linux keybinder v2.6", width=575, height=420, small_icon='assets/icon2.ico', large_icon='assets/icon2.ico')
dpg.setup_dearpygui()
dpg.show_viewport()

with dpg.font_registry():
    custom_font = dpg.add_font("assets/font.ttf", 15)
dpg.bind_font(custom_font)
with dpg.window(tag="linux keybinder v2.6", no_resize=True):

    with dpg.menu_bar():
        dpg.add_spacer(width=470)
        with dpg.menu(label="settings"):
            dpg.add_menu_item(label="refresh cfg", callback=load_config)
            with dpg.menu(label="sounds"):
                dpg.add_menu_item(label="success", callback=play_success_sound)
                dpg.add_menu_item(label="error", callback=play_error_sound)
                dpg.add_menu_item(label="on", callback=play_on_sound)
                dpg.add_menu_item(label="off", callback=play_off_sound)
            with dpg.menu(label="info"):
                dpg.add_menu_item(label="F2 to turn it on / off", callback=play_success_sound)
            with dpg.menu(label="credits"):
                dpg.add_menu_item(label="discord -> linux1337")
                dpg.add_menu_item(label="instagram -> theqdqr")
                dpg.add_menu_item(label="github -> linucswin")
            with dpg.menu(label="support"):
                dpg.add_menu_item(label="discord server", callback=lambda: webbrowser.open('https://discord.gg/3JdQUDbuqx'))
                dpg.add_menu_item(label="github page", callback=lambda: webbrowser.open('https://github.com/linucswin/keybinder'))
    dpg.add_spacer(height=5)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=220)
        dpg.add_text("on", color=[36, 173, 149])
        dpg.add_checkbox(label="", default_value=False ,callback=toggle_script, tag="checkbox_onoff")
        dpg.add_text("off", color=[145, 32, 32])
    dpg.add_spacer(height=10)
    for i in range(1, 11):  
        with dpg.group(tag=f"line{i}", horizontal=True):
            combo_tag = f"line{i}_key"
            dpg.add_combo(allowed_keys, label="", default_value="", width=50, tag=combo_tag)
            dpg.add_input_text(label="", hint="exemplu: /c salut", default_value="", width=475, tag=f"line{i}_command")
            
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_spacer(width=180)
        dpg.add_button(label=">>> save config <<<", callback=save_config)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (23, 97, 84), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (36, 173, 149), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (36, 145, 125), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (36, 145, 125), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (101, 105, 103), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (23, 97, 84), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (36, 173, 149), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (36, 173, 149), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (23, 97, 84), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (36, 173, 149), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
dpg.bind_theme(global_theme)

load_config()
listen_hotkey_toggle_script()
listen_hotkeys() 

dpg.set_primary_window("linux keybinder v2.6", True)
dpg.start_dearpygui()
dpg.destroy_context()
# updated v2.6