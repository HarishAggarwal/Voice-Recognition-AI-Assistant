# Antigravity AI - Voice Activated Desktop Assistant

Antigravity AI is a powerful, highly interactive voice assistant for Windows. It combines **Google's Gemini LLM** for human-like intelligence with **low-level system controls** (mouse, keyboard, app management) to allow you to control your computer completely hands-free.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flet](https://img.shields.io/badge/UI-Flet-purple)
![Gemini](https://img.shields.io/badge/AI-Gemini%201.5-orange)

## ✨ Features

- **🗣️ Natural Conversation**: Powered by Google Gemini, it understands context, nuance, and humor.
- **🖥️ Deep App Interaction**:
  - **Keyboard**: Typing, Hotkeys (Ctrl+C, Alt+Tab, etc.).
  - **Mouse**: Moving, Clicking, Scrolling.
  - **App launching**: Opens any application on your system.
- **🎨 Modern UI**: Built with Flet, featuring a dark-mode chat interface and real-time status visualization (Listening/Thinking/Speaking).
- **🔊 Natural Voice**: Uses Microsoft Edge's Neural TTS for high-quality speech output.
- **🛡️ Robustness**: Handles API rate limits gracefully with automatic retries.

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher.
- A [Google Cloud API Key](https://aistudio.google.com/) (Free tier available).

### Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/antigravity-ai.git
    cd antigravity-ai
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    - Create a file named `.env` in the root directory.
    - Add your API Key:
      ```env
      GOOGLE_API_KEY=AIzaSyYourKeyHere...
      ```

## 🎮 Usage

### Running the GUI (Recommended)
Launch the modern desktop interface:
```bash
python app.py
```

### Running in Console Mode
For a lightweight, terminal-only experience:
```bash
python main.py
```

### Building the Executable (Windows)
To create a standalone `.exe` file:
```bash
flet pack app.py --name AntigravityAI
```
The output will be in the `dist/` folder.

## 🗣️ Voice Commands Example

- **General**: "Who are you?", "Tell me a fun fact."
- **Browser**: "Search Google for Python tutorials", "Scroll down", "Click the first link."
- **Productivity**: "Open Notepad, type a meeting note, and save it."
- **System**: "Turn the volume up", "Switch windows", "Close this app."

## 📂 Project Structure

```
├── .env                # API Keys (Not committed)
├── .gitignore          # Git exclusion rules
├── app.py              # Main Entry Point (GUI)
├── main.py             # Console Entry Point
├── requirements.txt    # Python Dependencies
├── build_exe.bat       # Script to build .exe
├── src/                # Source Code
│   ├── actions.py      # System Control Tools (Mouse/Keyboard)
│   ├── audio_engine.py # STT and TTS Logic
│   ├── brain.py        # Gemini LLM Integration
│   └── gui.py          # Flet UI Implementation
└── dist/               # Built Executables
```

## 📄 License
MIT License.
