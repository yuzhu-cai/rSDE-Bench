from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai

class OpenAILLM(object):
    def __init__(self, api_key, base_url, model, description):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.description = description

    def infer(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.description},
                {"role": "user", "content": prompt}
            ]
            )
        return response.choices[0].message.content


class ClaudeAILLM(object):
    def __init__(self, api_key, base_url, model, description):
        self.client = Anthropic(
            api_key=api_key,
            # base_url=base_url
        )
        self.model = model
        self.description = description

    def infer(self, prompt):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=self.description,
            messages=[
                {"role": "user", "content": prompt}
            ]
            )
        return response.content[0].text

class GeminiAILLM(object):
    def __init__(self, api_key, base_url, model, description):
        genai.configure(api_key=api_key)
        self.model = model
        self.description = description
        self.client = genai.GenerativeModel(model_name=self.model,
                                            system_instruction=self.description)

    def infer(self, prompt):
        response = self.client.generate_content(prompt)
        return response.text