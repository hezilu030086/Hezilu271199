"""face_detect 模块的基础测试。"""

import numpy as np

from src.face_detect import detect_faces, recognize_faces


def test_detect_faces_no_face():
    """纯色图片应检测不到人脸。"""
    blank = np.zeros((100, 100, 3), dtype=np.uint8)
    faces = detect_faces(blank)
    assert faces == []


def test_recognize_faces_empty_db():
    """已知库为空时，所有人脸应标记为未知。"""
    fake_faces = [
        {"location": (10, 90, 90, 10), "encoding": np.random.rand(128)},
    ]
    result = recognize_faces(fake_faces, [], [], tolerance=0.45)
    assert len(result) == 1
    assert result[0]["name"] == "未知"
    assert result[0]["confidence"] == 0.0


def test_recognize_faces_match():
    """编码完全相同时应识别成功。"""
    encoding = np.random.rand(128)
    fake_faces = [
        {"location": (10, 90, 90, 10), "encoding": encoding.copy()},
    ]
    result = recognize_faces(fake_faces, [encoding], ["Alice"], tolerance=0.5)
    assert result[0]["name"] == "Alice"
    assert result[0]["confidence"] > 0.5
