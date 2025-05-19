from llama_cpp import Llama

llm = Llama(model_path="backend/models/llama-2-7b-chat.Q3_K_L.gguf")

def run_llama(prompt: str) -> str:
    full_prompt = f"User: {prompt}\nAssistant: "
    output = llm(
        prompt=full_prompt,
        max_tokens=200,
        stop=["User:", "Assistant:"],
        temperature=0.7,
    )
    return output["choices"][0]["text"].strip()
