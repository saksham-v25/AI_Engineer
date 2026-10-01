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


#structure it 
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schemat=Ticket.schema_json()

response_format={
    "type": "json_object"
}

system_prompt=f"""
Extract the personal information from ticket strictly based on schema and give me response on json.
{schemat}
"""

message_system={
    "role":"system",
    "content":system_prompt
}
text="my name is saksham .I have an iphone which is not working at all.my adddress is delhi.my email is abc@gmail.com.my cntact number is 823761"
prompt=f""" 
This is the customer ticket .Please extract the personal information fromt this.
{text}
"""
message={
    "role":role,
    "content":prompt
}

messages=[message_system, message]

response=client.chat.completions.create(model=model  ,messages=messages, response_format=response_format)


answer=response.choices[0].message.content
print(answer)



#isko padhte kaise hai 
import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)
