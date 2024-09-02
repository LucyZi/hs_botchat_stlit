import streamlit as st
import pandas as pd
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-4 model to generate responses."
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

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Ask a question about the data or anything else:"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API with additional context about the data
    messages = [
        {"role": "system", "content": "You are a data expert who can help answer questions about a dataset."},
        {"role": "system", "content": f"The dataset contains the following columns: {', '.join(data.columns)}"},
        {"role": "system", "content": "Please answer the user's question based on the dataset or provide insights where possible."},
    ] + st.session_state.messages

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150,  # Adjust the max_tokens if needed
    )

    # Display the response in the chat
    assistant_message = response.choices[0].message.content  # Update this line
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
