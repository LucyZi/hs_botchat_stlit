import streamlit as st
import pandas as pd
import openai
import time
from openai.error import RateLimitError, OpenAIError

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Set the OpenAI API key
    openai.api_key = openai_api_key

    # Load the CSV file
    try:
        data = pd.read_csv("health_systems_data.csv")
        st.write("### Health Systems Data", data)
    except FileNotFoundError:
        st.error("The file 'health_systems_data.csv' was not found. Please ensure it is in the correct directory.")

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        try:
            response = None
            retry_count = 0
            while retry_count < 5:
                try:
                    stream = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = ""
                    for message in stream:
                        content = message['choices'][0]['delta'].get('content', '')
                        response += content
                        st.chat_message("assistant").markdown(content)
                    break
                except RateLimitError:
                    retry_count += 1
                    st.warning("Rate limit reached. Retrying...")
                    time.sleep(2 ** retry_count)
                except OpenAIError as e:
                    st.error(f"An error occurred: {e}")
                    break

            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"An error occurred: {e}")
