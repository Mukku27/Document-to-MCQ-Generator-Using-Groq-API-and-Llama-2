from setuptools import find_packages,setup

setup(

    name='mcqgenerator',
    version='0.0.1',
    author='Mukesh Vemulapalli',
    author_email='vemulapallimukesh@gmail.com',
    install_requires=['openai','langchain','streamlit','python-dotenv','google-generativeai','pyPDF2'],
    packages=find_packages()
)