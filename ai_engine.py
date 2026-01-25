from gpt4all import GPT4All
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

def get_ai_reply(text):
    with model.chat_session():
        return model.generate(
            text,
            max_tokens=150
        )
    
