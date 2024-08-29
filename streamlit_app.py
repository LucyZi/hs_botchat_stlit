import streamlit as st
from openai import OpenAI, error
import pandas as pd
import plotly.express as px
import os
import time

# 设置页面配置
st.set_page_config(
    page_title="Healthcare Systems Data Chat",
    page_icon="🏥",
    layout="wide",
)

# 设置OpenAI API密钥
openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key is not set. Please set it in your Streamlit secrets or as an environment variable.")
    st.stop()

# 创建OpenAI客户端
client = OpenAI(api_key=openai_api_key)

# 加载CSV数据
@st.cache_data
def load_data():
    # 假设您的CSV文件名为'health_systems_data.csv'
    return pd.read_csv('health_systems_data.csv')

df = load_data()

# 显示标题和描述
st.title("🏥 Healthcare Systems Data Chat")
st.write(
    "This chatbot uses OpenAI's GPT-3.5 model to analyze healthcare systems data. "
    "You can ask questions about the data, and the AI will provide insights based on the available information."
)

# 创建会话状态变量来存储聊天消息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示示例提示
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

# 显示现有的聊天消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 创建聊天输入字段
if prompt := st.chat_input("Ask about the healthcare systems data..."):
    # 存储并显示当前提示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 使用OpenAI API生成响应
    messages = [
        {"role": "system", "content": "You are a helpful assistant analyzing healthcare systems data. Use the provided data to answer questions accurately."},
        {"role": "user", "content": f"Here's a summary of the data:\n{df.describe().to_string()}\n\nNow, answer this question: {prompt}"}
    ] + st.session_state.messages[-5:]  # 限制消息历史

    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ],
            stream=True,
        )
        
        # 将响应流式传输到聊天中
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    except error.RateLimitError:
        st.error("API rate limit exceeded. Please try again later.")
        time.sleep(5)  # 可选：在重试前添加延迟

# 添加数据预览功能
if st.checkbox("Show data preview"):
    st.write(df.head())

# 添加数据可视化功能
if st.checkbox("Show data visualization"):
    st.write("Select columns for visualization:")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    selected_columns = st.multiselect("Choose columns", numeric_columns)
    if selected_columns:
        fig = px.line(df, y=selected_columns)
        st.plotly_chart(fig)
