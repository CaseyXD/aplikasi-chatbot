from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import tkinter as tk
from tkinter import scrolledtext

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
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED)
        self.chat_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Entry untuk input pengguna
        self.user_input = tk.Entry(root, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        # Tombol untuk mengirimkan pesan
        self.send_button = tk.Button(root, text="Send", command=self.handle_input)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

    def handle_input(self):
        user_text = self.user_input.get().strip()
        if user_text:
            self.append_to_chat(f"You: {user_text}")
            self.user_input.delete(0, tk.END)
            
            if user_text.lower() == "exit":
                self.root.quit()
            else:
                ai_response = self.get_response(user_text)
                self.append_to_chat(f"AI: {ai_response}")
                self.context += f"\nUser: {user_text}\nAI: {ai_response}\n"

    def get_response(self, question):
        result = chain.invoke({"context": self.context, "question": question})
        return result.strip()

    def append_to_chat(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
