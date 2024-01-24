
import pandas as pd
import streamlit as st
from datasets import load_dataset
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 加载问答数据集
@st.cache_data
def load_qa_dataset(dataset_name, split):
    try:
        dataset = load_dataset(dataset_name, split=split)
        return dataset
    except Exception as e:
        st.error(e)
        return None

# 加载多模态数据集
@st.cache_data
def load_mm_dataset(dataset_name, split):
    try:
        dataset = load_dataset(dataset_name, split=split)
        return dataset
    except Exception as e:
        st.error(e)
        return None

# 生成词云
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400).generate(text)
    return wordcloud

def display_wordcloud(wordcloud):
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# 主界面
def main():
    st.title("Huggingface Dataset Viewer")
    st.sidebar.title("Options")

    # 对话的图标
    user_avatar = "🧑‍💻"
    robot_avatar = "🤖"

    # 初始化消息列表和当前索引
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # 选择数据集类型
    dataset_type = st.sidebar.selectbox("Select Dataset Type", ["Question-Answering", "Multimodal"])

    # 选择数据集名称
    if dataset_type == "Question-Answering":
        dataset_name = st.sidebar.text_input("Enter QA Dataset Name", "squad")
    else:
        dataset_name = st.sidebar.text_input("Enter Multimodal Dataset Name", "coco")

    # 获取数据集元信息
    try:
        dataset_info = load_dataset(dataset_name, split=None)
        available_splits = list(dataset_info.keys())
    except Exception as e:
        st.error(e)
        return None

    # 选择数据集分割
    split = st.sidebar.selectbox("Select Dataset Split", available_splits)

    # 根据选择的数据集类型加载数据
    if dataset_type == "Question-Answering":
        dataset = load_qa_dataset(dataset_name, split)
    else:
        dataset = load_mm_dataset(dataset_name, split)

    if dataset is not None:
        # 显示数据集大小
        st.write(f"Dataset Size: {len(dataset)}")
    else:
        return st.error(f"Dataset '{dataset_name}' not found. Please check the dataset name and try again.")

    # 控制数据集索引
    index = st.sidebar.number_input("Index", min_value=0, max_value=len(dataset)-1, step=1, value=st.session_state.current_index)

    # 如果索引改变，更新对话记录
    if st.session_state.current_index != index:
        st.session_state.current_index = index
        st.session_state.messages = []

    # 显示选择的数据
    data = dataset[index]
    if dataset_type == "Question-Answering":
        st.write(f"Dataset Keys: {list(data.keys())}")  # 添加这行来显示数据集的键值结构
        if 'context' in data:
            st.text_area("Context", value=data['context'], height=200)
            st.write("---")
        if 'query' in data:
            question = data['query']
        elif 'question' in data:
            question = data['question']
        else:
            question = ''
        # if question:
            # st.write(f"Question: {question}")

        if 'options' in data:
            st.write("Options:")
            for idx, option in enumerate(data['options']):
                st.write(f"{idx + 1}. {option}")

        if 'correct_option' in data:
            answers = [data['options'][data['correct_option'] - 1]]
        elif 'answers' in data:
            answers = data['answers']['text']
        else:
            answers = []

        # 更新对话记录
        if not st.session_state.messages:
            st.session_state.messages.append({"role": "user", "content": question, "avatar": user_avatar})
            st.session_state.messages.append({"role": "robot", "content": answers[0], "avatar": robot_avatar})

        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message.get("avatar")):
                st.markdown(message["content"])

        # 是否生成并显示词云
        show_wordcloud = st.sidebar.checkbox("Show Word Cloud")
        if show_wordcloud and dataset_type == "Question-Answering":
            text = " ".join([data['context'] for data in dataset])
            wordcloud = generate_wordcloud(text)
            display_wordcloud(wordcloud)

if __name__ == "__main__":
    main()