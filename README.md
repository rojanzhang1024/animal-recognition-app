# 动物识别 App (Animal Recognition)

基于 Kivy + TensorFlow Lite 的跨平台动物识别应用，支持 Android 手机和桌面端运行。

## 功能

- **拍照识别**：调用手机相机拍照，实时识别动物种类
- **相册选择**：从相册选取图片进行识别（桌面端）
- **中文显示**：识别结果以中文展示
- **多平台支持**：Android + Windows 均可运行

## 技术栈

| 组件 | 技术 |
|------|------|
| 界面框架 | Kivy |
| 图像识别 | TensorFlow Lite (MobileNetV2) |
| Android API | Pyjnius |
| 原生库 | TFLite C API (ctypes) |
| 打包工具 | Buildozer |
| 图像处理 | Pillow |

## 项目结构
animal/ 
├── main.py # 应用主程序 
├── tflite_c_api.py # TFLite C API 封装 (Android) 
├── resnet50.tflite # 预训练模型文件 
├── buildozer.spec # Android 打包配置 
├── libs/android-v8/ 
│ └── libtensorflowlite_jni.so 
└── README.md


## 运行方式

### 桌面端 
 pip install kivy pillow python main.py


### Android 打包 
 pip install buildozer cd ~/animalv2 buildozer -v android debug


## 使用方法

1. 点击拍照按钮，允许相机权限
2. 对准动物拍照
3. 点击识别按钮查看结果

## 常见问题

- **找不到 .so 文件**：检查 libs/android-v8/ 目录
- **识别结果乱码**：桌面端自动加载系统中文字体
- **识别不准**：可通过迁移学习自定义训练

## 自定义训练

1. 准备训练数据（每类至少 30 张）
2. 运行 train_model.py
3. 导出 TFLite 模型替换 resnet50.tflite
4. 更新 main.py 中的 NUM_CLASSES

## 许可证

本项目仅供学习参考使用。 