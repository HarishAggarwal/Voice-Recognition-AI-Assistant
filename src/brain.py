
import os
import google.generativeai as genai
from dotenv import load_dotenv
from src import actions

# Load environment variables
load_dotenv()

class Brain:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("WARNING: GOOGLE_API_KEY not found in environment variables.")
            # We will handle this gracefully in the main loop or here
            
        if api_key:
            genai.configure(api_key=api_key)
            
            # defined tools
            self.tools = actions.tools_list
            
            # Dynamic Model Selection
            model_name = 'gemini-1.5-flash' # Default preference
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # Preferences
                preferences = [
                    'models/gemini-1.5-flash',
                    'models/gemini-1.5-flash-latest',
                    'models/gemini-1.5-pro',
                    'models/gemini-1.5-pro-latest',
                    'models/gemini-pro',
                    'models/gemini-1.0-pro'
                ]
                
                selected_model = None
                for pref in preferences:
                    if pref in available_models:
                        selected_model = pref
                        break
                
                if not selected_model and available_models:
                    # Fallback to the first available one if none of our preferences match
                    selected_model = available_models[0]
                    
                if selected_model:
                    print(f"Selected Brain Model: {selected_model}")
                    model_name = selected_model
                else:
                    print("Warning: No suitable models found in list. Trying default.")
                    
            except Exception as e:
                print(f"Model list failed, using default: {e}")

            # Create the model with tools
            self.model = genai.GenerativeModel(
                model_name=model_name,
                tools=self.tools,
                system_instruction="""
                You are a highly intelligent, witty, and capable AI assistant named 'Antigravity' living on the user's Windows laptop.
                Your personality is human-like, slightly casual but professional, and very helpful.
                You are not just a text bot; you can control the computer.
                
                When the user asks you to do something that corresponds to a tool (like opening an app, searching, typing), USE THE TOOL.
                
                **Application Interaction Strategy:**
                You can interact with ANY application by simulating user actions.
                - **To send a message**: Open functionality (e.g. Type to search start menu or use run command if known), then use `type_text` to type the message, then `press_key('enter')` to send.
                - **To save a file**: Use `hotkey('ctrl+s')`.
                - **To Switch windows**: Use `hotkey('alt+tab')`.
                - **To Close window**: Use `hotkey('alt+f4')`.
                - **To Scroll**: Use `scroll(-500)` to scroll down, `scroll(500)` to scroll up.
                - **To Click**: If you need to focus or click something, use `mouse_click('left')`.
                - **To Navigate (e.g. 2nd URL)**: Since you cannot see, use `press_key('tab')` multiple times to move focus, then `press_key('enter')`. Or ask the user to position the mouse and say "Click".
                
                If the user asks for something vague like "Message mom on WhatsApp", you might need to:
                1. Open WhatsApp (try searching start menu or opening web).
                2. Wait (simulated by separate steps or just assuming loading).
                3. Type "Mom".
                4. Press Enter.
                5. Type the message.
                6. Press Enter.
                
                If the user just wants to chat, reply conversationally.
                Keep your responses concise and spoken-style, as they will be read out loud (TTS). Avoid long lists or markdown formatting in your speech unless necessary.
                If you execute a tool, acknowledge it briefly (e.g., "On it.", "Opening Notepad now.", "Searching for that.").
                """
            )
            self.chat_session = self.model.start_chat(enable_automatic_function_calling=True)
        else:
            self.model = None
            self.chat_session = None

    def process_input(self, user_text):
        """
        Sends text to the LLM and gets the response (text and/or action execution).
        """
        if not self.chat_session:
            return "I need a Google API Key to function properly. Please check your .env file."

        retries = 3
        delay = 2
        
        for attempt in range(retries):
            try:
                # Send message. Automatic function calling handles the tool execution
                response = self.chat_session.send_message(user_text)
                return response.text
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower():
                    print(f"Rate Limit Hit (Attempt {attempt+1}/{retries}). Waiting {delay}s...")
                    import time
                    time.sleep(delay)
                    delay *= 2 # Exponential backoff
                else:
                    return f"My brain hurts. Something went wrong: {e}"
        
        return "I'm feeling a bit overwhelmed (Rate Limited). Please give me a moment."

if __name__ == "__main__":
    # Test
    brain = Brain()
    if brain.model:
        print(brain.process_input("Hello, who are you?"))
