# 🎤 Sara - Your AI-Powered Voice Assistant

Sara is a **Python-based AI voice assistant** with a live GUI that listens to your voice commands, performs tasks like opening apps, searching the web, playing media, chatting with AI (LLaMA 2), and more — all in **real-time**.  
It comes with a **modern Tkinter-based frontend** featuring animations, a chat log, and a pulsing mic icon.

---

## 📸 Features
- **🎙️ Voice Commands** – Trigger Sara with "Hey Sara" or similar greetings.
- **💻 Open & Close Applications** – Launch installed apps dynamically using PowerShell.
- **🌐 Web Search** – Search Google or YouTube instantly.
- **🎬 Media Control** – Play/pause VLC, search and play local videos.
- **📂 File Operations** – Search and open files from drives.
- **📝 Notepad Automation** – Write dictated content directly into Notepad.
- **🤖 AI Chat Mode** – Have natural conversations with LLaMA 2 via `ollama`.
- **🔊 Multilingual Support** – Detects Hindi/English and adjusts responses.
- **📊 Live GUI** – Animated mic glow, live status, command history, and chat log.
- **🖥️ Cross-Platform Support** – Primarily for Windows, but adaptable.

---

## 📂 Project Structure

Sara-Voice-Assistant/
│
├── sara.py # Backend logic for Sara's commands and AI chat
├── gui.py # Tkinter frontend for Sara
├── icon.png # (Optional) Mic icon image for the GUI
├── requirements.txt # Required Python packages
└── README.md # Project documentation


---

## ⚙️ Requirements

Make sure you have:
- **Python 3.8+** installed
- **Ollama** installed with the `llama2` model pulled  
  👉 [Download Ollama](https://ollama.ai/download) and run:
  ```bash
  ollama pull llama2


VLC Media Player (for media controls)

Windows OS (PowerShell commands are used for fetching installed apps)

📦 Installation
1️⃣ Clone this repository

bash
Copy
Edit
git clone https://github.com/Tapish1310/sara-voice-assistant.git
cd sara-voice-assistant


2️⃣ Install dependencies

bash
Copy
Edit
pip install -r requirements.txt


3️⃣ Ensure Ollama is running in the background

bash
Copy
Edit
ollama serve

4️⃣ Run Sara

bash
Copy
Edit
python gui.py



🎮 Usage
Start Sara
Launch gui.py — a window will appear with a glowing mic icon.

Activate Sara
Say "Hey Sara", "Hi Sara", or "Hello Sara".

Give Commands
Example commands:

"Open YouTube"

"Search AI on Google"

"Play Avengers on VLC"

"Write in Notepad"

"Talk to me" → enters AI chat mode

"That's enough" → exits AI chat mode

"Close Chrome"

Idle Mode
Say "bye" or "go idle" to put Sara in idle listening mode.

🖼️ GUI Features
Pulsing Mic Animation – Indicates listening mode.

Status Indicator – Shows whether Sara is idle, listening, or processing.

Command History – Displays your last spoken command.

Chat Log – Shows back-and-forth between you and Sara.

🔧 Customization
Mic Icon: Replace icon.png with your preferred image.

Search Directories: Modify search_dirs in sara.py for file/video searches.

Voice: Change TTS voice in speak() method.

⚠️ Known Limitations
Windows-specific PowerShell command for listing apps.

LLaMA 2 chat requires ollama installed and configured.

Voice recognition depends on microphone quality and background noise.

📜 License
This project is licensed under the MIT License — feel free to modify and use it.

💡 Acknowledgements
Ollama for running local AI models.

SpeechRecognition for voice input.

Pyttsx3 for text-to-speech.

Tkinter for the GUI.