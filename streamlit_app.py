import streamlit as st
import pandas as pd
from openai import OpenAI

# Show title and description.
st.title("💬 Health Systems Data Chatbot")
st.write(
    "This chatbot uses OpenAI's GPT-3.5 model to generate responses based on your CSV data. "
    "Please provide your OpenAI API key to continue."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Load the CSV data
    csv_path = 'health_systems_data.csv'  # Path to your CSV file in the same directory
    df = pd.read_csv(csv_path)

    # Show the first few rows of the data to the user
    st.write("Here is a preview of the data:")
    st.dataframe(df.head())

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("Ask something about the data"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        response = client.chat_completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        # Display and store the response in session state.
        with st.chat_message("assistant"):
            # Collect the entire response and display it
            response_text = ''.join([chunk['choices'][0]['delta']['content'] for chunk in response])
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
