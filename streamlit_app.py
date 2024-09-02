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

    # Prepare a context for the model that describes the dataset
    context = (
        "You are a data expert. You have access to the following dataset. "
        "Here are the columns of the dataset: "
        f"{', '.join(data.columns)}. "
        "The user may ask questions related to this dataset or anything else. "
        "If the question is about the dataset, try to derive the answer from the data "
        "directly or give an appropriate suggestion on how to get the answer."
    )

    # Combine the context with the user messages
    messages = [{"role": "system", "content": context}] + st.session_state.messages

    # Generate a response using the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=200,  # Adjust max tokens as needed
    )

    # Display the response in the chat
    assistant_message = response.choices[0].message['content']
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
