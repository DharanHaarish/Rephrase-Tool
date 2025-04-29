# Rephrase Tool

A desktop automation tool to quickly rephrase selected text (Casual, Formal, Humorous) using Google Gemini LLM. Works globally with a hotkey and provides a simple popup UI and system tray control.

---

## Features
- Select and copy text anywhere (email, browser, chat, etc.)
- Press `Ctrl+Alt+Shift+R` to open a popup and choose a rephrase style
- Get the rephrased text in a new popup with copy and close options
- System tray icon to pause/resume or exit the tool

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/DharanHaarish/Rephrase-Tool.git
cd Rephrase-Tool
```

### 2. Create and Activate a Virtual Environment (Recommended)
```sh
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```sh
pip install google-generativeai pyperclip keyboard pystray pillow
```

### 4. Get Your Gemini API Key
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create an API key (free tier available)
- **Copy your API key**

### 5. Add Your API Key
- Open `hotkey_copy_test.py`
- Replace the placeholder in this line:
  ```python
  GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
  ```
  with your actual Gemini API key.

### 6. Run the Tool
- Double-click `run_rephrase_tool.bat` (recommended, uses your venv)
- Or, run from terminal:
  ```sh
  python hotkey_copy_test.py
  ```

---

## Usage
1. **Select and copy** any text (Ctrl+C or right-click → Copy)
2. **Press `Ctrl+Alt+Shift+R`**
3. **Choose a style** (Casual, Formal, Humorous) in the popup
4. **Get the rephrased text** in a new popup (copy or close)
5. Use the tray icon to pause/resume or exit the tool

---

## Troubleshooting
- If the hotkey doesn't work, make sure you have copied some text first.
- If you see errors about missing modules, re-run the pip install command.
- If you get API errors, check your Gemini API key and quota.

---

## Contributing
Pull requests and suggestions are welcome! Open an issue or submit a PR on [GitHub](https://github.com/DharanHaarish/Rephrase-Tool).
