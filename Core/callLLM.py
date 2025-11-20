import requests
import json
import os
from Config_Manager import Config_Manager

config = Config_Manager()



def call(chat_memory, max_tokens = 300, test = False):
    model = config.get('AI.model')
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.get("API.openrouter_key")}",
        
            
            
        },
        data=json.dumps({
            "model": model, 
            "messages": chat_memory,
            "max_tokens": max_tokens,
            "extra_body": {"reasoning": {"enabled": False}}
        }))
    
    response = response.json()

    if test:
        print(response)
        try:
            response["choices"][0]["message"]["content"]
        except:
            print(f"Error: {response['error']['message']} - Code: {response['error']['code']}")

    try:
        return response["choices"][0]["message"]["content"]
    except:
        return False, f"Error: {response['error']['message']} - Code: {response['error']['code']}"
if __name__ == '__main__':
    print(call([{"role": "system", "content": "you are GlaD0s from the video game Portal"}, {"role": "user", "content": "hello"}], test=True))