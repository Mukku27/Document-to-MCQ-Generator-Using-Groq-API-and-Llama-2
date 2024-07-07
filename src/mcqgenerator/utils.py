import re
import pandas as pd
import json
from src.mcqgenerator.logger import logging

def extract_text_from_file(file_path):
    """Extract text from a pdf or txt file."""
    logging.info(f"Extracting text from {file_path}")
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format")

def extract_text_from_pdf(file_path):
    """Placeholder function to extract text from a PDF file."""
    logging.info(f"Extracting text from PDF {file_path}")
    # Implement PDF extraction logic
    return "Extracted text from PDF"

def extract_text_from_txt(file_path):
    """Extract text from a TXT file."""
    logging.info(f"Extracting text from TXT {file_path}")
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def get_table_data(quiz_data):
    """Process quiz data into a table format with separate columns for options."""
    logging.info("Processing quiz data into table format")
    quiz_table_data = []

    if 'quiz' in quiz_data and 'questions' in quiz_data['quiz']:
        for question in quiz_data['quiz']['questions']:
            mcq = question.get('question', 'N/A')
            options = question.get('options', [])
            correct = question.get('correct', 'N/A')
            
            row = {
                "MCQ": mcq,
                "Correct": correct
            }
            
            for i, option in enumerate(options):
                row[f"Option_{chr(65+i)}"] = option  # A, B, C, D...
            
            quiz_table_data.append(row)
    else:
        raise ValueError("Unexpected JSON structure. Please check the model's output format.")
    
    return quiz_table_data

def save_quiz_to_csv(quiz_table_data, filename='quiz.csv'):
    """Save the quiz table data to a CSV file."""
    logging.info(f"Saving quiz data to {filename}")
    df = pd.DataFrame(quiz_table_data)
    df.to_csv(filename, index=False)