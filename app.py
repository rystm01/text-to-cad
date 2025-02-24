import tkinter as tk
from tkinter import ttk, scrolledtext
import shutil
from agent import Agent
from datetime import datetime
from PIL import Image, ImageTk

class OpenSCADGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenSCAD Generator Chat")
        self.root.configure(padx=20, pady=20)
        self.agent = None
        self.photo = None
        self.image = None
        
        self._init_ui_components()
        self._setup_layout()
        self._init_agent()
        
    def _init_ui_components(self):
        """Initialize all UI components with improved styling"""
        # Create main frames
        self.settings_frame = ttk.Frame(self.root, padding="5")
        self.chat_frame = ttk.LabelFrame(self.root, text="Chat", padding="10")
        
        # Model selection
        self.model_label = ttk.Label(self.settings_frame, text="Model:")
        self.model_choice = ttk.Combobox(
            self.settings_frame,
            values=["gpt-4o", "gpt-4o-mini", "o1-mini", "claude-3-5-sonnet-20241022"],
            width=30,
            state="readonly"
        )
        self.model_choice.current(0)
        
        # Chat history area
        self.chat_history = scrolledtext.ScrolledText(
            self.chat_frame,
            width=60,
            height=20,
            wrap=tk.WORD,
            state='disabled'
        )
        
        # Message input area
        self.input_frame = ttk.Frame(self.chat_frame)
        self.message_input = scrolledtext.ScrolledText(
            self.input_frame,
            width=50,
            height=3,
            wrap=tk.WORD
        )
        self.send_button = ttk.Button(
            self.input_frame,
            text="Send",
            command=self._handle_send_message
        )
        
        # Bind Enter key to send message
        self.message_input.bind('<Return>', lambda e: self._handle_send_message())
        self.message_input.bind('<Shift-Return>', lambda e: 'break')  # Allow new lines with Shift+Enter

    def _setup_layout(self):
        """Set up the layout with proper spacing and organization"""
        # Settings layout
        self.settings_frame.pack(fill=tk.X, pady=(0, 10))
        self.model_label.pack(side=tk.LEFT, padx=(0, 5))
        self.model_choice.pack(side=tk.LEFT)
        
        # Chat frame layout
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        self.chat_history.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input area layout
        self.input_frame.pack(fill=tk.X)
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.send_button.pack(side=tk.RIGHT, fill=tk.Y)

    def _init_agent(self):
        """Initialize the agent with selected model"""
        self.agent = Agent(self.model_choice.get())
        self._append_to_chat("Assistant: Hello! I'm your OpenSCAD design assistant. Describe what you'd like to create, and I'll help generate the OpenSCAD code. You can also ask me to modify or improve existing designs.\n")

    def _append_to_chat(self, message):
        """Append a message to the chat history"""
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.see(tk.END)
        self.chat_history.configure(state='disabled')

    def _handle_send_message(self):
        """Handle sending a message"""
        message = self.message_input.get("1.0", tk.END).strip()
        if not message:
            return 'break'
            
        # Clear input
        self.message_input.delete("1.0", tk.END)
        
        # Add user message to chat
        self._append_to_chat(f"You: {message}")
        
        # Process message
        self.agent.set_model(self.model_choice.get())
        
        # If this is the first design request, generate new design
        if not self.agent.explanations:
            self.agent.generate(message)
        # Otherwise, iterate on existing design
        else:
            self.agent.iterate(message, self.image)
            
        # Add assistant's response to chat
        self._append_to_chat(f"Assistant: {self.agent.explanations[-1]}")
        
        return 'break'  # Prevent default Enter key behavior

    def _handle_closing(self):
        """Handle window closing"""
        time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        
        for i in range(self.agent.num_iter):
            source = f"scad_files/generated{i}.scad"
            dest = f"past_creations/{time}{i}.scad"
            shutil.move(source, dest)
            
        self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self._handle_closing)
        self.root.mainloop()

if __name__ == "__main__":
    app = OpenSCADGeneratorGUI()
    app.run()