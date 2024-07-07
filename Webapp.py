import streamlit as st
import os
from src.mcqgenerator.MCQgenerator import main, generate_mcqs, get_table_data, save_quiz_to_csv
from src.mcqgenerator.utils import extract_text_from_file
from src.mcqgenerator.logger import logging

st.set_page_config(page_title="Automated MCQ Generator", page_icon=":books:")

st.title("Automated MCQ Generator through Langchain")

# Custom CSS for highlighting correct and incorrect answers
st.markdown("""
    <style>
    .correct-answer {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .incorrect-answer {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .quiz-summary {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
subject = st.text_input("Enter the subject")
num_questions = st.number_input("Enter the number of questions", min_value=1, max_value=100, step=1)
tone = st.selectbox("Select the tone for the questions", ["Educational", "Informative", "Casual"])

if 'quiz_table_data' not in st.session_state:
    st.session_state.quiz_table_data = None
if 'quiz_results' not in st.session_state:
    st.session_state.quiz_results = {'total': 0, 'attempted': 0, 'correct': 0}
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

def generate_and_display_mcqs(file_path, subject, num_questions, tone):
    try:
        text = extract_text_from_file(file_path)
        quiz_data = generate_mcqs(subject, tone, int(num_questions), text)
        quiz_table_data = get_table_data(quiz_data)
        st.session_state.quiz_table_data = quiz_table_data
        st.session_state.quiz_results = {'total': len(quiz_table_data), 'attempted': 0, 'correct': 0}
        st.session_state.user_answers = {}
        st.session_state.current_question = 0
        st.experimental_rerun()
    except Exception as e:
        st.error(f"An error occurred: {e}")

def display_quiz_summary():
    st.markdown("<div class='quiz-summary'>", unsafe_allow_html=True)
    st.write(f"**Total Questions:** {st.session_state.quiz_results['total']}")
    st.write(f"**Attempted:** {st.session_state.quiz_results['attempted']}")
    st.write(f"**Correct:** {st.session_state.quiz_results['correct']}")
    st.write(f"**Wrong:** {st.session_state.quiz_results['attempted'] - st.session_state.quiz_results['correct']}")
    st.markdown("</div>", unsafe_allow_html=True)

def display_current_question():
    if st.session_state.current_question < len(st.session_state.quiz_table_data):
        item = st.session_state.quiz_table_data[st.session_state.current_question]
        st.write(f"### Question {st.session_state.current_question + 1}")
        st.write(f"**{item['MCQ']}**")
        options = [item[f'Option_{chr(65+i)}'] for i in range(4)]  # Assuming 4 options A, B, C, D
        selected_option = st.radio("Choose your answer:", options, key=f"question_{st.session_state.current_question}")

        if st.button("Submit Answer"):
            st.session_state.user_answers[st.session_state.current_question] = selected_option
            st.session_state.quiz_results['attempted'] += 1
            if selected_option.strip() == item['Correct'].strip():
                st.session_state.quiz_results['correct'] += 1
                st.markdown(f"<div class='correct-answer'>Correct! Your answer: {selected_option}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='incorrect-answer'>Incorrect. Your answer: {selected_option}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='correct-answer'>Correct answer: {item['Correct']}</div>", unsafe_allow_html=True)
            
            st.session_state.current_question += 1
            st.experimental_rerun()
    else:
        st.write("You have completed the quiz!")
        if st.button("Start Over"):
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.quiz_results = {'total': len(st.session_state.quiz_table_data), 'attempted': 0, 'correct': 0}
            st.experimental_rerun()

if st.button("Generate MCQs"):
    if uploaded_file is not None and subject and num_questions and tone:
        file_path = f"temp/{uploaded_file.name}"
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Generating MCQs..."):
            generate_and_display_mcqs(file_path, subject, num_questions, tone)
    else:
        st.error("Please fill all the fields and upload a file.")

if st.session_state.quiz_table_data:
    display_quiz_summary()
    display_current_question()

    if st.button("Download MCQ CSV"):
        save_quiz_to_csv(st.session_state.quiz_table_data)
        with open("quiz.csv", "rb") as file:
            btn = st.download_button(
                label="Download MCQ CSV",
                data=file,
                file_name="quiz.csv",
                mime="text/csv"
            )

    if st.button("Regenerate MCQs"):
        if uploaded_file is not None and subject and num_questions and tone:
            file_path = f"temp/{uploaded_file.name}"
            with st.spinner("Regenerating MCQs..."):
                generate_and_display_mcqs(file_path, subject, num_questions, tone)
        else:
            st.error("Please fill all the fields and upload a file.")