import tkinter as tk
from tkinter import scrolledtext
from chatbot_engine import chatbot_response  # Import the chatbot logic

# Create the main window
root = tk.Tk()
root.title("India State Info Chatbot")
root.geometry("600x500")
root.configure(bg="#f0f8ff")

# Title Label
title = tk.Label(root, text="🌏 India State Info Chatbot", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#004080")
title.pack(pady=10)

# Chat Display Area
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), width=70, height=20, state='disabled')
chat_display.pack(padx=10, pady=10)

# Entry field for user input
user_input = tk.Entry(root, font=("Arial", 12), width=60)
user_input.pack(padx=10, pady=5)

# Function to handle user input
def send_message():
    message = user_input.get()
    if message.strip() == "":
        return

    # Display user message
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"You: {message}\n")
    chat_display.configure(state='disabled')

    # Get bot response
    response = chatbot_response(message)

    # Display bot response
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, f"Bot: {response}\n\n")
    chat_display.configure(state='disabled')

    user_input.delete(0, tk.END)
    chat_display.see(tk.END)  # Scroll to latest message

# Send Button
send_button = tk.Button(root, text="Ask", command=send_message, font=("Arial", 12), bg="#004080", fg="white")
send_button.pack(pady=5)

# Run the application
root.mainloop()
