import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from openai import OpenAI
import subprocess
import os
import re
import sys




def extract_code_blocks(text):
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)\n```", text, re.DOTALL)
    return code_blocks

# Set your OpenAI API key
# Function to generate OpenSCAD code using ChatGPT
def generate_openscad_code():
    prompt = user_input.get("1.0", tk.END).strip()
    
    if not prompt:
        output_text.insert(tk.END, "Please enter a description.\n")
        return
    
    output_text.insert(tk.END, "Generating OpenSCAD code...\n")
    client = OpenAI()

    messages = [{"role" : "system", "content" : "You are a part of an english to CAD AI application. \
                  You write openSCAD code."}]
    try:
        messages.append({"role": "user", "content": f"Write OpenSCAD code for: {prompt}"})
        # Query ChatGPT for OpenSCAD code
        response = client.chat.completions.create(
            model=model_choice.get(),
            messages=messages,
        )

        output = response.choices[0].message.content
        scad_code = extract_code_blocks(output)[0]
        # scad_code.replace("openscad")
        output.replace(scad_code, "")

        
        # Display the code
        output_text.insert(tk.END, output + "\n")
        
        # Save to a file
        print(scad_code)
        print(output_text)
        with open("generated.scad", "w") as f:
            f.write(scad_code)

        # Open OpenSCAD for preview
        subprocess.run(["openscad", "scad_files\generated.scad"])

    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}\n")


# GUI setup
root = tk.Tk()
root.title("OpenSCAD Generator")

tk.Label(root, text="Choose a model:").pack()
model_choice = ttk.Combobox(values=["gpt-4o", "gpt-4o-mini", "o1-mini"])
model_choice.current(0)
model_choice.pack()
tk.Label(root, text="Enter description:").pack()
user_input = scrolledtext.ScrolledText(root, width=50, height=5)
user_input.pack()

generate_button = tk.Button(root, text="Generate & Preview", command=generate_openscad_code)
generate_button.pack()

output_text = scrolledtext.ScrolledText(root, width=50, height=10)
output_text.pack()

root.mainloop()
