# Resume Parser

## Overview
This is a Python application that parses resumes in PDF format and extracts key information such as name, email, mobile number, education, skills, and work experience. It utilizes the spaCy library for natural language processing.

## Features
- Extracts name, email, and mobile number from the resume.
- Parses education details including degree and year.
- Identifies skills mentioned in the resume.
- Extracts work experience including company, role, and duration.

## Installation
1. Clone this repository to your local machine:
    ```
    git clone <repository_url>
    ```
2. Navigate to the project directory:
    ```
    cd resume-parser
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage
1. Run the `app.py` file:
    ```
    streamlit run app.py
    ```
2. Upload a PDF file containing a resume using the file uploader.
3. Once the file is uploaded, the parsed information will be displayed on the Streamlit UI.

## Dependencies
- Streamlit
- spaCy
- pandas
- pdfminer.six
- docx2txt

## Project Structure
- `app.py`: Contains the Streamlit application code for UI.
- `resume.py`: Defines functions for parsing resume files.
- `functions.py`: Includes helper functions for text extraction and parsing.
- `likes.py`: Stores patterns and stopwords for text extraction.
- `requirements.txt`: Lists all the required Python dependencies.

## License
This project is licensed under the [MIT License](LICENSE).
