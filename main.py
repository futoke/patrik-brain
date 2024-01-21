import time
import string
import requests
import logging

from time import perf_counter
from llama_cpp import Llama

WAIT_ADDRESS_TIMEOUT = 0.1
SPEECH_SERVER_URL = "http://localhost:8006/say"

llm = Llama(
    model_path="models/model-q4_K.gguf",
    use_mlock=True,
    n_threads=4,
    n_batch=1600
)

stream = llm(
    "Расскажи про котов.",
    max_tokens=256,
    # stop=".",
    # stop=["Q:", "\n"],
    stream=True,
)


def say(phrase):
    time.sleep(WAIT_ADDRESS_TIMEOUT)

    try:
        requests.post(SPEECH_SERVER_URL, json={"phrase": phrase},timeout=1e-10)
    except requests.exceptions.ReadTimeout: 
        pass
    # try:
    #     r = )
    #     if r.status_code != 200:
    #         logging.error("Speech server returns non OK answer")
    # except requests.exceptions.ConnectionError:
    #     logging.error(f"No connection to speech server {SPEECH_SERVER_URL}")


buffer = ""
word = ""
sentence = []

for output in stream:
    token = output["choices"][0]["text"].removeprefix('"').removesuffix('"')

    if token.startswith(" "):
        if buffer:
            if buffer[-1] not in string.punctuation:
                word = buffer[1:]
            else:
                word = buffer[1:]
        buffer = ""
        
    if token not in (" –", " -"):
        buffer += token

    # if word and word[0].isupper():
    #     say(" ".join(sequence))
    #     sequence = []
    
    if len(sentence) == 13:
        print(sentence)
        say(" ".join(sentence))
        sentence = []
    
    if word:
        sentence += [word]
        word = ""
