import os
import json
import numpy as np
from labelme.utils import shapes_to_label
from PIL import Image

def json_to_tiff_mask(json_file_path, output_folder):
    # 读取 JSON 文件
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # 获取图像的高度和宽度
    image_height = data['imageHeight']
    image_width = data['imageWidth']

    # 获取所有标注的形状
    shapes = data['shapes']

    # 获取所有标签名称
    label_name_to_value = {'_background_': 0}
    for shape in shapes:
        label_name = shape['label']
        if label_name not in label_name_to_value:
            label_name_to_value[label_name] = len(label_name_to_value)

    # 将标注形状转换为标签掩码
    result = shapes_to_label(
        img_shape=(image_height, image_width),
        shapes=shapes,
        label_name_to_value=label_name_to_value
    )

    # 检查返回值是否为元组
    if isinstance(result, tuple):
        # 假设第一个元素是所需的标签掩码
        label = result[0]
    else:
        label = result

    # 生成 TIFF 格式的掩码文件路径
    json_file_name = os.path.basename(json_file_path)
    base_name = os.path.splitext(json_file_name)[0]
    output_file_path = os.path.join(output_folder, f'{base_name}_mask.tiff')

    # 使用 Pillow 库保存 TIFF 格式的掩码
    label_image = Image.fromarray(label.astype(np.uint8))
    label_image.save(output_file_path)

    print(f"Mask saved to: {output_file_path}")

# JSON 文件所在文件夹路径
json_folder = r"C:\Users\18281\OneDrive\Desktop\label"
# 输出文件夹路径
output_folder = r"C:\Users\18281\OneDrive\Desktop\label"

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历 JSON 文件夹中的所有 JSON 文件
for root, dirs, files in os.walk(json_folder):
    for file in files:
        if file.endswith('.json'):
            json_file_path = os.path.join(root, file)
            json_to_tiff_mask(json_file_path, output_folder)
