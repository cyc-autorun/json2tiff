import os
import numpy as np
from PIL import Image


def is_black(pixel):
    """严格匹配纯黑色"""
    return (pixel[0] == 0) and (pixel[1] == 0) and (pixel[2] == 0)


def is_red(pixel):
    """红色范围判断"""
    return (125 <= pixel[0] <= 130) and (pixel[1] <= 5) and (pixel[2] <= 5)


def is_green(pixel):
    """绿色范围判断"""
    return (0 <= pixel[0] <=50) and (80 <= pixel[1] <= 150) and (0 <= pixel[2] <= 50)


def jpg_to_tiff_mask(jpg_path, output_folder):
    # 读取图像
    img = Image.open(jpg_path).convert("RGB")
    rgb_array = np.array(img)

    # 初始化索引矩阵
    h, w = rgb_array.shape[:2]
    index_array = np.zeros((h, w), dtype=np.uint8)

    # 矢量化的颜色判断
    red_mask = np.logical_and(
        np.logical_and(125 <= rgb_array[:, :, 0], rgb_array[:, :, 0] <= 130),
        np.logical_and(rgb_array[:, :, 1] <= 5, rgb_array[:, :, 2] <= 5)
    )

    green_mask = np.logical_and(
        np.logical_and(0 <= rgb_array[:, :, 0], rgb_array[:, :, 0] <= 30),
        np.logical_and(
            np.logical_and(100 <= rgb_array[:, :, 1], rgb_array[:, :, 1] <= 130),
            np.logical_and(0 <= rgb_array[:, :, 2], rgb_array[:, :, 2] <= 10)
        )
    )

    black_mask = np.logical_and(
        np.logical_and(rgb_array[:, :, 0] == 0, rgb_array[:, :, 1] == 0),
        rgb_array[:, :, 2] == 0
    )

    # 优先级：黑色 > 红色 > 绿色
    index_array[black_mask] = 0  # 背景
    index_array[red_mask] = 1  # 红色类别
    index_array[green_mask] = 2  # 绿色类别

    # 创建调色板
    palette = np.zeros(256 * 3, dtype=np.uint8)
    # 索引0: 黑色 (0,0,0)
    # 索引1: 红色 (128,0,0) 使用中间值更易区分
    # 索引2: 绿色 (0,115,5) 使用中间值更易区分
    palette[3:6] = [128, 0, 0]  # 索引1
    palette[6:9] = [0, 115, 5]  # 索引2

    # 转换为调色板模式
    mask_img = Image.fromarray(index_array, mode='P')
    mask_img.putpalette(palette)

    # 保存文件
    output_path = os.path.join(output_folder,
                               os.path.basename(jpg_path).replace('.jpg', '_mask.tiff'))
    mask_img.save(output_path, compression="tiff_lzw")
    print(f"Successfully saved: {output_path}")


# 使用示例
input_folder = r"C:\Users\18281\OneDrive\Desktop\label" #改成自己的输入文件夹
output_folder = r"C:\Users\18281\OneDrive\Desktop\label" #输出文件夹

# 创建输出目录
os.makedirs(output_folder, exist_ok=True)

# 批量处理
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        jpg_path = os.path.join(input_folder, filename)
        jpg_to_tiff_mask(jpg_path, output_folder)