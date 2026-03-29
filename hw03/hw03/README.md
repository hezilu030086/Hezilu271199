# 人脸识别系统 (HW03)

基于 `face_recognition` 和 `Streamlit` 的人脸检测与识别 Web 应用。

## 项目结构

```
hw03/
├── app.py                  # Streamlit 主应用入口
├── src/
│   ├── __init__.py
│   ├── face_detect.py      # 人脸检测、特征编码、结果绘制
│   └── face_db.py          # 已知人脸库加载与管理
├── known_faces/            # 已知人脸图片目录（文件名 = 人名）
├── tests/
├── requirements.txt        # Python 依赖
└── README.md
```

## 功能说明

### 人脸检测
- 上传任意图片，自动检测所有人脸位置
- 使用 HOG 模型进行人脸定位
- 提取 128 维人脸特征编码

### 人脸识别
- 将检测到的人脸与 `known_faces/` 目录中的已知人脸进行比对
- 显示匹配的身份和置信度
- 支持可调节的识别阈值

### Web 界面
- 支持上传 JPG、PNG、BMP、WebP 格式图片
- 人脸边界框绘制与标签显示
- 多人脸检测支持
- 详细的人脸信息卡片（身份、置信度、位置、尺寸）
- 128 维特征向量查看

## 环境配置与运行

### 1. 安装系统依赖

`face_recognition` 底层依赖 `dlib`，需要先安装 CMake：

**Windows:**
```bash
pip install cmake
pip install dlib
```

**macOS:**
```bash
brew install cmake
```

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 准备已知人脸库（可选）

将人脸照片放入 `known_faces/` 目录，**文件名即为该人的名字**：

```
known_faces/
    张三.jpg
    李四.png
    Alice.jpg
```

每张图片应包含且仅包含一张清晰正脸。

### 4. 运行应用

```bash
streamlit run app.py
```

应用启动后，浏览器会自动打开，默认地址为 `http://localhost:8501`。

## 使用方法

1. 打开 Web 界面
2. 点击「上传图片」选择一张包含人脸的图片
3. 系统自动进行人脸检测与识别
4. 左侧查看标注后的图片，右侧查看每张人脸的详细信息
5. 可在侧边栏调整识别阈值参数

## 技术栈

| 组件 | 说明 |
|------|------|
| face_recognition | 基于 dlib 的人脸检测与128维特征编码 |
| Streamlit | Web 界面框架 |
| Pillow | 图片处理与标注绘制 |
| NumPy | 数值计算 |
| OpenCV | 图像处理辅助 |
