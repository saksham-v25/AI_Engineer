import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"


JD="""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
RESUME="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def ask_llm(sys_prompt,user_prompt):
    sys_msg={
        'role': 'system',
        'content':sys_prompt
    }

    user_msg={
            'role': 'user',
            'content':user_prompt
        }

    messages=[sys_msg,user_msg]
    response=client.chat.completions.create(model=model,messages=messages)
    answer= response.choices[0].message.content
    return answer


def step1_extract_resume(RESUME):

    print("Extracting candidate from resume...")
    sys_prompt=f"""
                   You are an expert HR Resume Parser.

                    Your task is to extract structured candidate information from the resume.

                    Return ONLY valid JSON.

                    Extract:
                    - Candidate Name
                    - Total Experience
                    - Skills
                    - Projects
                    - Technologies
                    - Education (if available)

                    Do not add explanations.
                    Do not add markdown.
                    Return JSON only.
          
    """

    user_prompt=f"""
                        Extract candidate information from the following resume.

                        Resume:
                        {RESUME} 
                """

    return ask_llm(sys_prompt,user_prompt)


def step2_jd_extract(JD,RESUME):

    print("Extracting job description from resume...")
    sys_prompt=f"""
                        You are an expert Recruitment Analyst.

                        Your task is to extract hiring requirements from a Job Description.

                        Return ONLY valid JSON.

                        Extract:
                        - Role
                        - Required Skills
                        - Preferred Skills
                        - Required Experience
                        - Tools and Technologies
                        - Responsibilities

                        Do not explain.
                        Return JSON only.
          
    """     
    user_prompt=f"""
                        Extract hiring requirements from the following Job Description.

                        Job Description:
                        {JD}
                  
                """
    return ask_llm(sys_prompt,user_prompt)

def step3_match_result(candidate,jd):

    print("Matching candidate with job description...")
    sys_prompt=f"""
                        
                            You are an expert Technical Recruiter.

                            Compare the candidate profile with the Job Description.

                            Analyze:

                            1. Skill Match
                            2. Experience Match
                            3. Missing Skills
                            4. Strengths
                            5. Weaknesses
                            6. Overall Recommendation

                            Generate:

                            - Match Percentage
                            - Matching Skills
                            - Missing Skills
                            - Recommendation

                            Recommendation should be one of:
                            - Strong Match
                            - Moderate Match
                            - Weak Match

                            Give the result in a clean structured format.        
    """     
    user_prompt=f"""

                                Candidate Information:

                                {candidate}

                                Job Description Information:

                                {jd}

                                Compare both and generate the final evaluation.

                  
            """
    return ask_llm(sys_prompt,user_prompt)



candidate=step1_extract_resume(RESUME)
print("Candidate extracted from resume:",candidate)
sleep(2)
jd=step2_jd_extract(JD,RESUME)
print("Job Description extracted:",jd)
sleep(2)
match_result=step3_match_result(candidate, jd)      
print("Match result:",match_result)