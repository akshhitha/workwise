import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import pandas as pd
import uuid
import chromadb
from utils import clean_text
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from docx import Document
import re


class Portfolio:
    def __init__(self, file_path="res/my_resume.docx"):
        self.file_path = file_path
        self.techstack_skills = []
        self.name = ""
        self.contact = ""
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def parse_resume(self):
        """Parses the resume document to extract name, contact, tech stack, and skills."""
        document = Document(self.file_path)
        techstack, skills = [], []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            # Search for name and contact using regex patterns
            name_match = re.search(r"Name:\s*(.+)", text)
            contact_match = re.search(r"Contact:\s*(.+)", text)

            if name_match:
                self.name = name_match.group(1).strip()
            if contact_match:
                self.contact = contact_match.group(1).strip()
            if text.startswith("Techstack:"):
                techstack = [item.strip() for item in text.split("Techstack:")[1].split(",")]
            elif text.startswith("Skills:"):
                skills = [item.strip() for item in text.split("Skills:")[1].split(",")]

        self.techstack_skills = list(zip(techstack, skills))

    def load_portfolio(self):
        """Loads portfolio data into ChromaDB."""
        if not self.collection.count():
            self.parse_resume()
            for tech, skill in self.techstack_skills:
                self.collection.add(documents=[tech],
                                    metadatas={"skills": skill},
                                    ids=[str(uuid.uuid4())])

    def query_skills(self, skills):
        """Queries ChromaDB to find relevant skills based on input skills."""
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])


load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key='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', model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, page_data):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION: 
            The scraped text is from the careers page of a website.
            Your task is to extract the job posting information and return in JSON format including the keys: 'role', 'experience', 'skills', 'description'.
            Only return the JSON format.
            ### VALID JSON (NO PREAMBLE):    
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': page_data})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Unable to parse")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, skills, name, contact):
        prompt_email = PromptTemplate.from_template(
            """ 
           ### JOB DESCRIPTION:
           {job_description}

           ### INSTRUCTION:
           You must write a cold email to the client based on the above description.
            Add only the relevant skill from the following to show highest relevancy: {skill_list}. 
            Write in a pleasing and professional tone.
           """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "skill_list": skills, "name": name, "contact": contact})
        return res.content


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cold Mail Generator")

    # Resume upload section
    uploaded_file = st.file_uploader("Upload your resume (DOCX format):", type=["docx"])
    if uploaded_file is not None:
        save_path = os.path.join("res", "my_resume.docx")
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Resume uploaded successfully!")
        portfolio.file_path = save_path

    url_input = st.text_input("Enter a URL:", value="")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                relevant_skills = portfolio.query_skills(skills)
                email = llm.write_mail(job, relevant_skills, portfolio.name, portfolio.contact)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator")
    create_streamlit_app(chain, portfolio, clean_text)
