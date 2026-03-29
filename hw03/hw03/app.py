"""基于 face_recognition 和 Streamlit 的人脸识别系统。"""

import numpy as np
import streamlit as st
from PIL import Image

from src.face_db import load_known_faces
from src.face_detect import detect_faces, draw_results, recognize_faces

# ── 页面配置 ──────────────────────────────────────────────
st.set_page_config(
    page_title="人脸识别系统 - HW03",
    page_icon=":bust_in_silhouette:",
    layout="wide",
)

# ── 自定义样式 ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .face-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #4ECDC4;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── 标题 ──────────────────────────────────────────────────
st.markdown("<h1 class='main-header'>人脸识别系统</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "基于 face_recognition 与 Streamlit | HW03 人工智能通识课程作业"
    "</p>",
    unsafe_allow_html=True,
)

st.divider()


# ── 加载已知人脸库（缓存） ─────────────────────────────────
@st.cache_resource
def get_known_faces():
    return load_known_faces("known_faces")


known_encodings, known_names = get_known_faces()

# ── 侧边栏 ────────────────────────────────────────────────
with st.sidebar:
    st.header("设置")

    st.subheader("已知人脸库")
    if known_names:
        st.success(f"已加载 {len(known_names)} 张已知人脸")
        for name in known_names:
            st.write(f"  - {name}")
    else:
        st.info("未加载已知人脸。将 人脸图片 放入 `known_faces/` 目录，文件名即为人名。")

    st.divider()

    st.subheader("检测参数")
    tolerance = st.slider(
        "识别阈值（越小越严格）",
        min_value=0.2,
        max_value=0.7,
        value=0.45,
        step=0.05,
        help="人脸距离小于此值时判定为匹配",
    )

    st.divider()
    st.subheader("使用说明")
    st.markdown(
        """
        1. 上传一张包含人脸的图片
        2. 系统自动检测所有人脸
        3. 若 `known_faces/` 中有已知人脸，将进行身份识别
        4. 查看检测框和识别结果
        """
    )

# ── 图片上传 ───────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "上传图片",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    help="支持 JPG、PNG、BMP、WebP 格式",
)

if uploaded_file is not None:
    # 读取图片
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    # ── 检测人脸 ───────────────────────────────────────────
    with st.spinner("正在检测人脸..."):
        faces = detect_faces(image_array)
        faces = recognize_faces(faces, known_encodings, known_names, tolerance)

    # ── 统计指标 ───────────────────────────────────────────
    num_faces = len(faces)
    num_recognized = sum(1 for f in faces if f.get("name") != "未知")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("检测到的人脸数", num_faces)
    with col_m2:
        st.metric("已识别", num_recognized)
    with col_m3:
        st.metric("未识别", num_faces - num_recognized)

    st.divider()

    # ── 结果展示 ───────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("检测结果")
        if faces:
            result_image = draw_results(image, faces)
            st.image(result_image, use_container_width=True)
        else:
            st.image(image, use_container_width=True)
            st.warning("未检测到人脸，请尝试其他图片。")

    with col_right:
        st.subheader("人脸详情")
        if faces:
            for i, face in enumerate(faces):
                top, right, bottom, left = face["location"]
                name = face.get("name", "未知")
                confidence = face.get("confidence", 0)

                with st.container():
                    st.markdown(
                        f"""
                        <div class='face-card'>
                            <strong>人脸 #{i + 1}</strong><br>
                            身份: <b>{name}</b><br>
                            置信度: <b>{confidence:.0%}</b><br>
                            位置: ({left}, {top}) → ({right}, {bottom})<br>
                            尺寸: {right - left} × {bottom - top} px
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # ── 特征编码展示 ───────────────────────────────
            with st.expander("查看人脸特征编码（128维向量）"):
                for i, face in enumerate(faces):
                    st.write(f"**人脸 #{i + 1}** 的特征向量：")
                    st.code(
                        np.array2string(face["encoding"], precision=4, separator=", "),
                        language=None,
                    )
        else:
            st.info("暂无检测结果。")

    # ── 原图对比 ───────────────────────────────────────────
    with st.expander("查看原图"):
        st.image(image, caption="原始上传图片", use_container_width=True)

else:
    # ── 欢迎页面 ───────────────────────────────────────────
    st.markdown(
        """
        <div style='text-align:center; padding: 60px 20px; color: #888;'>
            <h3>请上传一张图片开始人脸检测</h3>
            <p>支持 JPG、PNG、BMP、WebP 格式</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── 页脚 ──────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray; font-size:0.85rem;'>"
    "HW03 人脸识别系统 | 基于 face_recognition + Streamlit"
    "</p>",
    unsafe_allow_html=True,
)
