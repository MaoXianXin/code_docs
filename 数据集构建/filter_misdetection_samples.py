import os
import shutil
import xml.etree.ElementTree as ET
import argparse

"""
python filter_misdetection_samples.py \
    --root_dir "/home/mao/workspace/yolov5/runs/detect/exp/origin" \
    --dest_dir "/home/mao/workspace/yolov5/runs/detect/exp/filter_misdetection" \
    --categories "年" \
    --categories "月" \
    --categories "日" \
    --categories "号码上" \
    --categories "号码下" \
    --categories "出票人账号" \
    --categories "小写金额"
"""

# 设置 argparse
parser = argparse.ArgumentParser(description='处理XML文件并根据缺失类别移动文件。')
parser.add_argument('--root_dir', type=str, required=True, help='源目录路径')
parser.add_argument('--dest_dir', type=str, required=True, help='目标目录路径')
parser.add_argument('--categories', action='append', required=True, help='需要检查的类别列表')

args = parser.parse_args()

# 使用 argparse 解析的参数
root_dir = args.root_dir
dest_dir = args.dest_dir
categories = args.categories

# 确保目标目录存在
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# 遍历root_dir下的所有文件
for dir_path, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.xml'):  # 找到xml文件
            xml_path = os.path.join(dir_path, file)
            tree = ET.parse(xml_path)
            xml_root = tree.getroot()  # 使用xml_root代替之前的root

            # 提取xml文件中的所有类别
            found_categories = [obj.find('name').text for obj in xml_root.findall('object')]

            # 检查是否每个类别都被找到
            if not all(category in found_categories for category in categories):
                # 类别缺失，拷贝对应的jpg和xml文件到dest_dir
                base_name, _ = os.path.splitext(file)
                jpg_file = base_name + '.jpg'
                jpg_path = os.path.join(dir_path, jpg_file)

                # 检查jpg文件是否存在
                if os.path.exists(jpg_path):
                    shutil.copy(jpg_path, dest_dir)
                shutil.copy(xml_path, dest_dir)

                print(f"Copied missing category files: {jpg_file} and {file}")
