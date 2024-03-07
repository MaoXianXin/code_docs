from pathlib import Path
import xml.etree.ElementTree as ET
import argparse

"""
python removeNoneXML.py \
    --filepath "/path/to/your/directory"
"""

def get_xml_files(directory: Path) -> list:
    """获取指定目录下的所有XML文件"""
    return directory.glob('*.xml')

def remove_file_if_no_object(xml_file: Path):
    """如果XML文件中没有object标签，则删除XML和对应的图片"""
    root = ET.parse(xml_file).getroot()
    objects = root.findall("object")
    
    if not objects:
        try:
            xml_file.unlink()
            jpg_file = xml_file.with_suffix('.jpg')
            if jpg_file.exists():
                jpg_file.unlink()
        except OSError as e:
            print(f"Error: {e}")

def process_directory(filepath: str):
    """处理指定目录下的XML和JPEG文件"""
    path = Path(filepath)
    for xml_file in get_xml_files(path):
        remove_file_if_no_object(xml_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="处理指定文件夹下的xml和图片文件")
    parser.add_argument("--filepath", required=True, help="文件夹路径，例如：/home/mao/datasets/...")
    args = parser.parse_args()

    process_directory(args.filepath)
