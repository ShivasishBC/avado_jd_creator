import streamlit as st
from openai import OpenAI



def gpt_function(client, skills, experience, job_role):
    user_content = f"""
    Create a Job Description for 
    Company : [Company Name]
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

    response = client.chat.completions.create(
        messages=conversation,
        model="gpt-4o",
        temperature=0
    )
    text_response = response.choices[0].message.content

    return text_response

def main():
    st.title(" Job Description Drafter")
    description = """
    ###### Create a job description for the role you are hiring.
    """
    st.markdown(description , unsafe_allow_html=True)

    st.sidebar.title("Azure OpenAI API Key and Endpoint")
    api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")
    client = OpenAI(api_key=api_key)

    input_list = ["Any Specific Required Skills","Experience Level","Job Title"]

    job_role = st.text_input(input_list[2])
    experience = st.text_input(input_list[1])
    skills = st.text_input(input_list[0])
    
    if not skills:
        skills = "None"
    

    if experience and job_role and api_key:
        if st.button("Submit"):
            with st.spinner("Saving you time ...."):
                output = gpt_function(client, skills, experience, job_role)
                st.markdown(output,unsafe_allow_html=True)

if __name__ == "__main__":
    main()
