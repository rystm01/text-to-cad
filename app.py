import tkinter as tk
from tkinter import ttk, scrolledtext
import shutil
from agent import Agent
from datetime import datetime
from PIL import Image, ImageTk

class OpenSCADGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenSCAD Generator")
        self.root.configure(padx=20, pady=20)
        self.agent = None
        self.photo = None
        self.image = None
        
        self._init_ui_components()
        self._setup_layout()
        self._init_agent()
        
    def _init_ui_components(self):
        """Initialize all UI components with improved styling"""
        # Create main frames for better organization
        self.input_frame = ttk.LabelFrame(self.root, text="Input", padding="10")
        self.output_frame = ttk.LabelFrame(self.root, text="Generated OpenSCAD Output Explanation", padding="10")
        self.iteration_frame = ttk.LabelFrame(self.root, text="Design Iteration", padding="10")

        # Model selection
        self.model_frame = ttk.Frame(self.input_frame)
        self.model_label = ttk.Label(self.model_frame, text="Model:")
        self.model_choice = ttk.Combobox(
            self.model_frame,
            values=["gpt-4o", "gpt-4o-mini", "o1-mini", "claude-3-5-sonnet-20241022"],
            width=30,
            state="readonly"
        )
        self.model_choice.current(0)
        
        # Text input area
        self.input_label = ttk.Label(self.input_frame, text="Enter your design description:")
        self.user_input = scrolledtext.ScrolledText(
            self.input_frame,
            width=50,
            height=5,
            wrap=tk.WORD
        )

        # Generate button
        self.generate_button = ttk.Button(
            self.input_frame,
            text="Generate & Preview",
            command=self._handle_generate
        )
        
        # Output area
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            width=50,
            height=10,
            wrap=tk.WORD,
            state='disabled'
        )
        
        # Iteration area
        self.iteration_label = ttk.Label(
            self.iteration_frame,
            text="Describe how you would like to improve or modify the design:"
        )
        self.iteration_prompt = scrolledtext.ScrolledText(
            self.iteration_frame,
            width=50,
            height=5,
            wrap=tk.WORD
        )
        self.iterate_button = ttk.Button(
            self.iteration_frame,
            text="Iterate on Design",
            command=self._handle_iterate
        )
        self.iteration_message = ttk.Label(self.iteration_frame)

    def _setup_layout(self):
        """Set up the layout with proper spacing and organization"""
        # Model selection layout
        self.model_frame.pack(fill=tk.X, pady=(0, 10))
        self.model_label.pack(side=tk.LEFT)
        self.model_choice.pack(side=tk.LEFT, padx=(10, 0))
        
        # Input section layout
        self.input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.input_label.pack(anchor=tk.W, pady=(0, 5))
        self.user_input.pack(fill=tk.BOTH, expand=True)
        self.generate_button.pack(pady=(10, 0))
        
        # Output section layout
        self.output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Iteration section layout
        self.iteration_frame.pack(fill=tk.BOTH, expand=True)
        self.iteration_label.pack(anchor=tk.W, pady=(0, 5))
        self.iteration_prompt.pack(fill=tk.BOTH, expand=True)
        self.iterate_button.pack(pady=(10, 0))
        self.iteration_message.pack(pady=(5, 0))

    def _init_agent(self):
        """Initialize the agent with selected model"""
        self.agent = Agent(self.model_choice.get())

    def _handle_generate(self):
        """Handle generate button click"""
        self.agent.set_model(self.model_choice.get())
        user_text = self.user_input.get("1.0", tk.END).strip()
        self.agent.generate(user_text)
        
        # Update output text
        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, self.agent.explanations[-1] + "\n")
        self.output_text.configure(state='disabled')

    def _handle_iterate(self):
        """Handle iteration button click"""
        self.agent.set_model(self.model_choice.get())
        prompt = self.iteration_prompt.get("1.0", tk.END).strip()
        self.agent.iterate(prompt, self.image)
        
        # Update output text
        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, self.agent.explanations[-1] + "\n")
        self.output_text.configure(state='disabled')

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