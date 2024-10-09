import openai
import requests


class Checker():

    def __init__(self,  api_key, api_base):
        self.api_key = api_key
        self.api_base = api_base

    def check(self, message, base64_images):
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.api_key}"
        }
        content = [
            {
                "type": "text",
                "text": message
            }
        ]
        for base64_image in base64_images:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    }
                }
            )
        
        payload = {
            "model": "gpt-4o",
            "messages": [
            {
                "role": "user",
                "content": content,
            }
            ],
            "temperature": 0,
            "max_tokens": 300,
        }
    
        response = requests.post(self.api_base, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        print(response.json())
        return response.json()