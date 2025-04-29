import keyboard
import pyperclip
import time
import tkinter as tk
import threading
import sys
from PIL import Image, ImageDraw
import pystray
import google.generativeai as genai
import queue

# --- Gemini API Setup ---
GEMINI_API_KEY = "AIzaSyCewoBcQnfBLIPZALL-ezqV_pnPovNEPZY"  # <-- Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Global state for pause/play
listening = True
hotkey = 'ctrl+alt+shift+r'

# Prompt templates for each style
def get_prompt(style, text):
    if style == "Casual":
        return (
            f"Rephrase the following text in a casual tone. "
            f"Return only the rephrased text, with no explanations or alternatives:\n{text}"
        )
    elif style == "Formal":
        return (
            f"Rephrase the following text in a formal tone. "
            f"Return only the rephrased text, with no explanations or alternatives:\n{text}"
        )
    elif style == "Humorous":
        return (
            f"Rephrase the following text in a humorous way. "
            f"Return only the rephrased text, with no explanations or alternatives:\n{text}"
        )
    else:
        return text

# Function to show a loading popup
def show_loading_popup():
    popup = tk.Tk()
    popup.overrideredirect(True)
    popup.geometry("250x80")
    popup.attributes('-topmost', True)
    label = tk.Label(popup, text="Rephrasing, please wait...", font=("Arial", 12))
    label.pack(expand=True, fill='both', pady=20)
    popup.update()
    return popup

# Function to show the popup with rephrase options
def show_popup(original_text):
    def on_option(style):
        print(f"Selected style: {style}")
        print(f"Copied text: {original_text}")
        popup.destroy()
        # Show loading popup
        loading_popup = show_loading_popup()
        result_queue = queue.Queue()

        # Run Gemini call in a thread to avoid blocking UI
        def get_rephrased():
            try:
                prompt = get_prompt(style, original_text)
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)
                rephrased = response.text.strip()
            except Exception as e:
                rephrased = f"[Error: {e}]"
            result_queue.put(rephrased)
        threading.Thread(target=get_rephrased, daemon=True).start()

        def check_queue():
            try:
                rephrased = result_queue.get_nowait()
                loading_popup.destroy()
                show_rephrased_popup(rephrased)
            except queue.Empty:
                loading_popup.after(100, check_queue)

        check_queue()

    def on_close():
        print("Popup closed")
        popup.destroy()

    popup = tk.Tk()
    popup.title("Rephrase Options")
    popup.geometry("250x180")
    popup.resizable(False, False)
    popup.protocol("WM_DELETE_WINDOW", on_close)
    popup.attributes('-topmost', True)  # Bring to front

    label = tk.Label(popup, text="Choose a rephrase style:")
    label.pack(pady=12)

    btn_casual = tk.Button(popup, text="Casual", width=20, command=lambda: on_option("Casual"))
    btn_casual.pack(pady=5)
    btn_formal = tk.Button(popup, text="Formal", width=20, command=lambda: on_option("Formal"))
    btn_formal.pack(pady=5)
    btn_humorous = tk.Button(popup, text="Humorous", width=20, command=lambda: on_option("Humorous"))
    btn_humorous.pack(pady=5)

    popup.after(100, lambda: popup.attributes('-topmost', False))  # Allow normal stacking after focus
    popup.mainloop()

# Function to show the rephrased text popup
def show_rephrased_popup(rephrased_text):
    def on_copy():
        pyperclip.copy(rephrased_text)
        print("[INFO] Rephrased text copied to clipboard.")
        popup.destroy()

    def on_close():
        print("Rephrased popup closed")
        popup.destroy()

    def on_minimize():
        popup.iconify()

    def start_move(event):
        popup.x = event.x
        popup.y = event.y

    def do_move(event):
        x = popup.winfo_pointerx() - popup.x
        y = popup.winfo_pointery() - popup.y
        popup.geometry(f"+{x}+{y}")

    popup = tk.Tk()
    popup.overrideredirect(True)  # Remove window decorations
    popup.geometry("400x200")
    popup.resizable(False, False)
    popup.attributes('-topmost', True)

    # Custom title bar frame
    title_bar = tk.Frame(popup, bg="#f0f0f0", relief='raised', bd=0, height=30)
    title_bar.pack(fill='x', side='top')
    title_bar.bind('<Button-1>', start_move)
    title_bar.bind('<B1-Motion>', do_move)

    # Icons in the custom title bar
    icon_frame = tk.Frame(title_bar, bg="#f0f0f0")
    icon_frame.pack(side='right', padx=5)

    copy_btn = tk.Button(icon_frame, text="📋", command=on_copy, bd=0, font=("Arial", 12), cursor="hand2", bg="#f0f0f0", activebackground="#e0e0e0")
    copy_btn.pack(side='left', padx=(0, 5))
    minimize_btn = tk.Button(icon_frame, text="-", command=on_minimize, bd=0, font=("Arial", 12), cursor="hand2", bg="#f0f0f0", activebackground="#e0e0e0")
    minimize_btn.pack(side='left', padx=(0, 5))
    close_btn = tk.Button(icon_frame, text="✕", command=on_close, bd=0, fg="red", font=("Arial", 12, "bold"), cursor="hand2", bg="#f0f0f0", activebackground="#e0e0e0")
    close_btn.pack(side='left')

    # Centered label
    label = tk.Label(popup, text="Rephrased Text:", bg="#f0f0f0")
    label.pack(pady=(10, 5))

    text_box = tk.Text(popup, height=5, width=45, wrap='word')
    text_box.insert('1.0', rephrased_text)
    text_box.config(state='disabled')
    text_box.pack(pady=5)

    popup.after(100, lambda: popup.attributes('-topmost', False))
    popup.mainloop()

# Function to handle the hotkey event
def on_hotkey():
    if not listening:
        return
    print("[HOTKEY] Triggered!")
    time.sleep(0.1)  # Just to ensure clipboard is ready
    copied_text = pyperclip.paste()
    if not copied_text.strip():
        print("[ERROR] Clipboard is empty or no text copied.")
        return
    show_popup(copied_text)

def add_hotkey():
    keyboard.add_hotkey(hotkey, on_hotkey)

def remove_hotkey():
    keyboard.remove_hotkey(hotkey)

def tray_icon():
    def create_image():
        # Simple black/white icon
        image = Image.new('RGB', (64, 64), color='white')
        d = ImageDraw.Draw(image)
        d.rectangle([16, 16, 48, 48], fill='black')
        return image

    def on_pause(icon, item):
        global listening
        listening = False
        remove_hotkey()
        print("[INFO] Paused hotkey listening.")
        icon.menu = pystray.Menu(
            pystray.MenuItem('Play', on_play),
            pystray.MenuItem('Exit', on_exit)
        )

    def on_play(icon, item):
        global listening
        listening = True
        add_hotkey()
        print("[INFO] Resumed hotkey listening.")
        icon.menu = pystray.Menu(
            pystray.MenuItem('Pause', on_pause),
            pystray.MenuItem('Exit', on_exit)
        )

    def on_exit(icon, item):
        print("[INFO] Exiting script.")
        icon.stop()
        sys.exit()

    menu = pystray.Menu(
        pystray.MenuItem('Pause', on_pause),
        pystray.MenuItem('Exit', on_exit)
    )
    icon = pystray.Icon("RephraseTool", create_image(), "Rephrase Tool", menu)
    icon.run()

# Start tray icon in a separate thread
tray_thread = threading.Thread(target=tray_icon, daemon=True)
tray_thread.start()

print("[INFO] Select and copy text, then press Ctrl+Alt+Shift+R to rephrase.")
add_hotkey()

# Keep the script running
keyboard.wait() 