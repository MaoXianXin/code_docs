import xml.etree.ElementTree as ET
import os
import glob
import argparse
import shutil
import yaml

"""
代码运行示例:
python convert_voc_to_yolo.py \
    --folder_path /home/mao/datasets/小码定位/最新训练样本/train \
    --yaml_path /home/mao/github_repo/ultralytics/ultralytics/cfg/datasets/autoTrain_1.yaml
"""

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='XML to TXT converter.')
# Add argument
parser.add_argument('--folder_path', type=str, help='The path of the folder containing XML files.')
parser.add_argument('--yaml_path', type=str, help='The path of the yaml file containing class mapping.')
# Parse arguments
args = parser.parse_args()

def convert_coordinates(size, box):
    # Extract image dimensions
    width, height = size
    # Extract box coordinates
    xmin, ymin, xmax, ymax = box
    # Convert to YOLO format
    x_center = (xmin + xmax) / (2 * width)
    y_center = (ymin + ymax) / (2 * height)
    w = (xmax - xmin) / width
    h = (ymax - ymin) / height
    return (x_center, y_center, w, h)

def xml_to_txt(xml_path, class_mapping):
    # Parse XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # Extract image size
    size = (int(root.find("size/width").text), int(root.find("size/height").text))
    # Initialize results
    results = []
    # Iterate over each object in the XML
    for obj in root.findall("object"):
        # Get class name and convert to class id
        class_name = obj.find("name").text
        class_id = class_mapping.get(class_name)
        # Convert box coordinates
        box = (
            float(obj.find("bndbox/xmin").text),
            float(obj.find("bndbox/ymin").text),
            float(obj.find("bndbox/xmax").text),
            float(obj.find("bndbox/ymax").text),
        )
        x_center, y_center, w, h = convert_coordinates(size, box)
        results.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")
    
    # Save to txt
    txt_path = os.path.splitext(xml_path)[0] + ".txt"
    with open(txt_path, "w") as txt_file:
        txt_file.write("\n".join(results))

def batch_process(folder_path, yaml_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return
    # Load class mapping from yaml file
    with open(yaml_path, 'r') as stream:
        data = yaml.safe_load(stream)
    class_mapping = {name: idx for idx, name in data['names'].items()}
    # Get all XML files in the folder
    xml_files = glob.glob(os.path.join(folder_path, "*.xml"))
    for xml_file in xml_files:
        xml_to_txt(xml_file, class_mapping)

    # After processing all xml_files, create images, labels, xmls folders
    os.makedirs(os.path.join(folder_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(folder_path, 'labels'), exist_ok=True)
    os.makedirs(os.path.join(folder_path, 'xmls'), exist_ok=True)

    # Move files into corresponding folders
    for file in glob.glob(os.path.join(folder_path, "*")):
        if file.endswith(".jpg"):
            shutil.move(file, os.path.join(folder_path, "images"))
        elif file.endswith(".txt"):
            shutil.move(file, os.path.join(folder_path, "labels"))
        elif file.endswith(".xml"):
            shutil.move(file, os.path.join(folder_path, "xmls"))

# Use the function
folder_path = args.folder_path  # Replace with your folder path
yaml_path = args.yaml_path  # Replace with your yaml file path
batch_process(folder_path, yaml_path)