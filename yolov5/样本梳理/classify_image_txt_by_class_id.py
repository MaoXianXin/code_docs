#%%

import os
import shutil

def create_class_id_to_name_dict(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return {i: line.strip() for i, line in enumerate(lines)}

def copy_files_with_condition(txt_src_path, img_src_path, target_path, txt_file_path):
    # 从文本文件创建class_id_to_name字典
    class_id_to_name = create_class_id_to_name_dict(txt_file_path)

    # 确保目标路径存在
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    # 创建"组合类别"文件夹的路径
    combined_category_path = os.path.join(target_path, "组合类别")
    if not os.path.exists(combined_category_path):
        os.makedirs(combined_category_path)

    for root, dirs, files in os.walk(txt_src_path):
        for file in files:
            if file.endswith('.txt'):
                txt_file_path = os.path.join(root, file)
                with open(txt_file_path, 'r') as txt_file:
                    lines = txt_file.readlines()
                    label_ids = [int(line.split()[0]) for line in lines]
                    unique_label_ids = set(label_ids)

                    # 更安全地处理图片文件名
                    img_file_name = os.path.splitext(file)[0] + '.jpg'
                    img_file_path = os.path.join(img_src_path, img_file_name)

                    # 如果txt文本存在多行，并且存在多个不相同的labelID
                    if len(lines) > 1 and len(unique_label_ids) > 1:
                        shutil.copy2(txt_file_path, combined_category_path)
                        if os.path.exists(img_file_path):
                            shutil.copy2(img_file_path, combined_category_path)

                    # 如果txt文本中所有行的labelID都是相同的
                    elif len(unique_label_ids) == 1:
                        class_name = class_id_to_name[unique_label_ids.pop()]
                        class_target_path = os.path.join(target_path, class_name)
                        if not os.path.exists(class_target_path):
                            os.makedirs(class_target_path)
                        shutil.copy2(txt_file_path, class_target_path)
                        if os.path.exists(img_file_path):
                            shutil.copy2(img_file_path, class_target_path)

# 示例文本文件路径，实际使用时需要替换为实际路径
txt_file_path = '/home/mao/datasets/支票类版面清分/split_1_分类结果/predefine_classes.txt'
txt_source_path = '/home/mao/workspace/yolov5/runs/detect/exp/labels'
img_source_path = '/home/mao/datasets/tilseal_split/split_2'
target_path = '/home/mao/datasets/支票类版面清分/split_2_分类结果'

# 调用函数，使用从文本文件中读取的class_id_to_name
copy_files_with_condition(txt_source_path, img_source_path, target_path, txt_file_path)


# %%
