import speech_recognition as sr
import pyttsx3
import subprocess
import os
import webbrowser
import re
import pyautogui
import time
import psutil
import fnmatch
import difflib
import threading
import langdetect

class SaraAssistant:
    def __init__(self, update_ui_callback=None):
        self.update_ui = update_ui_callback
        self.chat_mode = False
        self.start_ollama_background()

    def start_ollama_background(self):
        def run_model():
            subprocess.Popen(["ollama", "run", "llama2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        threading.Thread(target=run_model, daemon=True).start()

    def speak(self, text, language="en"):
        print(f"Sara: {text}")
        if self.update_ui:
            self.update_ui("log", f"{text}")
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if language == "en":
            for voice in voices:
                if 'zira' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        else:
            for voice in voices:
                if 'zira' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        engine.say(text)
        engine.runAndWait()

    def detect_language(self, text):
        try:
            lang = langdetect.detect(text)
            return "hinglish" if lang == "hi" else "english"
        except:
            return "english"

    def transcribe_audio_google(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Listening...")
            if self.update_ui:
                self.update_ui("status", "Listening")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🧠 You said: {text}")
            return text.lower()
        except:
            print("❌ Couldn't understand.")
            return ""

    def get_installed_apps(self):
        ps_script = """
        $apps = Get-StartApps
        $apps | ForEach-Object { "$($_.Name):::$(($_.AppID))" }
        """
        result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
        apps = {}
        for line in result.stdout.strip().split('\n'):
            if ":::" in line:
                name, appid = line.strip().split(":::")
                apps[name.lower()] = appid
        return apps

    def open_dynamic_app(self, app_name):
        apps = self.get_installed_apps()
        matches = difflib.get_close_matches(app_name.lower(), apps.keys(), n=1, cutoff=0.5)
        if matches:
            matched = matches[0]
            subprocess.run(["explorer", f"shell:AppsFolder\\{apps[matched]}"])
            self.speak(f"Opening {matched}")
            return True
        return False

    def close_app_by_name(self, app_name):
        closed_any = False
        app_name = app_name.lower()
        for proc in psutil.process_iter(['name']):
            try:
                if app_name in proc.info['name'].lower():
                    proc.kill()
                    closed_any = True
            except:
                continue
        if closed_any:
            self.speak(f"Closed {app_name}")
        else:
            self.speak(f"No running app found for {app_name}")

    def open_website_if_possible(self, text):
        if "." in text:
            url = f"https://{text.strip().replace(' ', '')}"
        else:
            url = f"https://{text.strip().replace(' ', '')}.com"
        self.speak(f"Opening {url}")
        webbrowser.open(url)

    def play_video_in_vlc(self, search_name):
        self.speak(f"Searching for {search_name} in your PC...")
        search_dirs = ["C:\\", "D:\\", "E:\\"]
        video_exts = ['.mp4', '.mkv', '.avi', '.mov']
        for base in search_dirs:
            for root, dirs, files in os.walk(base):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in video_exts) and search_name.lower() in file.lower():
                        os.startfile(os.path.join(root, file))
                        self.speak(f"Playing {search_name}")
                        return
        self.speak("No video found.")

    def toggle_vlc_play_pause(self):
        pyautogui.press('space')
        self.speak("Toggled play/pause in VLC")

    def play_on_youtube(self, query):
        self.speak(f"Searching YouTube for {query}")
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)

    def search_google(self, query):
        self.speak(f"Searching Google for {query}")
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)

    def open_file(self, file_name):
        search_dirs = ["C:\\", "D:\\", "E:\\"]
        for base in search_dirs:
            for root, dirs, files in os.walk(base):
                for file in files:
                    if file_name.lower() in file.lower():
                        os.startfile(os.path.join(root, file))
                        self.speak(f"Opening {file}")
                        return
        self.speak("No matching file found.")

    def open_notepad_and_write(self, content):
        os.system("start notepad")
        time.sleep(2)
        pyautogui.typewrite(content)
        self.speak("Code written in Notepad.")

    def start_llama_chat(self):
        self.speak("Sure, let's chat! Say 'that's enough' to stop.")
        self.chat_mode = True
        while self.chat_mode:
            user_input = self.transcribe_audio_google()
            if "that's enough" in user_input:
                self.chat_mode = False
                self.speak("Chat ended.")
                break
            if user_input:
                lang_type = self.detect_language(user_input)
                if self.update_ui:
                    self.update_ui("command", user_input)
                try:
                    response = subprocess.run(
                        ["ollama", "run", "llama2"],
                        input=user_input,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    output = response.stdout.strip()
                    if "generate" in user_input and "code" in user_input and "notepad" in user_input:
                        self.open_notepad_and_write(output)
                    else:
                        self.speak(output, language="en" if lang_type == "english" else "hi")
                except Exception as e:
                    self.speak("Error in AI response.")
                    print(f"⚠️ Error: {e}")

    def do_what_i_say(self, command):
        if self.update_ui:
            self.update_ui("command", command)

        if "shutdown sara" in command:
            self.speak("Shutting down. Bye!")
            exit()

        elif command in ["exit", "bye", "go idle"]:
            self.speak("Okay, going idle. Say 'Hey Sara' to wake me.")
            return "IDLE"

        elif "play" in command and "on vlc" in command:
            movie = command.replace("play", "").replace("on vlc", "").strip()
            self.play_video_in_vlc(movie)
            return

        elif "pause vlc" in command or "play vlc" in command:
            self.toggle_vlc_play_pause()
            return

        elif "search" in command and "youtube" in command:
            query = command.replace("search", "").replace("on youtube", "").strip()
            self.play_on_youtube(query)
            return

        elif "open youtube" in command or "youtube kholo" in command:
            self.speak("Opening YouTube homepage")
            webbrowser.open("https://www.youtube.com")
            return

        elif "close youtube" in command or "youtube band karo" in command:
            self.close_app_by_name("chrome")
            self.close_app_by_name("msedge")
            return

        elif "search" in command and ("google" in command or "chrome" in command):
            query = command.replace("search", "").replace("on google", "").replace("on chrome", "").strip()
            self.search_google(query)
            return

        elif "write" in command and "notepad" in command:
            self.speak("What should I write?")
            content = self.transcribe_audio_google()
            self.open_notepad_and_write(content)
            return

        elif "open" in command and "." in command:
            match = re.search(r"open (.+)", command)
            if match:
                self.open_website_if_possible(match.group(1))
                return

        elif "close" in command:
            match = re.search(r"close (.+)", command)
            if match:
                self.close_app_by_name(match.group(1))
                return

        elif "talk to me" in command or "Let's Chat" in command:
            self.start_llama_chat()
            return

        elif "open" in command or "start" in command or "karo" in command or "kholo" in command:
            app_or_site = command.replace("open", "").replace("start", "").replace("karo", "").replace("kholo", "").strip()
            if not self.open_dynamic_app(app_or_site):
                self.open_website_if_possible(app_or_site)
            return

        self.speak("Sorry, I couldn't understand that.")

    def run(self):
        self.speak("Hello! Say 'Hey Sara' to begin.")
        while True:
            self.speak("Sara is idle. Say 'Hey Sara' to activate.")
            while True:
                command = self.transcribe_audio_google()
                if any(trigger in command for trigger in ["hey sara", "hi sara", "hello sara"]):
                    self.speak("I'm here. How can I help?")
                    break

            while True:
                command = self.transcribe_audio_google()
                if not command:
                    continue
                result = self.do_what_i_say(command)
                if result == "IDLE":
                    break
