import io
import os
import re
import nltk
import spacy
import pandas as pd
import csv
import docx2txt
from nltk.corpus import stopwords
import likes as cs
from spacy.matcher import Matcher
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from nltk.stem import WordNetLemmatizer


def extract_text_from_pdf(pdf_path):
    '''
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted
    :return: iterator of string of extracted text
    '''
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
            yield text
 
            # close open handles
            converter.close()
            fake_file_handle.close()

def extract_text_from_doc(doc_path):
    '''
    Helper function to extract plain text from .doc or .docx files

    :param doc_path: path to .doc or .docx file to be extracted
    :return: string of extracted text
    '''
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)

def extract_text(file_path, extension):
    '''
    Wrapper function to detect the file extension and call text extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    if extension == '.pdf':
        for page in extract_text_from_pdf(file_path):
            text += ' ' + page
    elif extension == '.docx' or extension == '.doc':
        text = extract_text_from_doc(file_path)
    return text

def extract_entity_sections(text):
    '''
    Helper function to extract all the raw text from sections of resume

    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(cs.RESUME_SECTIONS)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)
    return entities

def extract_email(text):
    '''
    Helper function to extract email id from text

    :param text: plain text extracted from resume file
    '''
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)
    emails = []
    for token in doc:
        if token.like_email:
            emails.append(token.text)
    if emails:
        return emails[0]
    else:
        return None




def extract_name(nlp_text):
    '''
    Helper function to extract name from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: string of full name
    '''
    # Load English tokenizer, tagger, parser, NER, and word vectors
    nlp = spacy.load("en_core_web_md")
    
    # Initialize matcher
    matcher = Matcher(nlp.vocab)
    
    pattern1 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern1])
  # Add the pattern to the matcher (notice the list wrapping the pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text


def extract_mobile_number(text):
    '''
    Helper function to extract mobile number from text

    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    '''
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number
    return None

def extract_skills(text):
    '''
    Helper function to extract skills from text

    :param text: plain text extracted from resume file
    :return: list of skills extracted
    '''
    nlp = spacy.load("en_core_web_md")
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) 
    skills = data.iloc[:, 0].tolist()
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams
    for token in doc.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

# def extract_education(text):
#     '''
#     Helper function to extract education from text

#     :param text: plain text extracted from resume file
#     :return: tuple of education degree and year if year if found else only returns education degree
#     '''
#     edu = {}
#     # Extract education degree
#     for index, word in enumerate(text.split()):
#         for edu_degree in cs.EDUCATION:
#             if word.upper() == edu_degree:
#                 if index < len(text.split()) - 1:
#                     next_word = text.split()[index + 1]
#                     edu[edu_degree] = next_word
#                 break

#     # Extract year
#     education = []
#     for key in edu.keys():
#         year = re.search(re.compile(cs.YEAR), edu[key])
#         if year:
#             education.append((key, ''.join(year.group(0))))
#         else:
#             education.append(key)
#     return education



def extract_education(text):
    '''
    Helper function to extract education from text

    :param text: plain text extracted from resume file
    :return: list of dictionaries containing education information
    '''
    # Split the text based on common delimiters
    education_sections = re.split(r'\b(education)\b', text, flags=re.IGNORECASE)

    # List to store extracted education information
    education_list = []

    # Iterate over the sections to find education details
    for section in education_sections:
        # Extract degree
        degree_match = re.search(r'\b(' + '|'.join(cs.EDUCATION) + r')\b', section, flags=re.IGNORECASE)
        if degree_match:
            degree = degree_match.group(0).strip()

            # Extract school
            school_match = re.search(r'\|\s*(.*?)\s*\|', section)
            if school_match:
                school = school_match.group(1).strip()

                # Extract grade
                grade_match = re.search(r'\b(cgpa|percentage)\s*[-:]\s*([\d.]+)\b', section, flags=re.IGNORECASE)
                if grade_match:
                    grade_type = grade_match.group(1).strip()
                    grade = float(grade_match.group(2).strip())

                    # Create a dictionary to store education information
                    education_info = {
                        'degree': degree,
                        'school': school,
                        'grade_type': grade_type,
                        'grade': grade
                    }

                    # Append the education information to the list
                    education_list.append(education_info)

    return education_list


# def extract_work_experience(text):
#     '''
#     Helper function to extract work experience from text

#     :param text: plain text extracted from resume file
#     :return: list of dictionaries, each containing company, role, and duration
#     '''
#     patterns = [
#         (r"^(.*?)\s*\|\s*(.*?)\s*\|\s*(\w+\s+-\s+\w+\s+\d+)$", ["company", "role", "duration"]),
#         (r"^(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)$", ["company", "role", "duration"])
#         # Add more patterns for different templates as needed
#     ]

#     work_experience = []
#     lines = text.split("\n")
#     for line in lines:
#         for pattern, labels in patterns:
#             match = re.search(pattern, line)
#             if match:
#                 entry = {label: match.group(i + 1).strip() for i, label in enumerate(labels)}
#                 work_experience.append(entry)
#                 break
#     return work_experience

# def extract_experience(text):
#     '''
#     Helper function to extract experience from text

#     :param text: plain text extracted from resume file
#     :return: list of dictionaries, each containing company, role, duration, and experience
#     '''
#     # Load the English language model
#     nlp = spacy.load("en_core_web_md")

#     # Process the text using spaCy
#     doc = nlp(text)

#     # Extract work experience using the WorkExperienceExtractor
#     work_experience = extract_work_experience(text)

#     # Filter work experience entries that contain 'experience'
#     experiences = []
#     for entry in work_experience:
#         if "experience" in entry["role"].lower():
#             # Add company, role, duration, and experience to the list of experiences
#             experiences.append({
#                 "company": entry["company"],
#                 "role": entry["role"],
#                 "duration": entry["duration"],
#                 "experience": entry["role"].replace("Experience", "").strip()
#             })

#     return experiences
def extract_experience(text):
    excluded_words = set()
    with open('/Users/dishaibrahim/Desktop/suryaproject/resumeparser/skills.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            excluded_words.add(row[0].strip())

    # Load roles from jobs.csv
    roles = set()
    with open('jobs.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            roles.add(row[0].strip())

    # Import patterns and competencies from likes.py
    from likes import RESUME_SECTIONS, COMPETENCIES, MONTH, YEAR

    # Extend excluded words with terms to exclude
    excluded_words.update(['location', 'email'])

    # Add competencies from likes.py to excluded words
    for competency_words in COMPETENCIES.values():
        excluded_words.update(competency_words)

    # Define patterns for parsing work experience
    patterns = [
        (re.compile(r"^(.*?)\s*\|\s*(" + '|'.join(roles) + r")\s*\|\s*(" + MONTH + r" " + YEAR + r")$"), ["company", "role", "duration"]),
        (re.compile(r"^(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)$"), ["company", "role", "duration"])
        # Add more patterns for different templates as needed
    ]

    work_experience = []
    lines = text.split("\n")
    for line in lines:
        for pattern, labels in patterns:
            match = pattern.search(line)
            if match:
                entry = {label: match.group(i + 1).strip() for i, label in enumerate(labels)}
                # Exclude skills, location, and email based on excluded words
                for label, value in entry.items():
                    if label == "role" and value not in roles:
                        # Skip if the role is not in the list of roles from jobs.csv
                        break
                    if label == "role":
                        skills = [skill.strip() for skill in value.split(",") if skill.strip() not in excluded_words]
                        entry[label] = ", ".join(skills)
                else:
                    work_experience.append(entry)
                    break
    return work_experience
     


   

def extract_competencies(text, experience_list):
    '''
    Helper function to extract competencies from text

    :param text: Plain text extracted from resume file
    :return: dictionary of competencies
    '''
    experience_text = ' '.join(experience_list)
    competency_dict = {}

    for competency in cs.COMPETENCIES.keys():
        for item in cs.COMPETENCIES[competency]:
            if string_found(item, experience_text):
                if competency not in competency_dict.keys():
                    competency_dict[competency] = [item]
                else:
                    competency_dict[competency].append(item)
    
    return competency_dict

def extract_measurable_results(text, experience_list):
    '''
    Helper function to extract measurable results from text

    :param text: Plain text extracted from resume file
    :return: dictionary of measurable results
    '''

    # we scan for measurable results only in first half of each sentence
    experience_text = ' '.join([text[:len(text) // 2 - 1] for text in experience_list])
    mr_dict = {}

    for mr in cs.MEASURABLE_RESULTS.keys():
        for item in cs.MEASURABLE_RESULTS[mr]:
            if string_found(item, experience_text):
                if mr not in mr_dict.keys():
                    mr_dict[mr] = [item]
                else:
                    mr_dict[mr].append(item)
    
    return mr_dict

def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False