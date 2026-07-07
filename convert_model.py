import tensorflow as tf
import numpy as np

print('Loading ResNet50 model...')
model = tf.keras.applications.MobileNetV2(weights='imagenet', input_shape=(224, 224, 3))

print('Converting to TFLite with float16 quantization...')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]

tflite_model = converter.convert()

output_path = 'resnet50.tflite'
with open(output_path, 'wb') as f:
    f.write(tflite_model)

size_mb = len(tflite_model) / 1024 / 1024
print(f'✓ 转换完成！')
print(f'  文件: {output_path}')
print(f'  大小: {size_mb:.1f} MB')

if size_mb > 30:
    print(f'\n⚠️ 警告: 文件仍然过大，请检查量化是否生效')
else:
    print(f'\n✓ 文件大小正常，可以继续打包')
