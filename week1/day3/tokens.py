import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq 

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai ")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role='user'

#3 prompts

prompt1="Hi!"
prompt2="explain time in detail but under 100 words"
prompt3="write a 1000 word essay on machine learning"
prompts=[prompt1, prompt2, prompt3]
for prompt in prompts:
    message={
    "role":role,
    "content":prompt
    }
    messages=[message]

    response=client.chat.completions.create(model=model  ,messages=messages, max_tokens=5000)
    print(response)

    usage=response.usage
    print(f"Prompt: {prompt}-->your tokens:{usage.prompt_tokens} completion_tokens:{usage.completion_tokens} total_tokens:{usage.total_tokens} finish reason:{response.choices[0].finish_reason}")
    print("#################################################################################################")

    #answer=response.choices[0].message.content
    #print(answer)

#prompt="do you know pratyush?"





