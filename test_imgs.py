import base64
from io import BytesIO
from PIL import Image
from anthropic import Anthropic
from openai import OpenAI

def prepare_img(image):
  image = image.convert('RGB')
  buffered = BytesIO()
  image.save(buffered, format="JPEG")
  img_bytes = buffered.getvalue()
  
  base64_image = base64.b64encode(img_bytes).decode('utf-8')
  return base64_image

def test_chat():
  image = Image.open("cartoon.jpeg")
  image = prepare_img(image)
  msg = {"role" : "user", 
               "content" : [
                {
                  "type" : "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{image}"
                  }
                },
                {"type": "text", "text": "What is in this image?"}
               ]
              }
  messages = [{"role" : "system", "content" : "You are an expert image Identifier"}]
  messages.append(msg)
  client = OpenAI()
  image = Image.open("cartoon.jpeg")
  image = prepare_img(image)


  response = client.chat.completions.create(
      model="gpt-4o",
      messages=messages
    )

  print(response.choices[0].message.content)

def test_claude():

  client = Anthropic()
  image = Image.open("cartoon.jpeg")
  image = prepare_img(image)

  messages = [{"role": "user", "content": [
    {
      "type": "image",
      "source": {
        "type": "base64",
        "media_type": "image/jpeg",
        "data": image,
      }
    },
    {"type": "text", "text": "What is in this image?"}
  ]}]
  response = client.messages.create(
      model="claude-3-5-sonnet-20241022",
      max_tokens=2048,
      system="You are an expert image identifier",
      messages=messages
    )

  print(response.content)

test_claude()
test_chat()