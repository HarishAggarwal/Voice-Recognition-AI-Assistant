
import flet as ft
from audio_engine import AudioEngine
from brain import Brain
import threading
import time
import os
import asyncio

# Global references for cross-thread updates
page_ref = None
chat_col_ref = None
status_text_ref = None
status_circle_ref = None

# System Components
audio = None
brain = None

def get_status_color(status):
    status = status.lower()
    if "listening" in status:
        return "red400"
    elif "thinking" in status or "processing" in status:
        return "yellow400"
    elif "speaking" in status:
        return "green400"
    return "grey400"

def update_ui_status(status):
    global page_ref, status_text_ref, status_circle_ref
    if page_ref and status_text_ref:
        status_text_ref.value = status.upper()
        status_circle_ref.bgcolor = get_status_color(status)
        page_ref.update()

def add_chat_message(role, text):
    global page_ref, chat_col_ref
    if page_ref and chat_col_ref:
        align = ft.MainAxisAlignment.END if role == "You" else ft.MainAxisAlignment.START
        bg_color = "blueGrey900" if role == "You" else "grey800"
        
        chat_col_ref.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(f"{text}", color="white"),
                        padding=15,
                        bgcolor=bg_color,
                        border_radius=15,
                        width=400, # Max width constraint
                    )
                ],
                alignment=align
            )
        )
        page_ref.update()

def run_system_loop():
    """
    The background loop that runs Voice Recognition.
    """
    global audio, brain
    
    # Initialize connection
    try:
        audio = AudioEngine(status_callback=update_ui_status)
        brain = Brain()
        
        # Initial greeting
        audio.speak_sync("System online.")
        add_chat_message("Assistant", "System online.")
        
        while True:
            try:
                user_text = audio.listen()
                
                if user_text:
                    add_chat_message("You", user_text)
                    
                    if user_text.lower() in ["exit", "quit", "stop system"]:
                         audio.speak_sync("Goodbye.")
                         os._exit(0) # Force kill
                    
                    response_text = brain.process_input(user_text)
                    
                    if response_text:
                        add_chat_message("Assistant", response_text)
                        audio.speak_sync(response_text)
            
            except Exception as e:
                print(f"Loop Error: {e}")
                
    except Exception as e:
        print(f"Init Error: {e}")

def main(page: ft.Page):
    global page_ref, chat_col_ref, status_text_ref, status_circle_ref
    page_ref = page
    
    page.title = "Antigravity AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 500
    page.window_height = 800
    page.window_resizable = True
    page.padding = 20
    
    # Header
    status_circle_ref = ft.Container(
        width=15, height=15, border_radius=15, bgcolor="grey400",
        animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT)
    )
    status_text_ref = ft.Text("IDLE", size=12, weight=ft.FontWeight.BOLD, color="grey400")
    
    header = ft.Row(
        [
            ft.Text("ANTIGRAVITY", size=20, weight=ft.FontWeight.BOLD, color="white"),
            ft.Row([status_circle_ref, status_text_ref], spacing=10)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    
    # Chat Area
    chat_col_ref = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)
    
    chat_container = ft.Container(
        content=chat_col_ref,
        border=ft.border.all(1, "grey800"),
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color="black")
    )
    
    # Input Area (Optional manual override)
    def send_manual_message(e):
        if input_field.value:
            text = input_field.value
            input_field.value = ""
            add_chat_message("You", text)
            
            # Run in thread to not block UI
            def process():
                response = brain.process_input(text)
                add_chat_message("Assistant", response)
                audio.speak_sync(response)
            
            threading.Thread(target=process).start()
            page.update()

    input_field = ft.TextField(hint_text="Type a command...", expand=True, on_submit=send_manual_message, border_color="grey700")
    send_btn = ft.IconButton(icon="send", on_click=send_manual_message, icon_color="blue400")
    
    input_row = ft.Row([input_field, send_btn])

    # Add components
    page.add(header, ft.Divider(color="grey800"), chat_container, input_row)

    # Start Background Thread
    threading.Thread(target=run_system_loop, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)
