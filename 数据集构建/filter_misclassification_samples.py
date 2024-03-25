import os
import shutil
import xml.etree.ElementTree as ET
from collections import Counter
import argparse  # 导入argparse库

"""
python filter_misclassification_samples.py \
    --root_dir /home/mao/workspace/yolov5/runs/detect/exp/origin \
    --dest_dir /home/mao/workspace/yolov5/runs/detect/exp/filter_misclassification
"""

def find_files(root_dir, extensions):
    """
    遍历root_dir，找到所有具有指定扩展名的文件。
    """
    files = []
    for root, dirs, files_in_dir in os.walk(root_dir):
        for file in files_in_dir:
            if file.endswith(extensions):
                files.append(os.path.join(root, file))
    return files

def parse_xml_and_count_labels(xml_file):
    """
    解析XML文件，统计每个label_name的出现次数。
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    labels = [obj.find('name').text for obj in root.findall('object')]
    label_counts = Counter(labels)
    return label_counts

def copy_files_if_condition_met(xml_files, dest_dir):
    """
    如果XML文件中至少有一个label_name出现次数大于1，则复制该XML文件及其对应的JPG图片到目标目录。
    在尝试复制文件之前，确保目标目录存在。
    """
    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for xml_file in xml_files:
        label_counts = parse_xml_and_count_labels(xml_file)
        if any(count > 1 for count in label_counts.values()):
            # 使用os.path.splitext()安全地替换文件扩展名
            base_file, _ = os.path.splitext(xml_file)
            jpg_file = base_file + '.jpg'
            if os.path.exists(jpg_file):
                shutil.copy(xml_file, dest_dir)
                shutil.copy(jpg_file, dest_dir)

def main(root_dir, dest_dir):
    """
    主函数，执行以上定义的函数。
    """
    xml_files = find_files(root_dir, '.xml')
    copy_files_if_condition_met(xml_files, dest_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="如果XML文件中存在重复labelName则复制该文件及对应的JPG图片到目标目录")
    parser.add_argument('--root_dir', type=str, required=True, help='源目录路径')
    parser.add_argument('--dest_dir', type=str, required=True, help='目标目录路径')
    args = parser.parse_args()
    main(args.root_dir, args.dest_dir)
