import tkinter as tk
from tkinter import ttk, scrolledtext, font
import shutil
from agent import Agent
from datetime import datetime
from PIL import Image, ImageTk

class OpenSCADGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenSCAD Generator Chat")
        self.root.configure(bg='#f0f2f5')
        self.root.geometry("800x600")
        
        # Configure custom styles
        self._configure_styles()
        
        self.agent = None
        self.photo = None
        self.image = None
        
        self._init_ui_components()
        self._setup_layout()
        self._init_agent()
        
    def _configure_styles(self):
        """Configure custom ttk styles"""
        # Create custom font
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
        
        style = ttk.Style()
        style.configure('Chat.TFrame', background='#f0f2f5')
        style.configure('Settings.TFrame', background='#ffffff', relief='flat')
        
        # Custom combobox style
        style.configure('Custom.TCombobox',
                       fieldbackground='#ffffff',
                       background='#ffffff',
                       arrowcolor='#1a73e8')
                       
        # Custom button style
        style.configure('Send.TButton',
                       background='#1a73e8',
                       foreground='#0d0a0a',
                       padding=(15, 8))
        
        # Custom label style
        style.configure('Custom.TLabel',
                       background='#ffffff',
                       font=('Segoe UI', 10))

    def _init_ui_components(self):
        """Initialize all UI components with improved styling"""
        # Create main container
        self.main_container = ttk.Frame(self.root, style='Chat.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Settings panel with modern look
        self.settings_frame = ttk.Frame(self.main_container, style='Settings.TFrame')
        self.settings_frame.pack(fill=tk.X, pady=(0, 10), ipady=10, ipadx=10)
        self.settings_frame.configure(relief='ridge', borderwidth=1)
        
        # Model selection with improved styling
        self.model_label = ttk.Label(
            self.settings_frame,
            text="Model:",
            style='Custom.TLabel'
        )
        self.model_choice = ttk.Combobox(
            self.settings_frame,
            values=["gpt-4o", "gpt-4o-mini", "o1-mini", "claude-3-5-sonnet-20241022"],
            width=30,
            state="readonly",
            style='Custom.TCombobox'
        )
        self.model_choice.current(0)
        
        # Chat container with modern styling
        self.chat_container = ttk.Frame(self.main_container, style='Chat.TFrame')
        self.chat_container.pack(fill=tk.BOTH, expand=True)
        
        # Chat history with custom colors and fonts
        self.chat_history = scrolledtext.ScrolledText(
            self.chat_container,
            width=60,
            height=20,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            state='disabled',
            background='#ffffff',
            borderwidth=1,
            relief='solid'
        )
        
        # Input area with modern styling
        self.input_frame = ttk.Frame(self.chat_container, style='Chat.TFrame')
        self.message_input = scrolledtext.ScrolledText(
            self.input_frame,
            width=50,
            height=3,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            background='#ffffff',
            borderwidth=1,
            relief='solid'
        )
        
        # Modern send button
        self.send_button = ttk.Button(
            self.input_frame,
            text="Send",
            style='Send.TButton',
            command=self._handle_send_message
        )
        
        # Bind Enter key
        self.message_input.bind('<Return>', lambda e: self._handle_send_message())
        self.message_input.bind('<Shift-Return>', lambda e: 'break')

    def _setup_layout(self):
        """Set up the layout with proper spacing and modern organization"""
        # Settings layout
        self.model_label.pack(side=tk.LEFT, padx=(10, 5))
        self.model_choice.pack(side=tk.LEFT, padx=(0, 10))
        
        # Chat history layout
        self.chat_history.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input area layout
        self.input_frame.pack(fill=tk.X)
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.send_button.pack(side=tk.RIGHT, fill=tk.Y)

    def _format_message(self, sender, message):
        """Format chat messages with distinct styling"""
        self.chat_history.configure(state='normal')
        
        # Add sender with distinct styling
        if sender == "You":
            self.chat_history.insert(tk.END, f"{sender}: ", "user")
            self.chat_history.tag_configure("user", foreground="#1a73e8", font=('Segoe UI', 10, 'bold'))
        else:
            self.chat_history.insert(tk.END, f"{sender}: ", "assistant")
            self.chat_history.tag_configure("assistant", foreground="#188038", font=('Segoe UI', 10, 'bold'))
        
        # Add message
        self.chat_history.insert(tk.END, f"{message}\n\n", "message")
        self.chat_history.tag_configure("message", font=('Segoe UI', 10))
        
        self.chat_history.see(tk.END)
        self.chat_history.configure(state='disabled')

    def _init_agent(self):
        """Initialize the agent with selected model"""
        self.agent = Agent(self.model_choice.get())
        self._format_message("Assistant", "Hello! I'm your OpenSCAD design assistant. Describe what you'd like to create, and I'll help generate the OpenSCAD code. You can also ask me to modify or improve existing designs.")

    def _handle_send_message(self):
        """Handle sending a message"""
        message = self.message_input.get("1.0", tk.END).strip()
        if not message:
            return 'break'
            
        # Clear input
        self.message_input.delete("1.0", tk.END)
        
        # Add user message to chat
        self._format_message("You", message)
        
        # Process message
        self.agent.set_model(self.model_choice.get())
        
        # If this is the first design request, generate new design
        if not self.agent.explanations:
            self.agent.generate(message)
        # Otherwise, iterate on existing design
        else:
            self.agent.iterate(message, self.image)
            
        # Add assistant's response to chat
        self._format_message("Assistant", self.agent.explanations[-1])
        
        return 'break'

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