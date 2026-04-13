import ollama
from config import OLLAMA_MODEL

def generate_text(prompt, system_prompt=None):
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})
    
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages
        )
        return response.get('message', {}).get('content', '').strip()
    except Exception as e:
        print(f"LLM Error: {e}")
        return None
