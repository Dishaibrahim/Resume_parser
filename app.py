import os
import streamlit as st
from resume import parse_resume

# Define a function to parse the resume and display the parsed information
def parse_and_display_resume(uploaded_file):
    # Save the uploaded file to a temporary location
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Parse the resume
    parsed_resume = parse_resume("temp_resume.pdf")

    # Display the parsed information
    st.write("### Parsed Resume Information:")
    st.write(f"**Name:** {parsed_resume['name']}")
    st.write(f"**Email:** {parsed_resume['email']}")
    st.write(f"**Mobile Number:** {parsed_resume['mobile_number']}")
    st.write(f"**Skills:** {', '.join(parsed_resume['skills'])}")
    st.write("#### Education:")
    for edu in parsed_resume['education']:
        st.write(f"- {edu}")
    st.write("#### Experience:")
    for exp in parsed_resume['experience']:
        st.write(f"- {exp}")
    

    # Delete the temporary file
    os.remove("temp_resume.pdf")

# Streamlit UI
st.title("Resume Parser")
st.write("Upload your resume file below:")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# If a file is uploaded
if uploaded_file is not None:
    # Display the file name
    st.write(f"Uploaded file: {uploaded_file.name}")

    # Parse and display the resume information
    parse_and_display_resume(uploaded_file)