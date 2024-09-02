import streamlit as st
import pandas as pd
import openai

# Show title and description.
st.title("💬 Health Systems Data Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses based on your CSV data. "
    "To use this app, you need to provide an OpenAI API key."
)

# Ask user for their OpenAI API key via st.text_input.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Initialize OpenAI API client with the API key
    openai.api_key = openai_api_key

    # Load the CSV data
    csv_path = 'health_systems_data.csv'  # Path to your CSV file in the same directory
    df = pd.read_csv(csv_path)

    # Show the first few rows of the data to the user
    st.write("Here is a preview of the data:")
    st.dataframe(df.head())

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via st.chat_message.
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
        df_description = df.describe().to_string()
        response_prompt = f"The user asked: {prompt}\nHere is a brief description of the data:\n{df_description}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can answer questions based on the data provided."},
                {"role": "user", "content": response_prompt}
            ]
        )

        # Stream the response to the chat using st.write_stream, then store it in session state.
        assistant_message = response.choices[0].message["content"]
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
