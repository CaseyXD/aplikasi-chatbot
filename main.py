from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import tkinter as tk
import requests
import threading
import os
import time

# Template untuk prompt
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

# Inisialisasi model dan chain
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


class ChatBotApp:
    def __init__(self, root):
        self.context = ""
        self.history_file = "history.txt"
        self.root = root
        self.root.title("AI ChatBot")

        # Area percakapan
        self.chat_area = tk.Text(root, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED, bg="white", font=("Arial", 12))
        self.chat_area.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Input pengguna
        self.user_input = tk.Entry(root, width=50, font=("Arial", 12))
        self.user_input.grid(row=1, column=0, padx=10, pady=10)
        self.user_input.bind("<Return>", self.handle_enter)

        # Tombol kirim pesan
        self.send_button = tk.Button(root, text="Send", command=self.handle_input, font=("Arial", 12))
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Tombol history
        self.history_button = tk.Button(root, text="History", command=self.show_history, font=("Arial", 12))
        self.history_button.grid(row=1, column=2, padx=10, pady=10)

        # Tombol clear history
        self.clear_button = tk.Button(root, text="Clear History", command=self.clear_history, font=("Arial", 12), fg="red")
        self.clear_button.grid(row=2, column=0, columnspan=3)

        # Label loading
        self.loading_label = tk.Label(root, text="", font=("Arial", 12), fg="gray")
        self.loading_label.grid(row=3, column=0, columnspan=3)

        # Tag warna untuk chat
        self.chat_area.tag_configure("you", foreground="blue", font=("Arial", 12, "bold"))
        self.chat_area.tag_configure("ai", foreground="green", font=("Arial", 12, "bold"))
        self.chat_area.tag_configure("message", foreground="black", font=("Arial", 12))

    def handle_input(self):
        user_text = self.user_input.get().strip()
        if user_text:
            self.append_to_chat(f"You: {user_text}", "you")
            self.user_input.delete(0, tk.END)

            if user_text.lower() == "exit":
                self.root.quit()
            else:
                threading.Thread(target=self.process_response, args=(user_text,)).start()

    def handle_enter(self, event):
        self.handle_input()

    def process_response(self, user_text):
        self.show_loading(True)

        if "map" in user_text.lower() or "location" in user_text.lower():
            ai_response = self.get_location_info(user_text)
        else:
            ai_response = self.get_response(user_text)

        self.show_loading(False)
        self.append_to_chat(f"AI: {ai_response}", "ai")
        self.context += f"\nUser: {user_text}\nAI: {ai_response}\n"
        self.save_to_history(f"You: {user_text}\nAI: {ai_response}\n")

    def show_loading(self, is_loading):
        if is_loading:
            self.loading_label.config(text="Loading...")
        else:
            self.loading_label.config(text="")

    def get_response(self, question):
        time.sleep(2)  # Simulasi delay
        result = chain.invoke({"context": self.context, "question": question})
        return result.strip()

    def get_location_info(self, query):
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json",
            "addressdetails": 1,
            "limit": 1,
        }
        headers = {
            "User-Agent": "CaseyXD/1.0 (wilhelm.ezael@deallabs.org)"  # Tambahkan User-Agent
        }

        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data:
                location = data[0]
                display_name = location.get("display_name", "Unknown location")
                lat = location.get("lat", "Unknown latitude")
                lon = location.get("lon", "Unknown longitude")
                return f"Location found: {display_name} (Latitude: {lat}, Longitude: {lon})"
            else:
                return "Sorry, I couldn't find any information for that location."
        except Exception as e:
            return f"Error fetching location: {e}"

    def append_to_chat(self, message, tag):
        self.chat_area.config(state=tk.NORMAL)
        name, text = message.split(":", 1)
        self.chat_area.insert(tk.END, name + ":", tag)
        self.chat_area.insert(tk.END, text + "\n", "message")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def save_to_history(self, conversation):
        with open(self.history_file, "a") as file:
            file.write(conversation)

    def show_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                history = file.read()
            self.display_popup("Chat History", history)
        else:
            self.display_popup("Chat History", "No history found.")

    def clear_history(self):
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
            self.display_popup("Clear History", "History has been cleared!")
        else:
            self.display_popup("Clear History", "No history found to clear.")

    def display_popup(self, title, content):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("500x400")

        content_text = tk.Text(popup, wrap=tk.WORD, bg="white", font=("Arial", 12))
        content_text.insert(tk.END, content)
        content_text.config(state=tk.DISABLED)
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
