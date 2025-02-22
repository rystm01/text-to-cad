
from openai import OpenAI
from anthropic import Anthropic
import subprocess
import re
import signal
import base64
from io import BytesIO






class Agent:
  openai_models = ["gpt-4o", "gpt-4o-mini", "o1-mini"]
  anthropic_models = [ "claude-3-5-sonnet-20241022"]
  xai_models = []
  def __init__(self, model, api_key=""):
    models = ["gpt-4o", "gpt-4o-mini", "o1-mini", "claude-3-5-sonnet-20241022"]
    if model not in models:
      raise ValueError("not a valid model")
    self.model = model

    self.messages = []
    if(model != "o1-mini"):
      self.messages.append({"role" : "system", "content" : "You are a part of an english to CAD AI application. \
                    You write openSCAD code."})

    if model in Agent.openai_models:
      self.client = OpenAI()
    elif model in Agent.anthropic_models:
      self.client = Anthropic()
    elif model in Agent.xai_models:
      self.client = OpenAI(
        api_key="an api key",
        base_url="https://api.x.ai/v1"
      )
    
    self.explanations = []
    self.scad_codes = []
    self.num_iter = 0
    self.cad_process = None

  def set_model(self, model):
    self.model = model

    if model in Agent.openai_models:
      if(model == 'o1-mini'):
        self.messages.pop(0)
      self.client = OpenAI()
    elif model in Agent.anthropic_models:
      self.client = Anthropic()
    elif model in Agent.xai_models:
      self.client = OpenAI(
        api_key="an api key",
        base_url="https://api.x.ai/v1"
      )
    
  
    
  def generate(self, prompt):
    # prompt = user_input.get("1.0", tk.END).strip()

    self.messages.append({"role" : "user", "content" : prompt})
    if not prompt:
      return "Please enter a description.\n"

    try:
      if self.model in Agent.openai_models+Agent.xai_models:
        response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
        )
        output = response.choices[0].message.content

      elif self.model in Agent.anthropic_models:
        print(self.messages[0])
        print(self.messages[1:])
        response = self.client.messages.create(
          model=self.model,
          max_tokens=2048,
          system=self.messages[0],
          messages=self.messages[1:]
        )
        output = response.content.text
      
      scad_code = extract_code_blocks(output)[0]
      output = output.replace(scad_code, "")
      scad_code = scad_code.replace("openscad", "")
      scad_code = scad_code.replace("scad", "")
      scad_code = scad_code.replace("```", "")
      
      
      output.replace(scad_code, "")

        
      self.explanations.append(output)
      self.scad_codes.append(scad_code)
      with open(f"scad_files/generated{self.num_iter}.scad", "w") as f:
        f.write(scad_code)
      
      self.cad_process = subprocess.Popen(["openscad", f"scad_files\generated{self.num_iter}.scad"])
    except Exception as e:
      self.explanations.append(f"Error: {e}\n")

    self.num_iter+=1
  
  def iterate(self, prompt, image):
    """
    accepts an image, improves based on it
    """
    image_msg = prepare_img(image, self.model)
    prompt = "Identify all the things wrong with your previous design and fix them. " + prompt

    image_msg["content"].append( {"type": "text", "text": prompt})
    self.messages.append(image_msg)
    try:
      print(self.model)

      if self.model in Agent.openai_models+Agent.xai_models:
        response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
        )
        output = response.choices[0].message.content

      elif self.model in Agent.anthropic_models:
        response = self.client.messages.create(
          model=self.model,
          max_tokens=2048,
          system=self.messages[0],
          messages=self.messages[1:]
        )
        output = response.content.text

      output = response.choices[0].message.content
      scad_code = extract_code_blocks(output)[0]
      output = output.replace(scad_code, "")
      scad_code = scad_code.replace("openscad", "")
      scad_code = scad_code.replace("scad", "")
      scad_code = scad_code.replace("```", "")


      
      self.explanations.append(output)
      self.scad_codes.append(scad_code)
      with open(f"scad_files/generated{self.num_iter}.scad", "w") as f:
        f.write(scad_code)
      
      self.cad_process = subprocess.Popen(["openscad", f"scad_files\generated{self.num_iter}.scad"])

    except Exception as e:
      self.explanations.append(f"Error: {e}\n")
    
    self.num_iter += 1


def extract_code_blocks(text):
  code_blocks = re.search(r"```(?:\w+)?\n(.*?)\n```", text, re.DOTALL)
  return code_blocks

def prepare_img(image, model):
  image = image.convert('RGB')
  buffered = BytesIO()
  image.save(buffered, format="JPEG")
  img_bytes = buffered.getvalue()
  
  base64_image = base64.b64encode(img_bytes).decode('utf-8')

  if model in Agent.anthropic_models:
    msg = {"role": "user", "content": [
    {
      "type": "image",
      "source": {
        "type": "base64",
        "media_type": "image/jpeg",
        "data": base64_image,
      }
    },
   
  ]}
  else:
    msg = {"role" : "user", 
               "content" : [
                {
                  "type" : "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{image}"
                  }
                }
               ]
              }

  return msg

