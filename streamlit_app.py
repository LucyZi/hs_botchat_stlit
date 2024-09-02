import streamlit as st
import pandas as pd
import openai

# 显示标题和描述
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-4 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# 让用户通过 `st.text_input` 输入他们的 OpenAI API 密钥
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # 设置 OpenAI API 密钥
    openai.api_key = openai_api_key

    # 加载 CSV 文件
    try:
        data = pd.read_csv("health_systems_data.csv")
        st.write("### Health Systems Data", data)
    except FileNotFoundError:
        st.error("The file 'health_systems_data.csv' was not found. Please ensure it is in the correct directory.")

    # 创建一个会话状态变量来存储聊天消息
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示已有的聊天消息
    for message in st.session_state.messages:
        st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

    # 创建一个聊天输入字段
    if prompt := st.text_input("Enter your question:"):
        # 存储并显示当前的用户输入
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f"**User:** {prompt}")

        # 使用 OpenAI API 生成响应
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # 使用 GPT-4 模型
                messages=st.session_state.messages,
            )

            assistant_message = response['choices'][0]['message']['content']
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            st.markdown(f"**Assistant:** {assistant_message}")

        except openai.error.OpenAIError as e:  # 捕获所有OpenAI API相关异常
            st.error(f"OpenAI API Error: {e}")
        except Exception as e:  # 捕获其他异常
            st.error(f"An unexpected error occurred: {e}")
