import tkinter as tk
from tkinter import ttk
import threading
import time
from sara import SaraAssistant
from PIL import Image, ImageTk
import os

class SaraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sara - Your Voice Assistant")
        self.root.geometry("700x600")
        self.root.configure(bg="#0d1117")

        # Mic Glow Canvas
        self.canvas = tk.Canvas(self.root, width=150, height=150, bg="#0d1117", highlightthickness=0)
        self.canvas.place(x=275, y=20)
        self.glow = self.canvas.create_oval(20, 20, 130, 130, fill="#1f6feb", outline="")

        # Mic Icon (optional icon.png)
        icon_path = "icon.png"
        if os.path.exists(icon_path):
            try:
                mic_image = Image.open(icon_path).resize((40, 40))
                self.mic_img = ImageTk.PhotoImage(mic_image)
                self.canvas.create_image(75, 75, image=self.mic_img)
            except Exception as e:
                print(f"⚠️ Error loading icon.png: {e}")
        else:
            print("⚠️ icon.png not found. Skipping mic image.")

        # Status
        self.status_label = tk.Label(self.root, text="Status: Idle", fg="#39d353", bg="#0d1117", font=("Segoe UI", 12))
        self.status_label.pack(pady=(180, 0))

        self.last_command_label = tk.Label(self.root, text="Last Command: None", fg="#58a6ff", bg="#0d1117", font=("Segoe UI", 11))
        self.last_command_label.pack(pady=5)

        # Chat Log
        self.log_frame = tk.Frame(self.root, bg="#0d1117")
        self.log_frame.pack(pady=10, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.log_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_log = tk.Text(self.log_frame, bg="#161b22", fg="white", wrap="word", font=("Consolas", 10), yscrollcommand=self.scrollbar.set)
        self.chat_log.pack(fill="both", expand=True)
        self.chat_log.insert(tk.END, "💬 Sara: Hello! Say 'Hey Sara' to begin.\n")
        self.chat_log.config(state=tk.DISABLED)
        self.scrollbar.config(command=self.chat_log.yview)

        # Initialize Sara Assistant
        self.sara = SaraAssistant(update_ui_callback=self.update_ui)

        # Start Sara thread
        threading.Thread(target=self.sara.run, daemon=True).start()

        # Mic pulse animation
        self.animate_glow()

    def update_ui(self, type_, message):
        if type_ == "status":
            self.status_label.config(text=f"Status: {message}")
        elif type_ == "command":
            self.last_command_label.config(text=f"Last Command: {message}")
            self.append_to_log("🧠 You", message)
        elif type_ == "log":
            self.append_to_log("💬 Sara", message)

    def append_to_log(self, speaker, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"{speaker}: {message}\n")
        self.chat_log.see(tk.END)
        self.chat_log.config(state=tk.DISABLED)

    def animate_glow(self):
        def pulse():
            scale = 0
            growing = True
            while True:
                scale += 1 if growing else -1
                radius = 55 + (scale * 2)
                self.canvas.coords(self.glow, 75 - radius//2, 75 - radius//2, 75 + radius//2, 75 + radius//2)
                if scale >= 10:
                    growing = False
                elif scale <= 0:
                    growing = True
                time.sleep(0.05)

        threading.Thread(target=pulse, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SaraGUI(root)
    root.mainloop()


