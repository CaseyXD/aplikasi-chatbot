from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import tkinter as tk
from tkinter import scrolledtext
import threading
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

# Fungsi untuk mengatur percakapan
class ChatBotApp:
    def __init__(self, root):
        self.context = ""
        self.root = root
        self.root.title("AI ChatBot")
        
        # Text area untuk menampilkan percakapan
        self.chat_area = tk.Text(root, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED, bg="white", font=("Arial", 12))
        self.chat_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Entry untuk input pengguna
        self.user_input = tk.Entry(root, width=50, font=("Arial", 12))
        self.user_input.grid(row=1, column=0, padx=10, pady=10)
        self.user_input.bind("<Return>", self.handle_enter)  # Menambahkan event handler untuk tombol Enter

        # Tombol untuk mengirimkan pesan
        self.send_button = tk.Button(root, text="Send", command=self.handle_input, font=("Arial", 12))
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Menambahkan tag warna untuk teks
        self.chat_area.tag_configure("you", foreground="blue", font=("Arial", 12, "bold"))
        self.chat_area.tag_configure("ai", foreground="green", font=("Arial", 12, "bold"))
        self.chat_area.tag_configure("message", foreground="black", font=("Arial", 12))

        # Label untuk loading
        self.loading_label = tk.Label(root, text="", font=("Arial", 12), fg="gray")
        self.loading_label.grid(row=2, column=0, columnspan=2)

    def handle_input(self):
        user_text = self.user_input.get().strip()
        if user_text:
            self.append_to_chat(f"You: {user_text}", "you")
            self.user_input.delete(0, tk.END)

            if user_text.lower() == "exit":
                self.root.quit()
            else:
                # Memulai thread untuk menangani loading dan respons
                threading.Thread(target=self.process_response, args=(user_text,)).start()

    def handle_enter(self, event):
        """Event handler untuk tombol Enter."""
        self.handle_input()

    def process_response(self, user_text):
        # Menampilkan simbol loading
        self.show_loading(True)
        ai_response = self.get_response(user_text)
        self.show_loading(False)
        self.append_to_chat(f"AI: {ai_response}", "ai")
        self.context += f"\nUser: {user_text}\nAI: {ai_response}\n"

    def show_loading(self, is_loading):
        """Menampilkan atau menyembunyikan simbol loading."""
        if is_loading:
            self.loading_label.config(text="Loading...")
            self.loading_label.update_idletasks()
        else:
            self.loading_label.config(text="")
            self.loading_label.update_idletasks()

    def get_response(self, question):
        time.sleep(2)  # Simulasi loading, hapus saat model asli digunakan
        result = chain.invoke({"context": self.context, "question": question})
        return result.strip()

    def append_to_chat(self, message, tag):
        self.chat_area.config(state=tk.NORMAL)
        name, text = message.split(":", 1)
        self.chat_area.insert(tk.END, name + ":", tag)  # Tambahkan nama dengan warna tertentu
        self.chat_area.insert(tk.END, text + "\n", "message")  # Tambahkan pesan dengan warna hitam
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
