import winreg
import sys
import os
import json
from prompt_toolkit.shortcuts import input_dialog, message_dialog, yes_no_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.containers import VSplit, HSplit, WindowAlign
from prompt_toolkit.widgets import Button, Dialog, Label, RadioList, TextArea, Frame
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

# --- Professional Themes Database ---
THEMES = {
    "Midnight Slate (Dark)": {
        'dialog': 'bg:#0f172a #e2e8f0',
        'dialog.body': 'bg:#0f172a #94a3b8',
        'dialog.border': '#334155',
        'frame.label': '#38bdf8 bold',
        'button': 'bg:#1e293b #f1f5f9',
        'button.focused': 'bg:#0ea5e9 #ffffff',
        'text-area': 'bg:#1e293b #f8fafc nounderline',
        'radiolist': '#94a3b8',
        'radiolist.current': '#0ea5e9 bold',
        'chat-frame': '#8ab4f8',
        'chat-input': 'bg:#131314 #e8eaed',
    },
    "Deep Dark": {
        'dialog': 'bg:#000000 #ffffff',
        'dialog.body': 'bg:#000000 #aaaaaa',
        'dialog.border': '#ffffff',
        'frame.label': '#ffffff bold',
        'button': 'bg:#222222 #ffffff',
        'button.focused': 'bg:#ffffff #000000',
        'text-area': 'bg:#111111 #ffffff nounderline',
        'radiolist': '#aaaaaa',
        'radiolist.current': '#ffffff bold',
        'chat-frame': '#8ab4f8',
        'chat-input': 'bg:#131314 #e8eaed',
    },
    "Nordic Frost": {
        'dialog': 'bg:#2e3440 #eceff4',
        'dialog.body': 'bg:#2e3440 #d8dee9',
        'dialog.border': '#4c566a',
        'frame.label': '#88c0d0 bold',
        'button': 'bg:#3b4252 #e5e9f0',
        'button.focused': 'bg:#81a1c1 #2e3440',
        'text-area': 'bg:#434c5e #eceff4 nounderline',
        'radiolist': '#d8dee9',
        'radiolist.current': '#8fbcbb bold',
        'chat-frame': '#88c0d0',
        'chat-input': 'bg:#2e3440 #eceff4',
    },
    "Arctic Snow (Light)": {
        'dialog': 'bg:#f8fafc #1e293b',
        'dialog.body': 'bg:#f8fafc #475569',
        'dialog.border': '#e2e8f0',
        'frame.label': '#0284c7 bold',
        'button': 'bg:#f1f5f9 #334155',
        'button.focused': 'bg:#0ea5e9 #ffffff',
        'text-area': 'bg:#ffffff #0f172a nounderline',
        'radiolist': '#475569',
        'radiolist.current': '#0284c7 bold',
        'chat-frame': '#0284c7',
        'chat-input': 'bg:#f1f5f9 #0f172a',
    },
    "Gruvbox Retro": {
        'dialog': 'bg:#282828 #ebdbb2',
        'dialog.body': 'bg:#282828 #a89984',
        'dialog.border': '#504945',
        'frame.label': '#fabd2f bold',
        'button': 'bg:#3c3836 #ebdbb2',
        'button.focused': 'bg:#b8bb26 #282828',
        'text-area': 'bg:#32302f #fbf1c7 nounderline',
        'radiolist': '#a89984',
        'radiolist.current': '#fe8019 bold',
        'chat-frame': '#fe8019',
        'chat-input': 'bg:#32302f #fbf1c7',
    },
    "Solarized Deep": {
        'dialog': 'bg:#002b36 #839496',
        'dialog.body': 'bg:#002b36 #586e75',
        'dialog.border': '#073642',
        'frame.label': '#268bd2 bold',
        'button': 'bg:#073642 #93a1a1',
        'button.focused': 'bg:#2aa198 #002b36',
        'text-area': 'bg:#001e26 #eee8d5 nounderline',
        'radiolist': '#586e75',
        'radiolist.current': '#859900 bold',
        'chat-frame': '#268bd2',
        'chat-input': 'bg:#001e26 #eee8d5',
    }
}

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "systemfont_pro_config.json")
APP_NAME = "FONT MANAGER"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"theme": "Midnight Slate (Dark)"}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception:
        pass

def get_current_style():
    config = load_config()
    theme_data = THEMES.get(config["theme"], THEMES["Midnight Slate (Dark)"])
    return Style.from_dict(theme_data)

# --- Registry Logic ---
def get_font_database():
    db = {}
    key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            i = 0
            while True:
                try:
                    reg_name, _, _ = winreg.EnumValue(key, i)
                    clean_name = reg_name.split(" (")[0] if " (" in reg_name else reg_name
                    parts = clean_name.split(' ')
                    family = parts[0]
                    prefixes = ["Microsoft", "Segoe", "Times", "Courier", "Lucida", "Century", "Comic", "Franklin", "Book", "Bodoni"]
                    if len(parts) > 1 and parts[0] in prefixes:
                        family = parts[0] + " " + parts[1]
                    if family not in db:
                        db[family] = []
                    if clean_name not in db[family]:
                        db[family].append(clean_name)
                    i += 1
                except OSError:
                    break
    except Exception:
        pass
    return {fam: sorted(db[fam]) for fam in sorted(db.keys())}

def set_system_font(font_name):
    fonts_key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    sub_key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
    segoe_fonts = [
        "Segoe UI (TrueType)", "Segoe UI Bold (TrueType)", "Segoe UI Italic (TrueType)",
        "Segoe UI Bold Italic (TrueType)", "Segoe UI Semibold (TrueType)",
        "Segoe UI Light (TrueType)", "Segoe UI Semilight (TrueType)", "Segoe UI Black (TrueType)"
    ]
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, fonts_key_path, 0, winreg.KEY_SET_VALUE) as key:
            for f in segoe_fonts:
                try:
                    winreg.SetValueEx(key, f, 0, winreg.REG_SZ, "")
                except FileNotFoundError:
                    pass
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, font_name)
        message_dialog(
            title=f"{APP_NAME}",
            text=f"Success! Set to {font_name}.\nRestart Windows to apply.",
            style=get_current_style()
        ).run()
    except PermissionError:
        message_dialog(
            title=f"{APP_NAME}",
            text="Admin privileges required.",
            style=get_current_style()
        ).run()
    except Exception as e:
        message_dialog(
            title=f"{APP_NAME}",
            text=str(e),
            style=get_current_style()
        ).run()

def restore_defaults():
    fonts_key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    sub_key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
    defaults = {
        "Segoe UI (TrueType)": "segoeui.ttf", "Segoe UI Bold (TrueType)": "segoeuib.ttf",
        "Segoe UI Italic (TrueType)": "segoeuii.ttf", "Segoe UI Bold Italic (TrueType)": "segoeuiz.ttf",
        "Segoe UI Semibold (TrueType)": "seguisb.ttf", "Segoe UI Light (TrueType)": "segoeuil.ttf",
        "Segoe UI Semilight (TrueType)": "segoeuisl.ttf", "Segoe UI Black (TrueType)": "seguibl.ttf"
    }
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, fonts_key_path, 0, winreg.KEY_SET_VALUE) as key:
            for f, v in defaults.items():
                winreg.SetValueEx(key, f, 0, winreg.REG_SZ, v)
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key_path, 0, winreg.KEY_SET_VALUE) as key:
            try:
                winreg.DeleteValue(key, "Segoe UI")
            except FileNotFoundError:
                pass
        message_dialog(
            title=f"{APP_NAME}",
            text="Default Segoe UI restored. Please restart PC.",
            style=get_current_style()
        ).run()
    except Exception as e:
        message_dialog(
            title=f"{APP_NAME}",
            text=str(e),
            style=get_current_style()
        ).run()

# --- Universal Hotkey Logic ---
def create_hotkey_bindings(btn_ok=None, btn_cancel=None, btn_yes=None, btn_no=None, radio_list=None):
    kb = KeyBindings()
    @kb.add('o')
    @kb.add('O')
    def _(event):
        if btn_ok:
            event.app.layout.focus(btn_ok)

    @kb.add('c')
    @kb.add('C')
    def _(event):
        if btn_cancel:
            event.app.layout.focus(btn_cancel)

    @kb.add('y')
    @kb.add('Y')
    def _(event):
        if btn_yes:
            event.app.layout.focus(btn_yes)

    @kb.add('n')
    @kb.add('N')
    def _(event):
        if btn_no:
            event.app.layout.focus(btn_no)

    if radio_list:
        @kb.add('<any>')
        def _(event):
            key = event.data.lower()
            if len(key) == 1 and 'a' <= key <= 'z':
                for idx, (val, label) in enumerate(radio_list.values):
                    if str(label).lower().startswith(key):
                        radio_list._selected_index = idx
                        break

    @kb.add('tab')
    def _(event):
        focus_next(event)

    @kb.add('s-tab')
    def _(event):
        focus_previous(event)

    return kb

# --- UI Engines ---
def run_home_app():
    result = {"action": None}
    def set_action(action):
        result["action"] = action
        app.exit()

    btn_search = Button(text="Search", handler=lambda: set_action("search"))
    btn_browse = Button(text="Browse", handler=lambda: set_action("browse"))
    btn_theme = Button(text="Themes", handler=lambda: set_action("theme"))
    btn_restore = Button(text="Restore", handler=lambda: set_action("restore"))
    btn_exit = Button(text="Exit", handler=lambda: set_action("exit"))

    kb = KeyBindings()
    @kb.add('s')
    @kb.add('S')
    def _(event):
        event.app.layout.focus(btn_search)

    @kb.add('b')
    @kb.add('B')
    def _(event):
        event.app.layout.focus(btn_browse)

    @kb.add('t')
    @kb.add('T')
    def _(event):
        event.app.layout.focus(btn_theme)

    @kb.add('r')
    @kb.add('R')
    def _(event):
        event.app.layout.focus(btn_restore)

    @kb.add('e')
    @kb.add('E')
    def _(event):
        event.app.layout.focus(btn_exit)

    @kb.add('tab')
    def _(event):
        focus_next(event)

    @kb.add('s-tab')
    def _(event):
        focus_previous(event)

    @kb.add('q')
    def _(event):
        app.exit()

    dialog_body = HSplit([
        Label(
            text="Windows System Font Orchestrator\n--------------------------------\nHotkeys: [S]earch, [B]rowse, [T]hemes, [R]estore, [E]xit",
            align=WindowAlign.CENTER
        ),
        VSplit([btn_search, btn_browse, btn_theme, btn_restore, btn_exit], padding=1, align=WindowAlign.CENTER),
    ], padding=1)

    dialog = Dialog(title=APP_NAME, body=dialog_body, with_background=True)
    app = Application(
        layout=Layout(dialog),
        key_bindings=kb,
        style=get_current_style(),
        full_screen=True,
        mouse_support=True
    )
    app.run()
    return result["action"]

def custom_radiolist_dialog(title, text, values):
    result = {"value": None}
    radio_list = RadioList(values)
    def ok_handler():
        result["value"] = radio_list.current_value
        app.exit()
    btn_ok = Button(text="OK", handler=ok_handler)
    btn_cancel = Button(text="Cancel", handler=lambda: app.exit())
    kb = create_hotkey_bindings(btn_ok=btn_ok, btn_cancel=btn_cancel, radio_list=radio_list)
    dialog = Dialog(
        title=title,
        body=HSplit([Label(text=text), radio_list], padding=1),
        buttons=[btn_ok, btn_cancel],
        with_background=True
    )
    app = Application(
        layout=Layout(dialog),
        key_bindings=kb,
        style=get_current_style(),
        full_screen=True,
        mouse_support=True
    )
    app.run()
    return result["value"]

def main():
    db = get_font_database()
    while True:
        choice = run_home_app()
        if choice == "exit" or choice is None:
            break
        
        current_style = get_current_style()

        if choice == "theme":
            config = load_config()
            new_theme = custom_radiolist_dialog(
                title=f"{APP_NAME} - Visual Themes",
                text="Choose a professional color scheme (Press first letter to jump):",
                values=[(t, t) for t in THEMES.keys()]
            )
            if new_theme:
                config["theme"] = new_theme
                save_config(config)
            continue

        if choice == "restore":
            if yes_no_dialog(title=f"{APP_NAME}", text="Restore default font?", style=current_style).run():
                restore_defaults()
            continue

        families = list(db.keys())
        title_suffix = "Repository"
        if choice == "search":
            query = input_dialog(
                title=f"{APP_NAME} - Search",
                text="Enter font name or letter:",
                style=current_style
            ).run()
            if not query:
                continue
            starts_with = [f for f in families if f.lower().startswith(query.lower())]
            contains = [f for f in families if query.lower() in f.lower() and not f.lower().startswith(query.lower())]
            families = starts_with + contains
            if not families:
                message_dialog(
                    title=f"{APP_NAME}",
                    text=f"No fonts found matching '{query}'.",
                    style=current_style
                ).run()
                continue
            title_suffix = f"Search: '{query}'"

        selected_fam = custom_radiolist_dialog(
            title=f"{APP_NAME} - {title_suffix}",
            text="Select a family (Press letter to jump, 'o' for OK, 'c' for Cancel):",
            values=[(f, f) for f in families]
        )
        if selected_fam:
            target_font = custom_radiolist_dialog(
                title=f"{APP_NAME} - {selected_fam}",
                text="Select variation:",
                values=[(v, v) for v in db[selected_fam]]
            )
            if target_font:
                if yes_no_dialog(
                    title=f"{APP_NAME}",
                    text=f"Apply '{target_font}'?\nRequires restart.",
                    style=current_style
                ).run():
                    set_system_font(target_font)
                    break

if __name__ == "__main__":
    main()