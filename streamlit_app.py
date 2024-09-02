import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

# Show title and description.
st.title("💬 Intelligent Data Analysis with PandasAI")
st.write(
    "This chatbot uses PandasAI and OpenAI's GPT-4 model to analyze your data in a more intelligent way."
)

# Load the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["openai"]["openai_api_key"]

# Initialize PandasAI with OpenAI
llm = OpenAI(api_token=openai_api_key)
pandas_ai = PandasAI(llm)

# Load the CSV data
data = pd.read_csv("health_systems_data.csv")

# Display the first 10 rows of the dataset as a preview
st.write("Here is a preview of the first 10 rows of the dataset:")
st.dataframe(data.head(10))

# Create a chat input field to allow the user to enter a message.
if prompt := st.chat_input("Ask a question about the data:"):

    # Process the prompt using PandasAI
    try:
        result = pandas_ai.run(data, prompt)
        response_message = f"The result of your query is:\n{result}"
    except Exception as e:
        response_message = f"Sorry, I encountered an error while processing your request:\n{e}"

    # Display the result or error in the chat
    st.write(response_message)
