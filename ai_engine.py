from iris_system_prompt import IRIS_SYSTEM_PROMPT


from groq import Groq

client = Groq(
    api_key="Your API KEY"
)

def get_ai_reply(user_query: str) -> str:
    full_prompt = f"{IRIS_SYSTEM_PROMPT}\n\nUser: {user_query}\nIRIS:"

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()


