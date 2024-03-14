import streamlit as st
import openai

def get_openai_client(api_key, endpoint):
    openai.api_type = 'azure'
    openai.api_key = api_key
    openai.api_version = '2023-12-01-preview'
    openai.api_base = endpoint
    return openai

def gpt_function(client, skills, experience, job_role):
    user_content = f"""
    Create a Job Description for 
    Required Skills: {skills}.
    Experience: {experience} 
    Job Role: {job_role}
"""

    conversation = [{"role": "system", "content": """You are a Job Description creator bot,
                                    you have to only give well formatted Job Description for mentioned job title , experience level and required skills (if any).
                                    - Divide your answer in sections like Job title ,Experience level ,Role summary,Responsibilities ,Success metrics ,Skills required and Recommended qualifications 
                                    - You may  add an extra catch up line for the interviewer to get his/her interest in the Technology and Roles that <Company Name> is going to offer.
                                    - if adding a catch up line then give few spaces and dont mention any title for it. just give the line
                                    """},
                     {"role": "user", "content": f"{user_content}"}]

    response = client.ChatCompletion.create(
        messages=conversation,
        engine="gpt-35-turbo",
    )
    text_response = response.choices[0].message.content

    return text_response

def main():
    st.title(" Job Description Drafter")
    description = """
    #### About the App
    ###### This app generates a well-formatted job description based on the provided job title, experience level, and required skills (optional).
    """
    st.markdown(description , unsafe_allow_html=True)

    st.sidebar.title("Azure OpenAI API Key and Endpoint")
    openai_api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")
    openai_endpoint = 'https://bc-api-management-uksouth.azure-api.net'
    client = get_openai_client(openai_api_key,openai_endpoint)

    input_list = ["Any Specific Required Skills(Optional)","Experience Level","Job Title"]

    job_role = st.text_input(input_list[2])
    experience = st.text_input(input_list[1])
    skills = st.text_input(input_list[0])
    
    if not skills:
        skills = "None"
    

    if experience and job_role and openai_api_key and openai_endpoint:
        if st.button("Submit"):
            with st.spinner("Let the magic happen ...."):
                output = gpt_function(client, skills, experience, job_role)
                st.markdown(output,unsafe_allow_html=True)

if __name__ == "__main__":
    main()
