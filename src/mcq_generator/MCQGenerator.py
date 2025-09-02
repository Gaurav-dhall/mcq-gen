import os 
import json 
import pandas as pd 
import traceback
from dotenv import load_dotenv
load_dotenv()
from src.mcq_generator.logger import logging
from src.mcq_generator.utils import get_table_data,read_file


from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import PyPDF2
from langchain_groq import ChatGroq

llm = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0.7)


Template="""
Text:{text}
You are an expert mcq generator.Given the above text it is ur job to generate a quiz of {number} multiple choice questions for the {subject} students in {tone} tone. Make sure the questions are not repeated and check all the questions to be conforming the text as well. make sure to format the response like Response_JSON below to use it as a guide 
Ensure to make {number} mcq questions and not more than that.
###Response_JSON
{response_json}
"""

quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","tone","subject","response_json"],
    template=Template
)

quiz_chain= LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key="quiz",
    verbose=True

)


Template2="""
    You are an expert english grammarian and writer Given A MCQ quiz for {subject} students.You need to evaluatethe complexity of the question and give a complete analysis of the quiz only use at max 50 words for complexity if the quiz is not as per the cognitive and analytical abilities of the students update the quiz questions which needs to be changed and change tone such that it perfectly fits the students abilities 
    QQuiz Mcqs:{quiz}

    Check from an expert english writer of the above quiz :
    """


quiz_evaluation_prompt=PromptTemplate(
    input_variables=["quiz","subject"],
    template=Template2
)

review_chain=LLMChain(
    llm=llm,
    prompt=quiz_evaluation_prompt,
    output_key="review",
    verbose=True
)

generate_evaluated_chain=SequentialChain(
    chains=[quiz_chain,review_chain],
    input_variables=["text","number","tone","subject","response_json"],
    output_variables=["quiz","review"],
    verbose=True
)