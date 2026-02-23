from openai import OpenAI

client = OpenAI()

def llm_call(system: str, user: str, model: str = "gpt-5.2-chat-latest") -> str:
    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.output_text