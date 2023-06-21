import os
import time
import openai


class GPT3:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def call(self,
             prompt,
             engine="text-davinci-003",
             temperature=1,
             top_p=1.,
             frequency_penalty=0,
             presence_penalty=0,
             logprobs=0,
             n=1):
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            logprobs=logprobs,
            n=n)
        return response["choices"][0]["text"]

    def call_with_sleep(self,
                        prompt,
                        sleep=20,
                        engine="text-davinci-003",
                        temperature=1,
                        top_p=1.,
                        frequency_penalty=0,
                        presence_penalty=0,
                        logprobs=0,
                        n=1):
        time_start = time.time()
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            logprobs=logprobs,
            n=n)
        time_end = time.time()
        if time_end - time_start < sleep:
            time.sleep(sleep - (time_end - time_start))
        return response["choices"][0]["text"]
