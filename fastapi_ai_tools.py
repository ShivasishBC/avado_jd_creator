from fastapi import FastAPI, HTTPException
import openai

app = FastAPI()

def get_openai_client(api_key, endpoint):
    openai.api_type = 'azure'
    openai.api_key = api_key
    openai.api_version = '2023-12-01-preview'
    openai.api_base = endpoint
    return openai


@app.post("/job_description_creator")
async def job_description_creator(api_key: str, endpoint: str, experience: str, job_role: str, skills: str = None):

    client = get_openai_client(api_key, endpoint)

    if skills is None:
        skills = "None"

    user_content = f"""
    Create a Job Description for 
    Required Skills: {skills}.
    Experience: {experience} 
    Job Role: {job_role}
    """

    conversation = [{"role": "system", "content": """You are a Job Description creator bot,
                        you have to only give well formatted Job Description for mentioned Job Title [Job role] , Experience Level[Experience] and required skills (if any) in british english.
                        Divide your answer in proper formatted sections and subheadings including Job title and Experience level followed: 
                         
                        1. ### Role summary,
                        2. ### Responsibilities ,
                        3. ### Success metrics ,
                        4. ### Skills required, 
                        5. ### Recommended qualifications 
                        - You may  add an extra catch up line for the interviewer to get his/her interest in the Technology and Roles that <Company Name> is going to offer.
                        - if adding a catch up  line then give few spaces and dont mention any title for it. just give the line
                        """},
                    {"role": "user", "content": f"{user_content}"}]

    response = client.ChatCompletion.create(
        messages=conversation,
        engine="gpt-35-turbo",
        temperature=0
    )
    text_response = response.choices[0].message.content

    return {"job_description": text_response}




@app.post("/policy_checker")
async def policy_checker(api_key: str, endpoint: str, policy_type: str, hr_policy: str, sector: str, country: str):
    client = get_openai_client(api_key, endpoint)

    user_content = f"""
    Policy Type : {policy_type}
    Company Policy: {hr_policy}
    Sector: {sector}
    Country: {country}
    
    Use the provided Policy Type , company policy, sector, and country information to ensure alignment with legal standards and best practices.
    Provide a report highlighting alignment with industry best practices, including a summary of country best practices, alignment of your policy with regional best practices, and recommendations for greater alignment in british english.
    """

    conversation = [
        {"role": "system", "content": """You are a Policy Proofer bot 
                            
                        You will be given the following information in details with proper format and subheadings including Company Sector (Sector) , Country Located (Country):
                            
                        - Use this below Headings ad markdown
                                1. #### Summary of {policy_type}
                                2. #### Best practices in {country}
                                2. #### How Your Policy compares 
                                3. #### Recomandations to improve your policy
                                """},
        {"role": "user", "content": f"{user_content}"}
    ]

    response = client.ChatCompletion.create(
        messages=conversation,
        engine="gpt-35-turbo",
        temperature=0

    )
    text_response = response.choices[0].message.content
    return {"policy_check_result": text_response}


@app.post("/skills_planner")
async def skills_planner(api_key: str, endpoint: str, size: str, sector: str, business_function: str = None):
    client = get_openai_client(api_key, endpoint)

    user_content = f"""
    Get future recommendations for training or hiring strategies for the following parameters 
    Company Size: {size} People.
    Company Sector: {sector}
    Business function{business_function}(Optional)
    """

    conversation = [{"role": "system", "content": """You are a future AI skills Planner.
                        Your role is to identify AI skills gaps in your organization and get recommendations for training or hiring strategies, based on the given parameters Company size , Sector and function(Optional) in british english.
                        You should address skill gaps and inform talent development strategies
                                        
                        The output should only contain below details with proper format and subheadings:
                                        
                        1. #### AI impact
                            - How AI is changing in (Company Sector) - AI impact on sector summary Skills & Capabilities required to harness AI
                        2. #### Skills and capabilities needed to harness AI
                            - The Skills And Capabilities needed to harness AI in (Business function)
                        3. #### Recomandations
                            - Recomandation for training or hiring strategies to address AI skills gapsin (Company Size) and (Company Sector)    
                                            
                        Steps to analyze:
                        - Analyze the current skills inventory
                        - Forecast future needs
                        - Provide recommendations for training or hiring to fill gaps 
                        """},
                    {"role": "user", "content": f"{user_content}"}]

    response = client.ChatCompletion.create(
        messages=conversation,
        engine="gpt-35-turbo",
        temperature=0
    )
    text_response = response.choices[0].message.content

    return {"skills_plan": text_response}

