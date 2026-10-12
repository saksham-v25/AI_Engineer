import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)

model="openai/gpt-oss-20b"
role="user"

#structure it 
from pydantic import BaseModel

class Ticket(BaseModel):
    name:str
    email:str
    phone:str
    address:str

schema=Ticket.model_json_schema()

response_format={
    "type":"json_object"
}


system_prompt=f""" 
Extract the information from the tocket based on this schema and give me a json output and each information must start in new line.
{schema}
"""
message_system={
    "role":"system",
    "content":system_prompt
}

text="My name is Saksham.My iphone is not working.My address is delhi.My email is abc@g,ail,com.my phone number is 838389. "
prompt=f"""This is customer ticket .pls extract personel infromationfrom
{text}
 """
# message me role and content
message={
    "role": role,
    "content": prompt
}

messages=[message_system,message]

response=client.chat.completions.create(model=model, messages=messages ,response_format=response_format)


print("#######################################")

answer=response.choices[0].message.content
print(answer)


print("############------------------------------------------------------------------------------##########")

#isko padte kaise hai 
import json
raw_data=answer
data_file=json.loads(raw_data)
ticket=Ticket(**data_file)

# isko pass kar sakte hai aage
print(ticket.name)
print(ticket.email)
print(ticket.phone)
print(data_file["address"])

