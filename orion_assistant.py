import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import threading
import datetime
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO

class OrionVirtualAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("ORION - Virtual Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a192f")
        self.root.resizable(False, False)

        # Initialize speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 1.0)

        # Set up voice recognition
        self.recognizer = sr.Recognizer()
        self.listening = False

        # Create GUI
        self.create_gui()

        # Initial greeting
        self.root.after(1000, self.greet_user)

    def create_gui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#0a192f")
        header_frame.pack(pady=20)

        title_label = tk.Label(
            header_frame,
            text="O R I O N",
            font=("Roboto Mono", 36, "bold"),
            fg="#00bcd4",
            bg="#0a192f"
        )
        title_label.pack()

        # Main content
        main_frame = tk.Frame(self.root, bg="#0a192f")
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Load and display assistant image
        try:
            response = requests.get(
                "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80"
            )
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((180, 180), Image.LANCZOS)
            self.assistant_img = ImageTk.PhotoImage(img)

            image_frame = tk.Frame(main_frame, bg="#0a192f")
            image_frame.pack(pady=10)
            image_label = tk.Label(
                image_frame,
                image=self.assistant_img,
                borderwidth=0,
                highlightthickness=0,
                bg="#0a192f"
            )
            image_label.image = self.assistant_img
            image_label.pack()
        except Exception as e:
            print(f"Error loading image: {e}")
            image_frame = tk.Frame(main_frame, bg="#0a192f")
            image_frame.pack(pady=10)
            image_label = tk.Label(
                image_frame,
                text="ORION",
                font=("Roboto Mono", 24),
                fg="#00bcd4",
                bg="#0a192f"
            )
            image_label.pack()

        # Assistant message
        message_label = tk.Label(
            main_frame,
            text="I'm ORION, your AI-powered virtual assistant. How may I help you?",
            font=("Roboto Mono", 14),
            fg="#b1b7b8",
            bg="#0a192f",
            wraplength=500
        )
        message_label.pack(pady=20)

        # Voice input section
        input_frame = tk.Frame(
            main_frame,
            bg="#273c4e", 
            bd=0,
            highlightthickness=0,
            relief=tk.FLAT
        )
        input_frame.pack(pady=20, padx=50, fill=tk.X)

        # Microphone button
        self.mic_button = tk.Button(
            input_frame,
            text="🎤",
            font=("Arial", 24),
            command=self.toggle_listening,
            bg="#1a2c3d",
            fg="#00bcd4",
            activebackground="#2a3c4d",
            activeforeground="#00bcd4",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5
        )
        self.mic_button.pack(side=tk.LEFT, padx=20, pady=10)

        # Status display
        self.status_var = tk.StringVar(value="Click the microphone to speak")
        status_label = tk.Label(
            input_frame,
            textvariable=self.status_var,
            font=("Roboto Mono", 14),
            fg="#aed0d0",
            bg="#273c4e",
            padx=20
        )
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Command examples
        # CORRECTED: Replaced invalid 'rgba' color with a valid hex code.
        command_frame = tk.Frame(main_frame, bg="#1a2c3d", bd=0)
        command_frame.pack(pady=40, padx=20, fill=tk.BOTH, expand=True)
        
        command_title = tk.Label(
            command_frame,
            text="Try saying:",
            font=("Roboto Mono", 16, "bold"),
            fg="#00bcd4",
            bg="#1a2c3d", # CORRECTED: Matched parent background.
            pady=10
        )
        command_title.pack()

        # Command grid
        command_grid = tk.Frame(command_frame, bg="#1a2c3d") # CORRECTED: Matched parent background.
        command_grid.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        commands = [
            ("\"Hello\" or \"Hey\"", "Greet ORION to start a conversation"),
            ("\"Open Google\"", "Open Google in a new tab"),
            ("\"What is the time?\"", "Get the current time"),
            ("\"Search for cats\"", "Search anything on Google"),
            ("\"What's today's date?\"", "Get the current date"),
            ("\"Who are you?\"", "Learn about ORION")
        ]

        # Create 2 columns for commands
        for i, (cmd, desc) in enumerate(commands):
            # CORRECTED: Replaced invalid 'rgba' with a valid hex code from the theme.
            frame = tk.Frame(command_grid, bg="#273c4e", bd=0)
            frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")

            cmd_label = tk.Label(
                frame,
                text=cmd,
                font=("Roboto Mono", 12, "bold"),
                fg="#00ff9d",
                bg="#273c4e", # CORRECTED: Matched parent background.
                anchor="w"
            )
            cmd_label.pack(fill=tk.X, padx=10, pady=(10, 0))

            desc_label = tk.Label(
                frame,
                text=desc,
                font=("Roboto Mono", 10),
                fg="#b1b7b8",
                bg="#273c4e", # CORRECTED: Matched parent background.
                anchor="w"
            )
            desc_label.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Configure grid columns to expand
        command_grid.columnconfigure(0, weight=1)
        command_grid.columnconfigure(1, weight=1)

        # Footer
        footer_frame = tk.Frame(self.root, bg="#0a192f")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        footer_label = tk.Label(
            footer_frame,
            text="ORION Virtual Assistant © 2025 | Designed with Python",
            font=("Roboto Mono", 10),
            fg="#7c8c8d",
            bg="#0a192f"
        )
        footer_label.pack()

    def greet_user(self):
        current_hour = datetime.datetime.now().hour
        if 5 <= current_hour < 12:
            greeting = "Good morning! I'm ORION, your virtual assistant."
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon! I'm ORION, your virtual assistant."
        else:
            greeting = "Good evening! I'm ORION, your virtual assistant."
        self.speak(greeting)

    def speak(self, text):
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
        threading.Thread(target=speak_thread, daemon=True).start()

    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.mic_button.config(fg="#ff0055")
            self.status_var.set("Listening...")
            threading.Thread(target=self.listen_for_speech, daemon=True).start()
        else:
            self.listening = False
            self.mic_button.config(fg="#00bcd4")
            self.status_var.set("Click the microphone to speak")

    def listen_for_speech(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio).lower()
                self.root.after(0, lambda: self.process_command(command))
            except sr.WaitTimeoutError:
                self.root.after(0, lambda: self.status_var.set("No speech detected"))
                self.root.after(3000, lambda: self.status_var.set("Click the microphone to speak"))
            except sr.UnknownValueError:
                self.root.after(0, lambda: self.status_var.set("Could not understand audio"))
                self.root.after(3000, lambda: self.status_var.set("Click the microphone to speak"))
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
                self.root.after(3000, lambda: self.status_var.set("Click the microphone to speak"))
            finally:
                self.root.after(0, self.toggle_listening)


    def process_command(self, command):
        self.status_var.set(f"You said: {command}")
        response = ""

        if any(word in command for word in ["hello", "hi", "hey"]):
            response = "Hello! How can I assist you today?"
        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            response = "Opening Google..."
        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            response = "Opening YouTube..."
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            response = f"Today's date is {current_date}"
        # CORRECTED: Improved logic for extracting search query.
        elif "search for" in command or "search" in command:
            query = ""
            if "search for" in command:
                # Use replace with count 1 to only replace the first instance
                query = command.replace("search for", "", 1).strip()
            else:
                query = command.replace("search", "", 1).strip()
            
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                response = f"Searching for {query} on Google"
            else:
                response = "What would you like me to search for?"
        elif "your name" in command or "who are you" in command:
            response = "I am ORION, your virtual assistant. Designed to help you with your daily tasks."
        elif "thank you" in command or "thanks" in command:
            response = "You're welcome! Is there anything else I can help you with?"
        elif "weather" in command:
            response = "I'm sorry, I don't have weather information at the moment."
        else:
            response = f"I'm not sure how to respond to that. You said: '{command}'"
        
        self.speak(response)
        self.root.after(5000, lambda: self.status_var.set("Click the microphone to speak"))

if __name__ == "__main__":
    root = tk.Tk()
    app = OrionVirtualAssistant(root)
    root.mainloop()