import streamlit as st
import pandas as pd
from openai import OpenAI

# Show title and description.
st.title("💬 Intelligent Data Analysis Chatbot")
st.write(
    "This chatbot uses OpenAI's GPT-4 model combined with Python's data analysis capabilities to answer your questions."
)

# Load the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["openai"]["openai_api_key"]

# Load the CSV data
data = pd.read_csv("health_systems_data.csv")

# Display the first 10 rows of the dataset as a preview
st.write("Here is a preview of the first 10 rows of the dataset:")
st.dataframe(data.head(10))

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages. This ensures that the messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display automatically at the bottom of the page.
if prompt := st.chat_input("Ask a question about the data or anything else:"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Provide context for the model that describes the dataset
    context = (
        "You are a data assistant. The user will ask questions about a dataset. "
        "The dataset has the following columns: " + ", ".join(data.columns) + ". "
        "Your task is to generate a valid Python Pandas command that can be executed "
        "on a dataframe named 'data' to answer the user's question. "
        "If the question involves counting or filtering based on categories, automatically detect the appropriate column "
        "and apply the filtering or counting operation accordingly."
    )

    # Combine the context with the user messages
    messages = [{"role": "system", "content": context}]
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150,
    )

    code = response.choices[0].message.content.strip("```").strip()  # Remove code block formatting if present

    # Display the generated code for debugging purposes
    st.write("Generated code:")
    st.code(code)

    # Automatically correct the code if it doesn't handle categorical filtering properly
    if any(cat in prompt.lower() for cat in data.columns) and "str.contains" not in code:
        for col in data.columns:
            if any(word in prompt.lower() for word in col.lower().split()):
                code = f"result = data[data['{col}'].str.contains('{prompt.split()[-1]}', case=False)].shape[0]"
                break

    # Try to execute the generated code and capture the result
    try:
        result = eval(code)
        response_message = f"The result of your query is:\n{result}"
    except Exception as e:
        response_message = f"Sorry, I encountered an error while processing your request:\n{e}"

    # Display the result or error in the chat
    st.session_state.messages.append({"role": "assistant", "content": response_message})
    with st.chat_message("assistant"):
        st.markdown(response_message)
