import base64
import requests
from os import getenv

# OpenAI API Key
api_key = getenv('OPENAI_API_KEY')

def send_image_to_ai(image_url):
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  message = """
  ### qustion
  What items did you buy?

  ### requirement
  - Please speak in Japanese.
  - You should provide only item's name.
  - You should follow the format below.

  - おにぎり
  - お茶
  - お弁当
  """


  payload = {
    "model": "gpt-4o-2024-05-13",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": message
          },
          {
            "type": "image_url",
            "image_url": {
              "url": image_url
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  items_text = response.json()['choices'][0]['message']['content']


  print('品名\n', items_text, '\n')


  prompt = """
  ### question
  - calculate the virtual water of the items he bought.

  ### requirement
  - Please speak in Japanese.
  - If you do not know the virtual water content of an item, please mark this as 'データ未提供' and consider the item's virtual water content to be 0L in the total calculation. 
  - If you can't accommodate the request, please say so.
  - Please provide only the answer such as below.

  - おにぎり: 100L
  - お茶: 50L
  - お弁当: 200L
  - 合計: 350L
  """

  payload = {
      "model": "gpt-4o-2024-05-13",
      "messages": [
          {
              "role": "user",
              "content": [
                  {
                  "type": "text",
                  "text": prompt
                  },
                  {
                  "type": "text",
                  "text": items_text
                  }
              ]
          }
      ],
      "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  virtual_water_text = response.json()['choices'][0]['message']['content']

  print('仮想水\n', virtual_water_text)

  return virtual_water_text, items_text