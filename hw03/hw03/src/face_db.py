"""已知人脸库管理：加载 known_faces/ 目录中的人脸图片并编码。"""

import os
import face_recognition
import numpy as np


def load_known_faces(known_faces_dir: str = "known_faces") -> tuple[list[np.ndarray], list[str]]:
    """从目录加载已知人脸，文件名（不含扩展名）作为人名。

    目录结构示例:
        known_faces/
            张三.jpg
            李四.png
            Alice.jpg

    Args:
        known_faces_dir: 已知人脸图片目录路径。

    Returns:
        (encodings, names) 编码列表和对应名字列表。
    """
    encodings = []
    names = []

    if not os.path.isdir(known_faces_dir):
        return encodings, names

    supported_ext = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    for filename in sorted(os.listdir(known_faces_dir)):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in supported_ext:
            continue

        filepath = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(filepath)
        face_encs = face_recognition.face_encodings(image)

        if face_encs:
            encodings.append(face_encs[0])
            name = os.path.splitext(filename)[0]
            names.append(name)

    return encodings, names
