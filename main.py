
import os
import asyncio
import sys
from dotenv import load_dotenv

# Ensure the src directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.audio_engine import AudioEngine
from src.brain import Brain

def main():
    # Load environment variables
    load_dotenv()
    
    # Check for API Key
    if not os.getenv("GOOGLE_API_KEY"):
        print("CRITICAL ERROR: GOOGLE_API_KEY is missing from .env file.")
        print("Please create a .env file and add your Google API Key.")
        print("Example: GOOGLE_API_KEY=AIzaSy...")
        return

    print("Initializing System...")
    
    try:
        audio = AudioEngine()
        brain = Brain()
    except Exception as e:
        print(f"Initialization Failed: {e}")
        return

    print("\n--- Voice Recognition System Online ---")
    print("Speak now. Say 'Exit' or 'Quit' to stop.")

    # Initial Greeting
    audio.speak_sync("System online. How can I help you today?")

    while True:
        try:
            # 1. Listen
            user_text = audio.listen()
            
            if user_text:
                # Check for exit command
                if user_text.lower() in ["exit", "quit", "stop system", "terminate"]:
                    audio.speak_sync("Shutting down. Goodbye.")
                    break
                
                # 2. Think & Act
                response_text = brain.process_input(user_text)
                
                # 3. Speak
                if response_text:
                    audio.speak_sync(response_text)
            
            # Optional: Add a small delay if loop is too tight, 
            # but audio.listen() already has a pause.
            
        except KeyboardInterrupt:
            print("\nForce Exit.")
            break
        except Exception as e:
            print(f"Main Loop Error: {e}")
            audio.speak_sync("I encountered an error.")

if __name__ == "__main__":
    main()
