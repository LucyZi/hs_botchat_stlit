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


# 从 Streamlit 的 secrets 中获取 OpenAI API 密钥
openai.api_key = st.secrets["openai"]["openai_api_key"]

# 加载 CSV 数据
@st.cache_data
def load_data():
    df = pd.read_csv('health_systems_data.csv')
    return df

df = load_data()

# 生成基于 CSV 数据的回答
def generate_response(question, df):
    # 将数据框转换为字符串
    data_str = df.to_csv(index=False)

    # 构建 Prompt，提示 GPT 模型数据内容和用户问题
    prompt = f"Here is the data:\n\n{data_str}\n\nBased on this data, please answer the following question:\n\n{question}\n\nAnswer:"
    
    # 使用 OpenAI GPT 模型生成回答
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.2,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].text.strip()

# Streamlit 应用的界面
st.title("Health Systems Data 问答机器人")

st.write("上传的 CSV 数据将用于回答您提出的任何问题。")

question = st.text_input("输入您的问题:")

if question:
    response = generate_response(question, df)
    st.write("回答:")
    st.write(response)

