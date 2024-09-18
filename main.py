import os
import webbrowser
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pvporcupine
import struct
import pyaudio

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for wake word ("Jarvis")
def detect_wake_word():
    porcupine = pvporcupine.create(keywords=["jarvis"])
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
    
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            speak("Yes, how can I assist you?")
            handle_command()

# Function to recognize and return voice input as a command
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"Command recognized: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return None

# Function to handle commands
def handle_command():
    command = listen_command()
    if command:
        if 'wikipedia' in command:
            search_wikipedia(command)
        elif 'open youtube' in command:
            open_website('https://www.youtube.com')
        elif 'open google' in command:
            open_website('https://www.google.com')
        elif 'time' in command:
            tell_time()
        elif 'date' in command:
            tell_date()
        elif 'shutdown' in command:
            shutdown_pc()
        elif 'restart' in command:
            restart_pc()
        elif 'play music' in command:
            play_music()
        elif 'exit' in command or 'stop' in command:
            speak("Goodbye!")
            exit()

# Function to search Wikipedia
def search_wikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace('wikipedia', '')
    result = wikipedia.summary(query, sentences=2)
    speak(f"According to Wikipedia, {result}")

# Function to open a website
def open_website(url):
    speak(f"Opening {url}")
    webbrowser.open(url)

# Function to tell the current time
def tell_time():
    str_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {str_time}")

# Function to tell the current date
def tell_date():
    str_date = datetime.datetime.now().strftime("%Y-%m-%d")
    speak(f"Today's date is {str_date}")

# Function to shutdown the PC
def shutdown_pc():
    speak("Shutting down the PC.")
    os.system('shutdown /s /t 1')

# Function to restart the PC
def restart_pc():
    speak("Restarting the PC.")
    os.system('shutdown /r /t 1')

# Function to play music (requires valid path to music directory)
def play_music():
    music_dir = "path_to_music_directory"  # Replace with actual path
    songs = os.listdir(music_dir)
    speak("Playing music.")
    os.startfile(os.path.join(music_dir, songs[0]))

# Main function to start the AI assistant
def main():
    speak("Hello! I am Jarvis. Waiting for your command.")
    detect_wake_word()

# Start the assistant
if __name__ == "_main_":
    main()