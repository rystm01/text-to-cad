import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from openai import OpenAI
import subprocess
import os
import re
import sys
import shutil
from agent import Agent
from datetime import datetime
from PIL import Image, ImageTk


def generate_on_click():
  agent.generate(user_input.get("1.0", tk.END).strip())
  output_text.insert(tk.END, agent.explanations[-1] + "\n")

def upload_on_click():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        try:
            image = Image.open(file_path)
            image.thumbnail((300, 300))  # Resize image to fit in the window
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
            status_label.config(text=f"Image loaded: {file_path}")
        except Exception as e:
            status_label.config(text=f"Error: {e}")


def on_closing():
  """
  Move files 
  """
  for i in range(agent.num_iter):
    time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    print(time)
    shutil.move(f"scad_files/generated{i}.scad", f"past_creations/{time}{i}.scad")
  root.destroy()
      
# GUI setup
root = tk.Tk()
root.title("OpenSCAD Generator")

tk.Label(root, text="Choose a model:").pack()
model_choice = ttk.Combobox(values=["gpt-4o", "gpt-4o-mini", "o1-mini", "claude-3-5-sonnet-20241022"])
model_choice.current(0)
model_choice.pack()
tk.Label(root, text="Enter description:").pack()
user_input = scrolledtext.ScrolledText(root, width=50, height=5)
user_input.pack()

agent = Agent(model_choice.get())

generate_button = tk.Button(root, text="Generate & Preview", command=generate_on_click)
generate_button.pack()

upload_button = tk.Button(root, text="Upload Image of Preview", command=upload_on_click)
image_label = tk.Label(root)
status_label = tk.Label(root)
iterate_button = tk.Button(root, text="Iterate on Design", command=iterate_on_click)


iterate_button.pack()
image_label.pack()
status_label.pack()

output_text = scrolledtext.ScrolledText(root, width=50, height=10)
output_text.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
