import os
import re
from PIL import Image
import argparse

"""
python convert_yolo_to_voc.py \
    --folder /home/mao/github_repo/ultralytics/runs/detect/predict1000/low_confidence_imgs \
    --classes /home/mao/datasets/多个版面标题定位训练集/predefine_classes.txt
"""

def load_classes(file_path):
    with open(file_path, 'r') as f:
        return [x.strip() for x in f.readlines()]

def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def find_matching_image(base_file_name, search_dir):
    # 分割文件名和扩展名
    file_root, file_ext = os.path.splitext(base_file_name)
    
    # 确保原始文件扩展名是.txt
    if file_ext.lower() != '.txt':
        raise ValueError("Base file name does not have a .txt extension")

    for extension in ['.jpeg', '.jpg', '.png']:
        # 构建新的文件名
        img_name = f"{file_root}{extension}"
        if os.path.exists(os.path.join(search_dir, img_name)):
            return img_name
    return None

def convert_yolo_to_voc(line, classes, img_width, img_height):
    data = re.split("\s", line.rstrip())
    if len(data) == 5 and all(map(is_number, data)):
        class_id = int(data[0])
        class_name = classes[class_id]
        x_center, y_center, width, height = map(float, data[1:])
        box_width = width * img_width
        box_height = height * img_height
        x_min = str(int(x_center * img_width - box_width / 2))
        y_min = str(int(y_center * img_height - box_height / 2))
        x_max = str(int(x_center * img_width + box_width / 2))
        y_max = str(int(y_center * img_height + box_height / 2))
        return class_name, x_min, y_min, x_max, y_max
    return None

def process_yolo_file(yolo_file, classes):
    img_name = find_matching_image(yolo_file, os.getcwd())
    if not img_name:
        return

    orig_img = Image.open(img_name)
    img_width = orig_img.width
    img_height = orig_img.height

    # 分割文件名和扩展名
    file_root, file_ext = os.path.splitext(yolo_file)

    # 确保原始文件扩展名是.txt
    if file_ext.lower() != '.txt':
        raise ValueError("Yolo file name does not have a .txt extension")

    xml_file = f"{file_root}.xml"  # 使用.xml作为新的扩展名

    with open(xml_file, 'w') as f:  # 使用安全更改后的文件名
        f.write('<annotation>\n')
        f.write('\t<folder>XML</folder>\n')
        f.write('\t<filename>' + img_name + '</filename>\n')
        f.write('\t<path>' + os.getcwd() + os.sep + img_name + '</path>\n')
        f.write('\t<source>\n')
        f.write('\t\t<database>Unknown</database>\n')
        f.write('\t</source>\n')
        f.write('\t<size>\n')
        f.write('\t\t<width>' + str(img_width) + '</width>\n')
        f.write('\t\t<height>' + str(img_height) + '</height>\n')
        f.write('\t\t<depth>3</depth>\n')  # assuming a 3 channel color image (RGB)
        f.write('\t</size>\n')
        f.write('\t<segmented>0</segmented>\n')

        for line in open(yolo_file, 'r').readlines():
            result = convert_yolo_to_voc(line, classes, img_width, img_height)
            if result:
                class_name, x_min, y_min, x_max, y_max = result
                # write each object to the file
                f.write('\t<object>\n')
                f.write('\t\t<name>' + class_name + '</name>\n')
                f.write('\t\t<pose>Unspecified</pose>\n')
                f.write('\t\t<truncated>0</truncated>\n')
                f.write('\t\t<difficult>0</difficult>\n')
                f.write('\t\t<bndbox>\n')
                f.write('\t\t\t<xmin>' + x_min + '</xmin>\n')
                f.write('\t\t\t<ymin>' + y_min + '</ymin>\n')
                f.write('\t\t\t<xmax>' + x_max + '</xmax>\n')
                f.write('\t\t\t<ymax>' + y_max + '</ymax>\n')
                f.write('\t\t</bndbox>\n')
                f.write('\t</object>\n')

        f.write('</annotation>\n')

def main(args):
    classes = load_classes(args.yolo_class_list_file)
    os.chdir(args.folder_holding_yolo_files)

    for yolo_file in os.listdir(args.folder_holding_yolo_files):
        if yolo_file.endswith("txt"):
            process_yolo_file(yolo_file, classes)
            
    print("Conversion complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert YOLO annotations to VOC format.")
    parser.add_argument("--folder", dest="folder_holding_yolo_files", required=True, help="Path to the directory holding the YOLO txt files.")
    parser.add_argument("--classes", dest="yolo_class_list_file", required=True, help="Path to the file that has the YOLO classes (typically classes.txt).")

    args = parser.parse_args()
    main(args)