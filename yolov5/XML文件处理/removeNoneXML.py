import os
import xml.etree.ElementTree as ET
import argparse

"""
代码运行示例:
python removeNoneXML.py \
    --filepath /home/mao/datasets/支票类版面清分/20240304-最新训练数据
"""

def list_files(directory: str, extension: str) -> list:
    """获取指定目录下指定扩展名的所有文件"""
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(extension)]

def parse_xml(xml_file: str) -> ET.Element:
    """解析XML文件并返回root元素"""
    tree = ET.parse(xml_file)
    return tree.getroot()

def remove_if_no_object_tag(xml_file: str):
    """如果xml文件中没有object标签，则删除xml和对应的图片"""
    root = parse_xml(xml_file)
    objects = root.findall("object")
    
    if not objects:
        os.remove(xml_file)
        jpg_file = xml_file[:-3] + "jpg"
        if os.path.exists(jpg_file):
            os.remove(jpg_file)

def main(filepath: str):
    """主函数：遍历指定路径下的xml文件，检查并删除无object标签的xml和图片"""
    for xml_file in list_files(filepath, ".xml"):
        remove_if_no_object_tag(xml_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="处理指定文件夹下的xml和图片文件")
    parser.add_argument("--filepath", help="文件夹路径，例如：/home/mao/datasets/...")
    args = parser.parse_args()

    main(args.filepath)
