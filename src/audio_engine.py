
import speech_recognition as sr
import edge_tts
import pygame
import os
import asyncio
import time

# Initialize pygame mixer for audio playback
pygame.mixer.init()

class AudioEngine:
    def __init__(self, status_callback=None):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.status_callback = status_callback # Function to call with status updates
        
        # Adjust for ambient noise once at startup
        with self.microphone as source:
            if self.status_callback: self.status_callback("Adjusting noise...")
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready.")

    def update_status(self, status):
        if self.status_callback:
            self.status_callback(status)

    def listen(self):
        """
        Listens to the microphone and returns the recognized text.
        Returns None if no speech is detected or if it's unintelligible.
        """
        with self.microphone as source:
            self.update_status("Listening...")
            print("Listening...")
            try:
                # Listen with a timeout to avoid hanging forever
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                self.update_status("Thinking...")
                print("Processing audio...")
                text = self.recognizer.recognize_google(audio)
                print(f"User said: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None

    async def speak(self, text):
        """
        Synthesizes text to speech and plays it.
        """
        self.update_status("Speaking...")
        print(f"Assistant: {text}")
        if not text:
            return

        OUTPUT_FILE = "response.mp3"
        VOICE = "en-US-AriaNeural" # High quality female voice
        # RATE = "+0%"
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(OUTPUT_FILE)

        # Play the audio
        try:
            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
             # Stop and unload to release the file lock
             pygame.mixer.music.stop()
             try:
                 pygame.mixer.music.unload()
             except AttributeError:
                 # Fallback for older pygame versions if needed, though 2.6.1 has it
                 pass
        
        self.update_status("Idle")

    def speak_sync(self, text):
        asyncio.run(self.speak(text))

if __name__ == "__main__":
    # Test
    engine = AudioEngine()
    # text = engine.listen()
    # if text:
    #     engine.speak_sync(f"You said: {text}")
    engine.speak_sync("System initialized and ready.")
