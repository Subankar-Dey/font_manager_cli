# Font Manager CLI

A powerful, interactive Command Line Interface (CLI) utility built with Python that allows you to easily manage, search, and swap your Windows system fonts. It specifically targets and replaces the default "Segoe UI" font across the Windows operating system by safely modifying the registry.

## ✨ Features

- **Interactive UI:** A rich, keyboard-navigable terminal interface built with `prompt_toolkit`.
- **Search & Browse:** Quickly search through all installed fonts on your system or browse them via a categorized list.
- **Custom Themes:** Choose from several professional color schemes (e.g., Midnight Slate, Deep Dark, Nordic Frost, Gruvbox Retro) to personalize your CLI experience.
- **Safe Restoration:** A built-in 1-click option to restore the default Windows Segoe UI font settings.
- **Persistent Configuration:** Remembers your visual theme preferences between sessions.

## 🚀 Prerequisites

- **OS:** Windows (The script relies on the Windows Registry via the `winreg` module).
- **Python:** Python 3.6 or higher.
- **Dependencies:** The `prompt_toolkit` library is required for the interactive UI.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Subankar-Dey/font_manager_cli.git
   cd font_manager_cli
   ```

2. **Install the required dependencies:**
   ```bash
   pip install prompt_toolkit
   ```

## 💻 Usage

Run the script using Python:

```bash
python font_manager.py
```

### Hotkeys & Navigation
- **[S]** - Search for a specific font
- **[B]** - Browse the complete font repository
- **[T]** - Open Visual Themes menu
- **[R]** - Restore default Windows fonts
- **[E]** or **[Q]** - Exit the application
- **[Tab] / [Shift-Tab]** - Navigate between buttons and inputs
- **[Enter]** or **[O]** - Confirm selection
- **[C]** - Cancel/Go Back

## ⚠️ Important Notes

1. **Administrator Privileges:** Modifying system fonts requires altering the Windows Registry. Ensure you are running your terminal/command prompt as an **Administrator**.
2. **System Restart:** After applying a new font or restoring the default font, you **must restart your computer** for the changes to take effect across the entire operating system.

## 📄 License

This project is open-source and available under the MIT License.
