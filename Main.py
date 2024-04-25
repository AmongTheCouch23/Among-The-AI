import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import speech_recognition as sr
import pyttsx3
import wikipedia
import os
import datetime
import sys
import webbrowser
import subprocess
import re
from youtubesearchpython import VideosSearch
import openai
import nltk
from PersonalityGenerator import RoleBasedPersonality, ComprehensivePersonality

class VoiceAssistant:
    def __init__(self, text_widget):
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()
        self.start_time = datetime.datetime.now()
        self.paused = False
        self.text_widget = text_widget
        self.running = False

        self.RoleBasedPersonality = RoleBasedPersonality
        self.role_based_personality_instance = self.RoleBasedPersonality()
        self.role_based_personality_profile = self.role_based_personality_instance.generate_profile()

        self.ComprehensivePersonality = ComprehensivePersonality
        self.comprehensive_personality_instance = self.ComprehensivePersonality()
        
        openai.api_key = 'your-api-token-here'
        
        self.openai = openai

    def listen(self):
        with sr.Microphone() as source:
            # You can add some wait or static noise thresholding here.
            print("Listening...")
            audio = self.recognizer.listen(source)
            print("Processing...")
            try:
                # Try to recognize the recorded audio.
                statement = self.recognizer.recognize_google(audio)
                print("You said: ", statement)
                return statement
            except sr.RequestError:
                # API was unreachable or unresponsive
                print("API unavailable/unresponsive")
                return ""
            except sr.UnknownValueError:
                # speech was unintelligible
                print("Unable to recognize speech")
                return ""

    def speak(self, text):
        self.text_widget.insert(tk.END, f"Assistant: {text}\n")
        self.speaker.say(text)
        self.speaker.runAndWait()

    def generate_text(self, prompt):
        total_prompt = f"{str(self.role_based_personality_profile)}. Think like a friendly person. Now, regarding your question, '{prompt}'"
        response = self.openai.Completion.create(engine="davinci-002", prompt=total_prompt, temperature=0.6, max_tokens=400)
        text = response.choices[0].text.strip()
        sentences = nltk.sent_tokenize(text)  # breaks text into sentences
        condensed_text = ' '.join(sentences[:2])
        self.speak(condensed_text)  # Speak the generated text answer

    def execute_command(self, command):
        if self.paused:
            if "unpause assistant" in command:
                self.unpause_assistant()
            else:
                print("Assistant is paused. Listening for 'unpause assistant' only.")
        else:
            if "open" in command:
                self.open_application(command)
            elif "type" in command:
                self.type_text(command)
            elif "search" in command:
                self.search_web(command)
            elif "tell me about" in command:
                self.get_wikipedia_summary(command)
            elif "up time" in command:
                self.speak(self.get_uptime())
            elif "pause assistant" in command:
                self.pause_assistant()
            elif "play" in command:
                self.play_song(command)
            elif "goodbye" in command:
                self.speak("Goodbye!")
                self.running = False
            else:
                self.generate_text(command)  # Generate text if command is not recognized

    def play_song(self, command):
        song_query = re.search(r'play (.+)', command).group(1)
        videos = self.search_youtube_music(song_query)
        if videos:
            top_video = videos[0]
            self.speak(f"Playing {top_video['title']} by {top_video['channel']['name']}")
            
            video_url = f"https://www.youtube.com/watch?v={top_video['id']}"
            webbrowser.open(video_url)
        else:
            self.speak(f"Sorry, I couldn't find any results for {song_query} on YouTube Music.")

    def get_uptime(self):
        timedelta_obj = datetime.datetime.now() - self.start_time
        uptime_str = str(timedelta_obj)
        return uptime_str
    
    def search_youtube_music(self, query):
        video_search = VideosSearch(query, limit=1)
        results = video_search.result()
        videos = results['result']

        return videos
    
    def open_application(self, command):
        app_name = command.split("open ")[1]
        try:
            subprocess.Popen(["start", " ", app_name], shell=True)
            self.speak(f"Opening {app_name}.")
        except Exception as e:
            try:
                os.startfile(app_name)
                self.speak(f"Opening {app_name}.")
            except Exception as e:
                self.speak(f"Error opening {app_name}: {e}")

    def type_text(self, command):
        text_to_type = command.split("type ")[1]
        os.system(f'echo {text_to_type}| clip')
        self.speak("Text copied to clipboard.")
        self.speak("Please paste it where needed.")

    def search_web(self, command):
        search_query = command.split("search ")[1]
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

    def get_wikipedia_summary(self, command):
        query = command.replace("tell me about", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=1)
            self.speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak(f"There are multiple results for {query}. Please be more specific.")
        except wikipedia.exceptions.PageError as e:
            self.speak(f"Sorry, I couldn't find information about {query}.")

    def pause_assistant(self):
        self.paused = True
        self.speak("Assistant paused.")

    def unpause_assistant(self):
        self.paused = False
        self.speak("Assistant unpaused.")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant GUI")

        self.text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.text_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start Assistant", command=self.start_assistant)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(root, text="Stop Assistant", command=self.stop_assistant, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)

        self.pause_button = tk.Button(root, text="Toggle Pause Assistant", command=self.toggle_pause_assistant, state=tk.DISABLED)
        self.pause_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.assistant = None
        self.assistant_thread = None

    def start_assistant(self):
        self.text_widget.delete(1.0, tk.END)
        self.assistant = VoiceAssistant(self.text_widget)
        self.assistant_thread = Thread(target=self.assistant_loop)
        self.assistant_thread.start()

        self.start_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.NORMAL
        self.pause_button["state"] = tk.NORMAL

    def stop_assistant(self):
        if self.assistant:
            self.assistant.running = False
            self.assistant_thread.join()
            self.root.destroy()
            restart_program()

    def assistant_loop(self):
        self.assistant.running = True
        while self.assistant.running:
            if self.assistant:
                user_command = self.assistant.listen()
                if user_command:
                    self.assistant.execute_command(user_command)

    def toggle_pause_assistant(self):
        if self.assistant:
            if self.assistant.paused:
                self.assistant.unpause_assistant()
            else:
                self.assistant.pause_assistant()

def restart_program():
    python_executable = sys.executable
    script_path = os.path.abspath(__file__)
    subprocess.Popen([python_executable, script_path])
    sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()