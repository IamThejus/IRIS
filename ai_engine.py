from gpt4all import GPT4All
from iris_system_prompt import IRIS_SYSTEM_PROMPT

model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", device="kompute", ngl=-1)  # GPU via Vulkan/Kompute (RTX 3050)

def get_ai_reply(user_query: str) -> str:
    full_prompt = f"{IRIS_SYSTEM_PROMPT}\n\nUser: {user_query}\nIRIS:"
    with model.chat_session():
        response = model.generate(full_prompt, max_tokens=200)
    return response.strip()
