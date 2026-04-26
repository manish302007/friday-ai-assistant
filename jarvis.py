import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pyautogui
import pywhatkit
import psutil
import requests
import wikipedia
import subprocess
import threading
import customtkinter as ctk
from groq import Groq

# ========== SETUP ==========
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

client = Groq(api_key="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")

contacts = {
    "mom": "+91XXXXXXXXXX",
    "dad": "+91XXXXXXXXXX",
    "rahul": "+91XXXXXXXXXX",
    "bhai": "+91XXXXXXXXXX",
}

apps = {
    "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "vs code": "C:/Users/manis/AppData/Local/Programs/Microsoft VS Code/Code.exe",
    "vscode": "C:/Users/manis/AppData/Local/Programs/Microsoft VS Code/Code.exe",
    "whatsapp": "C:/Users/manis/AppData/Local/WhatsApp/WhatsApp.exe",
    "spotify": "C:/Users/manis/AppData/Roaming/Spotify/Spotify.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "explorer": "explorer.exe",
    "paint": "mspaint.exe",
    "telegram": "C:/Users/manis/AppData/Roaming/Telegram Desktop/Telegram.exe",
}

# ========== MAIN APP ==========
class FridayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FRIDAY — Advanced AI Assistant")
        self.geometry("1100x700")
        self.configure(fg_color="#0a0a0a")
        self.resizable(False, False)
        self.is_listening = False
        self.build_ui()
        self.after(500, self.startup_sequence)

    def build_ui(self):
        # ===== TOP BAR =====
        top = ctk.CTkFrame(self, fg_color="#0d0d0d", height=60, corner_radius=0)
        top.pack(fill="x", side="top")

        ctk.CTkLabel(top, text="⚡ F.R.I.D.A.Y", font=("Courier New", 22, "bold"),
                     text_color="#ff3c3c").pack(side="left", padx=20, pady=10)

        self.status_label = ctk.CTkLabel(top, text="● ONLINE",
                                          font=("Courier New", 13), text_color="#00ff88")
        self.status_label.pack(side="left", padx=10)

        self.clock_label = ctk.CTkLabel(top, text="",
                                         font=("Courier New", 13), text_color="#888888")
        self.clock_label.pack(side="right", padx=20)
        self.update_clock()

        # ===== MAIN CONTENT =====
        main = ctk.CTkFrame(self, fg_color="#0a0a0a")
        main.pack(fill="both", expand=True, padx=10, pady=5)

        # LEFT PANEL
        left = ctk.CTkFrame(main, fg_color="#0d0d0d", width=320, corner_radius=12)
        left.pack(side="left", fill="y", padx=(0, 5), pady=5)
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="SYSTEM STATUS",
                     font=("Courier New", 11, "bold"),
                     text_color="#ff3c3c").pack(pady=(15, 5), padx=15, anchor="w")

        # Battery
        self.battery_label = ctk.CTkLabel(left, text="🔋 Battery: --",
                                           font=("Courier New", 11), text_color="#aaaaaa")
        self.battery_label.pack(pady=3, padx=15, anchor="w")

        # CPU
        self.cpu_label = ctk.CTkLabel(left, text="⚙️ CPU: --",
                                       font=("Courier New", 11), text_color="#aaaaaa")
        self.cpu_label.pack(pady=3, padx=15, anchor="w")

        # RAM
        self.ram_label = ctk.CTkLabel(left, text="💾 RAM: --",
                                       font=("Courier New", 11), text_color="#aaaaaa")
        self.ram_label.pack(pady=3, padx=15, anchor="w")

        self.update_system_stats()

        ctk.CTkFrame(left, fg_color="#222222", height=1).pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(left, text="QUICK ACCESS",
                     font=("Courier New", 11, "bold"),
                     text_color="#ff3c3c").pack(pady=5, padx=15, anchor="w")

        quick_btns = [
            ("▶ YouTube", "https://youtube.com"),
            ("🔍 Google", "https://google.com"),
            ("💬 WhatsApp", "https://web.whatsapp.com"),
            ("🐙 GitHub", "https://github.com/manish302007"),
            ("📰 News", "https://news.google.com"),
            ("🤖 ChatGPT", "https://chat.openai.com"),
        ]

        for label, url in quick_btns:
            ctk.CTkButton(left, text=label, font=("Courier New", 11),
                          fg_color="#1a1a1a", hover_color="#2a2a2a",
                          text_color="#cccccc", height=30, corner_radius=6,
                          command=lambda u=url: self.quick_open(u)).pack(
                          fill="x", padx=15, pady=2)

        # CENTER PANEL
        center = ctk.CTkFrame(main, fg_color="#0d0d0d", corner_radius=12)
        center.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(center, text="CONVERSATION LOG",
                     font=("Courier New", 11, "bold"),
                     text_color="#ff3c3c").pack(pady=(15, 5), padx=15, anchor="w")

        self.chat_box = ctk.CTkTextbox(center, font=("Courier New", 12),
                                        fg_color="#111111", text_color="#cccccc",
                                        wrap="word", state="disabled",
                                        scrollbar_button_color="#333333")
        self.chat_box.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # AI CIRCLE
        self.circle_label = ctk.CTkLabel(center, text="◉",
                                          font=("Courier New", 40, "bold"),
                                          text_color="#ff3c3c")
        self.circle_label.pack(pady=5)

        self.state_label = ctk.CTkLabel(center, text="STANDBY",
                                         font=("Courier New", 12, "bold"),
                                         text_color="#555555")
        self.state_label.pack(pady=2)

        # BOTTOM BUTTONS
        btn_frame = ctk.CTkFrame(center, fg_color="#0d0d0d")
        btn_frame.pack(fill="x", padx=15, pady=10)

        self.mic_btn = ctk.CTkButton(btn_frame, text="🎙️ SPEAK TO FRIDAY",
                                      font=("Courier New", 13, "bold"),
                                      fg_color="#ff3c3c", hover_color="#cc0000",
                                      text_color="white", height=45, corner_radius=8,
                                      command=self.start_listening)
        self.mic_btn.pack(fill="x", pady=(0, 5))

        # TEXT INPUT
        input_frame = ctk.CTkFrame(btn_frame, fg_color="#0d0d0d")
        input_frame.pack(fill="x")

        self.text_input = ctk.CTkEntry(input_frame, font=("Courier New", 12),
                                        fg_color="#111111", text_color="#cccccc",
                                        placeholder_text="Or type command here...",
                                        border_color="#333333", height=38)
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.text_input.bind("<Return>", self.handle_text_input)

        ctk.CTkButton(input_frame, text="SEND", font=("Courier New", 12, "bold"),
                      fg_color="#1a1a1a", hover_color="#2a2a2a",
                      text_color="#ff3c3c", width=70, height=38,
                      command=self.handle_text_input).pack(side="right")

        # RIGHT PANEL
        right = ctk.CTkFrame(main, fg_color="#0d0d0d", width=220, corner_radius=12)
        right.pack(side="right", fill="y", padx=(5, 0), pady=5)
        right.pack_propagate(False)

        ctk.CTkLabel(right, text="FRIDAY INFO",
                     font=("Courier New", 11, "bold"),
                     text_color="#ff3c3c").pack(pady=(15, 5), padx=15, anchor="w")

        info_items = [
            ("Boss", "Manish"),
            ("City", "Jaipur"),
            ("Degree", "BTech AI/DS"),
            ("Version", "Friday 1.0"),
            ("Model", "Llama 3.3 70B"),
            ("Status", "Active"),
        ]

        for label, value in info_items:
            frame = ctk.CTkFrame(right, fg_color="#111111", corner_radius=6)
            frame.pack(fill="x", padx=15, pady=2)
            ctk.CTkLabel(frame, text=label, font=("Courier New", 10),
                         text_color="#666666").pack(side="left", padx=8, pady=5)
            ctk.CTkLabel(frame, text=value, font=("Courier New", 10, "bold"),
                         text_color="#ff3c3c").pack(side="right", padx=8, pady=5)

        ctk.CTkFrame(right, fg_color="#222222", height=1).pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(right, text="COMMANDS",
                     font=("Courier New", 11, "bold"),
                     text_color="#ff3c3c").pack(pady=5, padx=15, anchor="w")

        commands = [
            "Open YouTube",
            "Play [song]",
            "Search [topic]",
            "Weather in [city]",
            "Latest news",
            "Take screenshot",
            "Battery status",
            "Volume up/down",
            "Tell me a joke",
            "Motivate me",
            "Open WhatsApp",
            "Message [name]",
            "Lock laptop",
            "Shutdown",
        ]

        for cmd in commands:
            ctk.CTkLabel(right, text=f"› {cmd}",
                         font=("Courier New", 10),
                         text_color="#666666").pack(anchor="w", padx=15, pady=1)

    # ========== UI FUNCTIONS ==========
    def update_clock(self):
        now = datetime.datetime.now().strftime("%A %I:%M:%S %p")
        self.clock_label.configure(text=now)
        self.after(1000, self.update_clock)

    def update_system_stats(self):
        try:
            battery = psutil.sensors_battery()
            percent = int(battery.percent)
            plugged = "⚡" if battery.power_plugged else "🔋"
            self.battery_label.configure(text=f"{plugged} Battery: {percent}%")
            cpu = psutil.cpu_percent()
            self.cpu_label.configure(text=f"⚙️ CPU: {cpu}%")
            ram = psutil.virtual_memory().percent
            self.ram_label.configure(text=f"💾 RAM: {ram}%")
        except:
            pass
        self.after(3000, self.update_system_stats)

    def add_to_chat(self, sender, message):
        self.chat_box.configure(state="normal")
        if sender == "Boss":
            self.chat_box.insert("end", f"\n👤 Boss: {message}\n", )
        else:
            self.chat_box.insert("end", f"🤖 Friday: {message}\n\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def set_state(self, state, color):
        self.state_label.configure(text=state, text_color=color)
        self.circle_label.configure(text_color=color)

    def quick_open(self, url):
        self.open_in_chrome(url)
        self.add_to_chat("Friday", f"Opening {url} Boss!")

    def handle_text_input(self, event=None):
        query = self.text_input.get().strip().lower()
        if query:
            self.text_input.delete(0, "end")
            self.add_to_chat("Boss", query)
            threading.Thread(target=self.process_command, args=(query,), daemon=True).start()

    def startup_sequence(self):
        self.set_state("INITIALIZING...", "#ffaa00")
        self.after(1000, lambda: self.set_state("SYSTEMS ONLINE", "#00ff88"))
        self.after(1500, lambda: threading.Thread(target=self.greet, daemon=True).start())

    # ========== CORE FUNCTIONS ==========
    def speak(self, text):
        self.add_to_chat("Friday", text)
        self.set_state("SPEAKING", "#ff3c3c")
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        self.set_state("STANDBY", "#555555")

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.set_state("LISTENING...", "#00ff88")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=7)
            except sr.WaitTimeoutError:
                self.set_state("STANDBY", "#555555")
                return ""

        try:
            self.set_state("PROCESSING...", "#ffaa00")
            query = r.recognize_google(audio, language='en-in')
            self.add_to_chat("Boss", query)
            return query.lower()
        except sr.UnknownValueError:
            self.speak("Didn't catch that Boss, say again!")
            return ""
        except sr.RequestError:
            self.speak("Network error Boss!")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.mic_btn.configure(text="🔴 LISTENING...", fg_color="#cc0000")
            threading.Thread(target=self.listen_and_process, daemon=True).start()

    def listen_and_process(self):
        query = self.listen()
        self.is_listening = False
        self.mic_btn.configure(text="🎙️ SPEAK TO FRIDAY", fg_color="#ff3c3c")
        if query:
            self.process_command(query)

    def ask_groq(self, query):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Friday, an advanced female AI assistant of Boss. Boss is Manish, a BTech AI and Data Science student from Jaipur. Always call him Boss. Answer short and crisp in 2-3 lines only. Be professional, smart and friendly. Do not use bullet points or markdown symbols. Sound like a real advanced AI assistant."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq Error: {e}")
            return "Sorry Boss, I couldn't connect right now!"

    def open_in_chrome(self, url):
        chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        if os.path.exists(chrome):
            subprocess.Popen([chrome, url])
        else:
            webbrowser.open(url)

    def open_app(self, app_name):
        app_name = app_name.lower().strip()
        for key, path in apps.items():
            if key in app_name:
                try:
                    subprocess.Popen(path)
                    return f"Opening {key} Boss!"
                except:
                    os.system(f'start "" "{path}"')
                    return f"Opening {key} Boss!"
        return None

    def get_news(self, topic=""):
        try:
            if topic:
                result = self.ask_groq(f"Give me 3 latest news headlines about {topic} today. No bullet points.")
                self.open_in_chrome(f"https://www.google.com/search?q={topic}+news+today&tbm=nws")
            else:
                result = self.ask_groq("Give me 3 latest top world news headlines today. No bullet points.")
                self.open_in_chrome("https://news.google.com")
            return result
        except:
            return "Could not fetch news Boss!"

    def send_whatsapp(self, query):
        try:
            words = query.lower().split()
            for name, number in contacts.items():
                if name in words:
                    idx = words.index(name) + 1
                    message = " ".join(words[idx:])
                    if not message:
                        self.speak(f"What message should I send to {name} Boss?")
                        message = self.listen()
                    pywhatkit.sendwhatmsg_instantly(number, message, 15)
                    return f"Message sent to {name} Boss!"
            return "Contact not found Boss!"
        except Exception as e:
            return "Could not send message Boss!"

    def greet(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            self.speak("Good Morning Boss! I am Friday, your advanced AI assistant. All systems are online!")
        elif hour < 18:
            self.speak("Good Afternoon Boss! I am Friday, your advanced AI assistant. All systems are online!")
        else:
            self.speak("Good Evening Boss! I am Friday, your advanced AI assistant. All systems are online!")

    # ========== COMMAND HANDLER ==========
    def process_command(self, query):
        if "hello" in query or "hi" in query or "hey" in query:
            hour = datetime.datetime.now().hour
            if hour < 12:
                self.speak("Good Morning Boss! How can I assist you?")
            elif hour < 18:
                self.speak("Good Afternoon Boss! How can I assist you?")
            else:
                self.speak("Good Evening Boss! How can I assist you?")

        elif "your name" in query:
            self.speak("I am Friday, your advanced personal AI assistant Boss!")

        elif "how are you" in query:
            self.speak("All systems are fully operational Boss! Ready to assist!")

        elif "time" in query:
            time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"Boss, current time is {time}!")

        elif "date" in query:
            date = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Boss, today is {date}!")

        elif "weather" in query:
            city = query.split("in")[-1].strip() if "in" in query else "Jaipur"
            self.speak(f"Checking weather in {city} Boss!")
            result = self.ask_groq(f"What is the weather in {city} today? 2 lines only.")
            self.speak(result)

        elif "news" in query:
            if "about" in query:
                topic = query.split("about")[-1].strip()
            elif "on" in query:
                topic = query.split("on")[-1].strip()
            else:
                topic = ""
            self.speak("Fetching latest news Boss!")
            result = self.get_news(topic)
            self.speak(result)

        elif "who is" in query or "tell me about" in query:
            search = query.replace("who is", "").replace("tell me about", "").strip()
            self.speak(f"Searching about {search} Boss!")
            try:
                wikipedia.set_lang("en")
                result = wikipedia.summary(search, sentences=2)
                self.open_in_chrome(f"https://en.wikipedia.org/wiki/{search.replace(' ', '_')}")
            except:
                result = self.ask_groq(query)
            self.speak(result)

        elif "open" in query:
            app_name = query.replace("open", "").strip()
            sites = {
                "youtube": "https://youtube.com",
                "google": "https://google.com",
                "github": "https://github.com/manish302007",
                "instagram": "https://instagram.com",
                "twitter": "https://twitter.com",
                "chatgpt": "https://chat.openai.com",
                "linkedin": "https://linkedin.com",
                "gmail": "https://mail.google.com",
                "netflix": "https://netflix.com",
                "spotify web": "https://open.spotify.com",
            }
            opened = False
            for site, url in sites.items():
                if site in app_name:
                    self.speak(f"Opening {site} Boss!")
                    self.open_in_chrome(url)
                    opened = True
                    break
            if not opened:
                result = self.open_app(app_name)
                if result:
                    self.speak(result)
                else:
                    self.speak(f"Searching {app_name} online Boss!")
                    self.open_in_chrome(f"https://www.google.com/search?q={app_name}")

        elif "play" in query:
            song = query.replace("play", "").strip()
            self.speak(f"Playing {song} on YouTube Boss!")
            pywhatkit.playonyt(song)

        elif "search" in query:
            search = query.replace("search", "").strip()
            self.speak(f"Searching {search} on Google Boss!")
            self.open_in_chrome(f"https://www.google.com/search?q={search}")

        elif "message" in query or "send" in query:
            self.speak("Sending WhatsApp message Boss!")
            result = self.send_whatsapp(query)
            self.speak(result)

        elif "screenshot" in query:
            screenshot = pyautogui.screenshot()
            path = os.path.join(os.path.expanduser("~"), "Desktop", "screenshot.png")
            screenshot.save(path)
            self.speak("Screenshot taken and saved on desktop Boss!")

        elif "battery" in query:
            battery = psutil.sensors_battery()
            percent = int(battery.percent)
            plugged = "charging" if battery.power_plugged else "not charging"
            self.speak(f"Boss, battery is at {percent} percent and is {plugged}!")

        elif "volume up" in query:
            pyautogui.press("volumeup", presses=5)
            self.speak("Volume increased Boss!")

        elif "volume down" in query:
            pyautogui.press("volumedown", presses=5)
            self.speak("Volume decreased Boss!")

        elif "mute" in query:
            pyautogui.press("volumemute")
            self.speak("Muted Boss!")

        elif "system info" in query or "cpu" in query:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.speak(f"Boss, CPU is at {cpu} percent and RAM is at {ram} percent!")

        elif "ip address" in query:
            try:
                ip = requests.get("https://api.ipify.org").text
                self.speak(f"Boss, your public IP address is {ip}!")
            except:
                self.speak("Could not fetch IP address Boss!")

        elif "joke" in query:
            joke = self.ask_groq("Tell me a very funny short joke")
            self.speak(joke)

        elif "motivate" in query or "motivation" in query:
            quote = self.ask_groq("Give me a powerful motivational quote for a BTech AI student")
            self.speak(quote)

        elif "explain" in query or "teach" in query or "what is" in query:
            self.speak("Let me think Boss!")
            response = self.ask_groq(query)
            self.speak(response)

        elif "shutdown" in query:
            self.speak("Shutting down your laptop in 5 seconds Boss!")
            os.system("shutdown /s /t 5")

        elif "restart" in query:
            self.speak("Restarting your laptop Boss!")
            os.system("shutdown /r /t 5")

        elif "lock" in query:
            self.speak("Locking your laptop Boss!")
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif "stop" in query or "exit" in query or "bye" in query:
            self.speak("Goodbye Boss! Have a productive day. Friday signing off!")
            self.after(2000, self.destroy)

        else:
            self.speak("Let me think Boss!")
            response = self.ask_groq(query)
            self.speak(response)

# ========== RUN ==========
if __name__ == "__main__":
    app = FridayApp()
    app.mainloop()