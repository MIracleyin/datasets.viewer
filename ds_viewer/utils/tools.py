import os
import streamlit as st

def get_files(folder_path, supported_formats):
    '''
    获取文件
    :param folder_path:
    :param supported_formats:
    :return:
    '''
    files = os.listdir(folder_path)
    return [file for file in files if any(file.endswith(fmt) for fmt in supported_formats)]

def load_images(image_folder_path, image_index):
    if not image_folder_path:
        st.warning("请输入图像文件夹路径。")
        return None

    images = get_files(image_folder_path, [".jpg", ".png", ".jpeg", ".bmp", ".tiff"])
    if not images:
        st.warning("图像文件夹中没有找到支持的图像格式。请检查路径和图像格式。")
        return None

    image_file = st.sidebar.selectbox("选择图像文件:", images, index=image_index)
    return image_file