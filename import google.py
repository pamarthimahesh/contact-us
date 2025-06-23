import google.generativeai as genai  # pip install google-generativeai
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr

# Configure Gemini API
api_data = "AIzaSyCKbkPOKz9hqy_N_s3-3T44-umq5lS9qE4"
genai.configure(api_key=api_data)

# Load Gemini model
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Function to recognize voice
def recognize_voice():
    try:
        with sr.Microphone() as source:
            conversation_area.insert(tk.END, "🎙 Listening...\n", "bot")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            user_input.delete(0, tk.END)
            user_input.insert(0, text)
            send_query()  # Automatically send the voice text
    except sr.UnknownValueError:
        conversation_area.insert(tk.END, "😕 Could not understand audio.\n", "bot")
    except sr.RequestError:
        conversation_area.insert(tk.END, "⚠ Could not request results.\n", "bot")

# Generate response using Gemini
def generate_response(query):
    try:
        response = gemini_model.generate_content(
            query,
            generation_config=genai.GenerationConfig(
                max_output_tokens=75,
                temperature=0.1,
            )
        )
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"

# On Send button click
def send_query():
    query = user_input.get()
    if not query.strip():
        return
    conversation_area.insert(tk.END, f"You: {query}\n", "user")
    user_input.delete(0, tk.END)

    response = generate_response(query)
    conversation_area.insert(tk.END, f"MAHI: {response}\n", "bot")
    conversation_area.see(tk.END)

# Set up main GUI window
root = tk.Tk()
root.title("💬 MAHI Chatbot")
root.configure(bg="#1e1e1e")
root.geometry("550x550")

# Chat area
conversation_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    width=70,
    height=20,
    font=("Consolas", 12),
    bg="#2e2e2e",
    fg="#f0f0f0",
    insertbackground="white"
)
conversation_area.pack(padx=10, pady=10)
conversation_area.tag_config("user", foreground="#00bfff", font=("Consolas", 12, "bold"))
conversation_area.tag_config("bot", foreground="#7CFC00", font=("Consolas", 12, "bold"))

# Input area
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

user_input = tk.Entry(
    input_frame,
    font=("Consolas", 12),
    width=30,
    bg="#3c3c3c",
    fg="white",
    insertbackground="white",
    borderwidth=2,
    relief=tk.FLAT
)
user_input.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Consolas", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    padx=10,
    pady=5,
    relief=tk.FLAT,
    command=send_query
)
send_button.pack(side=tk.LEFT)

voice_button = tk.Button(
    input_frame,
    text="🎙 Speak",
    font=("Consolas", 12, "bold"),
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    padx=10,
    pady=5,
    relief=tk.FLAT,
    command=recognize_voice
)
voice_button.pack(side=tk.LEFT)

# Run the application
root.mainloop()