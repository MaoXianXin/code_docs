import os
import shutil
from xml.etree import ElementTree as ET
import argparse

"""
代码运行示例:
python organize_files_by_class.py \
    --source_dir /home/mao/datasets/支票类版面清分/20240304-最新训练数据/
    --target_dir /home/mao/datasets/支票类版面清分/分类结果
"""

def parse_xml_class_names(xml_path):
    """解析XML并返回类名集合."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    class_names = set()
    for obj in root.findall('object'):
        name = obj.find('name').text
        class_names.add(name)
    
    return class_names

def ensure_directory_exists(directory_path):
    """确保目录存在，如果不存在则创建."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def determine_dest_folder(class_names, target_dir, combined_name="组合类别"):
    """根据类名确定目标文件夹."""
    if len(class_names) == 1:
        return os.path.join(target_dir, list(class_names)[0])
    else:
        return os.path.join(target_dir, combined_name)

def copy_files_based_on_classes(source_dir, target_dir, xml_ext=".xml", img_ext=".jpg", combined_name="组合类别"):
    """基于类名复制文件."""
    for file_name in os.listdir(source_dir):
        if file_name.endswith(xml_ext):
            xml_path = os.path.join(source_dir, file_name)
            
            class_names = parse_xml_class_names(xml_path)
            dest_folder = determine_dest_folder(class_names, target_dir, combined_name)
                
            ensure_directory_exists(dest_folder)
            shutil.copy2(xml_path, os.path.join(dest_folder, file_name))

            image_filename = os.path.splitext(file_name)[0] + img_ext
            image_src = os.path.join(source_dir, image_filename)
            if os.path.exists(image_src):
                shutil.copy2(image_src, os.path.join(dest_folder, image_filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy files based on classes from source directory to target directory.")
    parser.add_argument("--source_dir", help="Path to the source directory.")
    parser.add_argument("--target_dir", help="Path to the target directory.")

    args = parser.parse_args()

    copy_files_based_on_classes(args.source_dir, args.target_dir)
