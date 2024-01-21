import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from llama_cpp import Llama


llm = Llama(
    model_path="models/model-q4_K.gguf",
    seed=-1,
    # use_mlock=True,
    n_threads=4,
    n_batch=1600,
    temperature=0.7,
    chat_format="llama-2"
)


app = FastAPI()


def get_llama_answer():
    buffer = ""

    stream = llm.create_chat_completion(
        stream=True,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "Подробно опиши прекрасную картину с рыжими котиками."
        }]
    )

    for id, output in enumerate(stream):
        token = output["choices"][0]["delta"].get("content")

        if token:
            token = token.replace("\n", " ")

            if token.startswith(" ") and len(buffer) >= 128:
                yield json.dumps({"chunk_id": id, "data": buffer.strip()})  + '\n'
                buffer = ""

            buffer += token


@app.get("/")
async def root():
    print("Received a request on /")
    return {"message": "Hello World"}


@app.get('/stream')
async def main():
    return StreamingResponse(
        get_llama_answer(),
        media_type='application/x-ndjson'
    )
