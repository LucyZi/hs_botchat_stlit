import streamlit as st
import openai
import pandas as pd
import plotly.express as px
import os
import time

# Set up page configuration
st.set_page_config(
    page_title="Healthcare Systems Data Chat",
    page_icon="🏥",
    layout="wide",
)

# Set OpenAI API key
openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key is not set. Please set it in your Streamlit secrets or as an environment variable.")
    st.stop()

# 设置 OpenAI API 密钥
openai.api_key = openai_api_key

# Load CSV data
@st.cache_data
def load_data():
    return pd.read_csv('health_systems_data.csv')

df = load_data()

# Display title and description
st.title("🏥 Healthcare Systems Data Chat")
st.write(
    "This chatbot uses OpenAI's GPT-3.5 model to analyze healthcare systems data. "
    "You can ask questions about the data, and the AI will provide insights based on the available information."
)

# Create session state variable to store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display sample prompts
with st.expander("Sample prompts", expanded=True):
    st.write(
        """
        - What kind of information is in this dataset?
        - What are the main trends in healthcare systems?
        - How does the data vary across different regions?
        - What are the key performance indicators for healthcare systems?
        - Can you provide a summary of the healthcare system efficiency?
        """
    )

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create chat input field
if prompt := st.chat_input("Ask about the healthcare systems data..."):
    # Store and display the current prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Use OpenAI API to generate a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant analyzing healthcare systems data. Use the provided data to answer questions accurately."},
        {"role": "user", "content": f"Here's a summary of the data:\n{df.describe().to_string()}\n\nNow, answer this question: {prompt}"}
    ] + st.session_state.messages[-5:]  # Limit message history

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        # Extract and display the assistant's response
        assistant_message = response.choices[0].message["content"]
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    except openai.error.OpenAIError as e:
        st.error(f"OpenAI API Error: {str(e)}")
        time.sleep(5)  # Optional: Add a delay before retrying

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Add data preview feature
if st.checkbox("Show data preview"):
    st.write(df.head())

# Add data visualization feature
if st.checkbox("Show data visualization"):
    st.write("Select columns for visualization:")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    selected_columns = st.multiselect("Choose columns", numeric_columns)
    if selected_columns:
        fig = px.line(df, y=selected_columns)
        st.plotly_chart(fig)
