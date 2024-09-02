import streamlit as st
import pandas as pd
from openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI as LangChainOpenAI

# Show title and description
st.title("💬 Intelligent Data Analysis Chatbot with LangChain")
st.write(
    "This chatbot uses LangChain combined with OpenAI's GPT-4 model to analyze your data intelligently."
)

# Load the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["openai"]["openai_api_key"]

# Load the CSV data
data = pd.read_csv("health_systems_data.csv")

# Display the first 10 rows of the dataset as a preview
st.write("Here is a preview of the first 10 rows of the dataset:")
st.dataframe(data.head(10))

# Initialize LangChain's OpenAI LLM
llm = LangChainOpenAI(openai_api_key=openai_api_key)

# Define a prompt template for generating Pandas code
template = """You are an expert in data analysis. A user has asked you a question about the following dataset:
{data_description}
Please generate a valid Python Pandas code to answer the user's question: "{user_question}"
The dataset is stored in a Pandas DataFrame called 'data'.
Return only the Python code, no explanations.
"""

# Create a LangChain prompt
prompt = PromptTemplate(input_variables=["data_description", "user_question"], template=template)

# Create an LLMChain for generating code
chain = LLMChain(llm=llm, prompt=prompt)

# Create a chat input field to allow the user to enter a message
if prompt_text := st.chat_input("Ask a question about the data:"):

    # Describe the dataset columns
    data_description = ", ".join(data.columns)

    # Generate the Pandas code using LangChain
    generated_code = chain.run(data_description=data_description, user_question=prompt_text)

    st.write("Generated code:")
    st.code(generated_code)

    try:
        # Execute the generated code and show the result
        result = eval(generated_code)
        st.write("Result:")
        st.write(result)
    except Exception as e:
        st.write(f"An error occurred: {e}")
