import os
import re 
import json
from src.mcqgenerator.logger import logging
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from src.mcqgenerator.utils import extract_text_from_file, get_table_data, save_quiz_to_csv

# Load environment variables
load_dotenv()
KEY = os.getenv("GROQ_API_KEY")

# Initialize ChatGroq
chat = ChatGroq(
    api_key=KEY,
    model="llama3-70b-8192",
    temperature=0.3
)

def generate_mcqs(subject, tone, num_questions, text):
    """Generate MCQs using a generative AI model."""
    logging.info("Generating MCQs")
    
    prompt_template = PromptTemplate(
        input_variables=["subject", "tone", "num_questions", "text"],
        template="""
        Act as an expert in {subject} and don't sound like AI.
        Create a quiz with the following specifications:
        - Subject: {subject}
        - Tone: {tone}
        - Number of questions: {num_questions}
        - Based on the following text: {text}
        - Format the response as JSON with the following structure:
        {{
          "quiz": {{
            "title": "Quiz Title",
            "questions": [
              {{
                "question": "Question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": "Correct option"
              }},
              ...
            ]
          }}
        }}
        """
    )
    
    formatted_prompt = prompt_template.format(
        subject=subject,
        tone=tone,
        num_questions=num_questions,
        text=text
    )
    
    response = chat.invoke(formatted_prompt)
    
    response_metadata = response.response_metadata
    logging.info(f"Total Tokens: {response_metadata['token_usage']['total_tokens']}")
    logging.info(f"Prompt Tokens: {response_metadata['token_usage']['prompt_tokens']}")
    logging.info(f"Completion Tokens: {response_metadata['token_usage']['completion_tokens']}")
    logging.info(f"Total cost: {response_metadata.get('total_cost', 'N/A')}")
    
    quiz = response.content
    logging.info("Raw response received")
    
    try:
        quiz_data = json.loads(quiz)
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', quiz, re.DOTALL)
        if json_match:
            try:
                quiz_data = json.loads(json_match.group())
            except json.JSONDecodeError:
                logging.error("Failed to extract valid JSON from the response.")
                raise
        else:
            logging.error("No JSON-like structure found in the response.")
            raise
    
    return quiz_data

def main(file_path, subject, num_questions, tone):
    """Main function to generate MCQs and save them to a CSV file."""
    logging.info("Starting the MCQ generation process")
    text = extract_text_from_file(file_path)
    quiz_data = generate_mcqs(subject, tone, num_questions, text)
    quiz_table_data = get_table_data(quiz_data)
    save_quiz_to_csv(quiz_table_data)
    logging.info("MCQ generation process completed")