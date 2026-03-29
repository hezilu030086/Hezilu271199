"""人脸检测模块：使用 face_recognition 进行人脸检测与特征编码。"""

import face_recognition
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def detect_faces(image_array: np.ndarray) -> list[dict]:
    """检测图片中的所有人脸，返回位置和128维特征编码。

    Args:
        image_array: RGB 格式的 numpy 数组图片。

    Returns:
        包含每张人脸信息的列表，每个元素为 dict:
            - location: (top, right, bottom, left) 人脸边界框
            - encoding: 128维人脸特征向量
    """
    locations = face_recognition.face_locations(image_array, model="hog")
    encodings = face_recognition.face_encodings(image_array, locations)

    faces = []
    for loc, enc in zip(locations, encodings):
        faces.append({"location": loc, "encoding": enc})
    return faces


def recognize_faces(
    faces: list[dict],
    known_encodings: list[np.ndarray],
    known_names: list[str],
    tolerance: float = 0.45,
) -> list[dict]:
    """将检测到的人脸与已知人脸库进行比对识别。

    Args:
        faces: detect_faces 的返回结果。
        known_encodings: 已知人脸的特征编码列表。
        known_names: 已知人脸对应的名字列表。
        tolerance: 匹配阈值，越小越严格（默认 0.45）。

    Returns:
        在每个 face dict 中添加:
            - name: 识别出的名字，未识别为 "未知"
            - confidence: 置信度（0~1，越高越相似）
    """
    for face in faces:
        if not known_encodings:
            face["name"] = "未知"
            face["confidence"] = 0.0
            continue

        distances = face_recognition.face_distance(known_encodings, face["encoding"])
        best_idx = int(np.argmin(distances))
        best_distance = distances[best_idx]

        if best_distance <= tolerance:
            face["name"] = known_names[best_idx]
            face["confidence"] = round(1.0 - best_distance, 2)
        else:
            face["name"] = "未知"
            face["confidence"] = round(1.0 - best_distance, 2)

    return faces


def draw_results(image: Image.Image, faces: list[dict]) -> Image.Image:
    """在图片上绘制人脸检测框和识别标签。

    Args:
        image: PIL Image 对象。
        faces: 包含 location、name、confidence 的人脸列表。

    Returns:
        绘制了标注的 PIL Image。
    """
    draw_img = image.copy()
    draw = ImageDraw.Draw(draw_img)

    try:
        font = ImageFont.truetype("msyh.ttc", 18)
    except OSError:
        try:
            font = ImageFont.truetype("simhei.ttf", 18)
        except OSError:
            font = ImageFont.load_default()

    colors = [
        "#FF4B4B", "#4ECDC4", "#45B7D1", "#96CEB4",
        "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F",
    ]

    for i, face in enumerate(faces):
        top, right, bottom, left = face["location"]
        color = colors[i % len(colors)]

        # 绘制边界框
        draw.rectangle([left, top, right, bottom], outline=color, width=3)

        # 构建标签文本
        name = face.get("name", "人脸")
        confidence = face.get("confidence")
        if confidence is not None and name != "未知":
            label = f"{name} ({confidence:.0%})"
        elif confidence is not None:
            label = f"{name} ({confidence:.0%})"
        else:
            label = name

        # 绘制标签背景和文字
        bbox = font.getbbox(label)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        label_y = top - text_h - 8 if top - text_h - 8 > 0 else bottom + 4
        draw.rectangle(
            [left, label_y, left + text_w + 8, label_y + text_h + 6],
            fill=color,
        )
        draw.text((left + 4, label_y + 2), label, fill="white", font=font)

    return draw_img
