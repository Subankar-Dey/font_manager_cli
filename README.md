# 🔤 Windows Font Manager CLI

![OS](https://img.shields.io/badge/OS-Windows-blue?style=flat-square&logo=windows)
![Python](https://img.shields.io/badge/Python-3.6%2B-brightgreen?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

A sleek, interactive Command Line Interface (CLI) to easily manage, search, and swap your default Windows system font (Segoe UI). Built entirely in Python using `prompt_toolkit`.

---

## ✨ Key Features

- **⌨️ Interactive UI:** Navigate entirely via quick keyboard shortcuts.
- **🔍 Smart Search:** Instantly find and filter your installed system fonts.
- **🎨 Custom Themes:** Personalize your CLI with professional color palettes (Midnight Slate, Deep Dark, Nordic Frost, etc.).
- **↩️ Safe Restore:** 1-click option to instantly revert to default Windows settings.
- **💾 Persistent Config:** Automatically saves your visual preferences between sessions.

---

## ⚙️ Quick Start

Follow these short steps to get up and running:

**1. Clone the repository**
```bash
git clone https://github.com/Subankar-Dey/font_manager_cli.git
cd font_manager_cli
```

**2. Install requirements**
```bash
pip install -r requirements.txt
```

**3. Run the application** *(Must run terminal as Administrator)*
```bash
python font_manager.py
```

---

## 🎮 Navigation & Hotkeys

| Key | Action |
| :--- | :--- |
| `[S]` | Search fonts |
| `[B]` | Browse all fonts |
| `[T]` | Change UI Theme |
| `[R]` | Restore default fonts |
| `[E]` / `[Q]` | Exit application |
| `[Tab]` | Move to next item |
| `[Enter]` / `[O]` | Confirm / OK |
| `[C]` | Cancel / Back |

---

## ⚠️ Important Requirements

*   🛡️ **Administrator Privileges:** Modifying system fonts changes the Windows Registry. You *must* open your terminal/command prompt as an Administrator to apply changes.
*   🔄 **System Restart:** After applying a new font or restoring defaults, you must restart your computer for the changes to take effect across the entire OS.
