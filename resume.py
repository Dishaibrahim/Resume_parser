import os
import spacy
import csv
import re
from functions import extract_text, extract_entity_sections, extract_email, extract_name, extract_mobile_number, extract_skills, extract_education, extract_experience, extract_competencies, extract_measurable_results

def parse_resume(resume_path):
    # Extract text from resume
    nlp = spacy.load('en_core_web_trf')
    text = extract_text(resume_path, os.path.splitext(resume_path)[1])

    # Process text with spaCy model
    nlp_text = nlp(text)

    name = extract_name(nlp_text)
    email = extract_email(text)
    mobile_number = extract_mobile_number(text)
    
    sections = extract_entity_sections(text)
    education = extract_education(text)
    
    # Extract experience using the provided function
    experience = extract_experience(text)

    skills = extract_skills(text)
  
    parsed_resume = {
        'name': name,
        'email': email,
        'mobile_number': mobile_number,
        'skills': skills,
        'education': education,
        'experience': experience
        
    }

    return parsed_resume

if __name__ == "__main__":
    # Provide the path to the resume file you want to parse
    resume_path = "/Users/dishaibrahim/Desktop/suryaproject/2903.pdf"

    # Parse the resume
    parsed_resume = parse_resume(resume_path)

    # Print the parsed information
    print("Name:", parsed_resume['name'])
    print("Email:", parsed_resume['email'])
    print("Mobile Number:", parsed_resume['mobile_number'])
    print("Skills:", parsed_resume['skills'])
    print("Education:", parsed_resume['education'])
    print("Experience:")
    for exp in parsed_resume['experience']:
        print(f"- {exp['company']}, {exp['role']}, {exp['duration']}")
    
