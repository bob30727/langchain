from backend.services.llama_engine import run_llama

def process_message(message: str) -> str:
    reply = run_llama(message)
    return reply