
import os
import sys
from dotenv import load_dotenv

# Ensure the src directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src import gui

if __name__ == "__main__":
    load_dotenv()
    # Check for API Key
    if not os.getenv("GOOGLE_API_KEY"):
        print("CRITICAL ERROR: GOOGLE_API_KEY is missing from .env file.")
        print("Please create a .env file and add your Google API Key.")
    
    # Run the Flet App
    # We call flet app target directly in gui.py's if main, 
    # but here we can invoke it.
    import flet as ft
    ft.app(target=gui.main)
