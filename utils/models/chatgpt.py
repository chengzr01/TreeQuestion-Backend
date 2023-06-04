import os
import time
import openai


class ChatGPT:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def call(self,
             prompt,
             temperature=0.,
             top_p=1.,
             frequency_penalty=0,
             presence_penalty=0):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            n=1)
        return response["choices"][0]["message"]["content"]

    def call_with_sleep(self,
                        prompt,
                        sleep=20,
                        temperature=0.,
                        top_p=1.,
                        frequency_penalty=0,
                        presence_penalty=0):
        time_start = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            n=1)
        time_end = time.time()
        if time_end - time_start < sleep:
            time.sleep(sleep - (time_end - time_start))
        return response["choices"][0]["message"]["content"]
