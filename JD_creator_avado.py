import streamlit as st
import openai
# from dotenv import load_dotenv
import os

# def get_user_api_key():
#     return st.sidebar.text_input("Enter your OpenAI API Key")

# def initialize_openai_client():
#     load_dotenv()
#     api_key = get_user_api_key()
#     openai.api_key = api_key

def gpt_function(skills, experience, job_role):
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

    response = openai.ChatCompletion.create(
        messages=conversation,
        model="gpt-3.5-turbo",
    )
    text_response = response.choices[0].message["content"]
    return text_response

def main():
    st.title("JD Creator")

    key = st.text_input("Enter your key")
    submit = st.button("Submit key")
    if submit :
        openai.api_key = key

    input_list = ["Specific Required Skills","Experience Level","Job Title"]
    skills = st.text_input(input_list[0])
    experience = st.text_input(input_list[1])
    job_role = st.text_input(input_list[2])

    if skills and experience and job_role:
        if st.button("Submit"):
            with st.spinner("Let the magic happen ...."):
                output = gpt_function(skills, experience, job_role)
                st.write(output)

if __name__ == "__main__":
    main()
