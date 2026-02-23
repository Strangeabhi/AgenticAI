import random

def ask_llm(system_prompt,user_input,temperature=0.3):
    responses=[
        "Client-side error detected. Validate input format.",
        "Configuration issue suspected. Check parameters.",
        "Improve validation before sending request."
    ]
    if temperature>0.6:
        return random.choice(responses)
    return responses[0]