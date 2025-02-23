import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog

import shutil
from agent import Agent
from datetime import datetime
from PIL import Image, ImageTk

class OpenSCADGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenSCAD Generator")
        self.agent = None
        self.photo = None  # Keep reference to prevent garbage collection
        self.image = None
        
        self._init_ui_components()
        self._setup_layout()
        self._init_agent()
        
    def _init_ui_components(self):
        """Initialize all UI components"""
        # Model selection
        self.model_label = tk.Label(self.root, text="Choose a model:")
        self.model_choice = ttk.Combobox(
            self.root,
            values=["gpt-4o", "gpt-4o-mini", "o1-mini", "claude-3-5-sonnet-20241022"]
        )
        self.model_choice.current(0)
        
        # Text input area
        self.input_label = tk.Label(self.root, text="Enter description:")
        self.user_input = scrolledtext.ScrolledText(self.root, width=50, height=5)

        self.iteration_label = tk.Label(self.root, text="Enter how you would like to improve/change:")
        self.iteration_prompt = scrolledtext.ScrolledText(self.root, width=50, height=5)
        self.iteration_message = tk.Label(self.root)
        
        # Buttons
        self.generate_button = tk.Button(
            self.root,
            text="Generate & Preview",
            command=self._handle_generate
        )
        self.upload_button = tk.Button(
            self.root,
            text="Upload Image of Preview",
            command=self._handle_upload
        )
        self.iterate_button = tk.Button(
            self.root,
            text="Iterate on Design",
            command=self._handle_iterate
        )
        
        # Display areas
        self.image_label = tk.Label(self.root)
        self.status_label = tk.Label(self.root)
        self.output_text = scrolledtext.ScrolledText(self.root, width=50, height=10)

    def _setup_layout(self):
        """Set up the layout of UI components"""
        components = [
            self.model_label,
            self.model_choice,
            self.input_label,
            self.user_input,
            self.generate_button,
            self.upload_button,
            self.iteration_prompt,
            self.iterate_button,
            self.iteration_message,
            self.image_label,
            self.output_text
        ]
        
        for component in components:
            component.pack()

    def _init_agent(self):
        """Initialize the agent with selected model"""
        self.agent = Agent(self.model_choice.get())

    def _handle_generate(self):
        """Handle generate button click"""
        print("setting agent to ")
        print(self.model_choice.get())
        self.agent.set_model(self.model_choice.get())
        user_text = self.user_input.get("1.0", tk.END).strip()
        self.agent.generate(user_text)
        self.output_text.insert(tk.END, self.agent.explanations[-1] + "\n")

    def _handle_upload(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        
        if not file_path:
            return
            
        try:
            self.image = Image.open(file_path)
            self.image.thumbnail((300, 300))  # Resize image
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def _handle_iterate(self):
        """Handle iteration button click"""
        # Implementation for iteration logic
        self.agent.set_model(self.model_choice.get())
        prompt = self.iteration_prompt.get("1.0", tk.END).strip()
        # if not self.photo and prompt == "":
        #     self.iteration_message.config(text="Please enter an Image or a prompt on how to improve the design")
        self.agent.iterate(prompt, self.image)
        self.output_text.insert(tk.END, self.agent.explanations[-1] + "\n")

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