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
                                    you have to only give well formatted Job Description for mentioned required skills, experience and job title.
                                    - Divide your answer in sections like Responsibilities, Requirements, Preferred Qualifications
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
    st.title("JD Creator")

    st.sidebar.title("Azure OpenAI API Key and Endpoint")
    openai_api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")
    openai_endpoint = st.sidebar.text_input("Enter your Azure OpenAI Endpoint")
    client = get_openai_client(openai_api_key, openai_endpoint)

    input_list = ["Specific Required Skills","Experience Level","Job Title"]
    skills = st.text_input(input_list[0])
    experience = st.text_input(input_list[1])
    job_role = st.text_input(input_list[2])

    if skills and experience and job_role and openai_api_key and openai_endpoint:
        if st.button("Submit"):
            with st.spinner("Let the magic happen ...."):
                output = gpt_function(client, skills, experience, job_role)
                st.write(output)

if __name__ == "__main__":
    main()
