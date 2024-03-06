import os
import argparse

"""
代码运行示例:
python remove_unpaired_files.py \
    --folder_path /home/mao/datasets/20个版面区域定位训练-实验版/测试样本/07-丝丽雅/预测错误样本-origin/ \
    --file_types "jpg,txt,json,xml"
"""

def get_files_from_directory(directory, extension):
    """
    递归地获取目录下所有指定扩展名的文件
    """
    files_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                files_list.append(os.path.join(root, file))

    return files_list

def check_and_delete_extras(folder_path, file_types):
    all_files_dict = {
        '.jpg': [],
        '.txt': [],
        '.json': [],
        '.xml': []
    }

    all_names_dict = {
        '.jpg': [],
        '.txt': [],
        '.json': [],
        '.xml': []
    }

    # 根据用户选择的文件类型，获取文件和对应的名称列表
    for ext in file_types:
        all_files_dict[ext] = get_files_from_directory(folder_path, ext)
        all_names_dict[ext] = [os.path.splitext(os.path.basename(f))[0] for f in all_files_dict[ext]]

    # 检查是否所有指定文件类型的文件名都存在于每种文件类型的文件名列表中
    for ext in file_types:
        for i, name in enumerate(all_names_dict[ext]):
            if any(name not in all_names_dict[other_ext] for other_ext in file_types if other_ext != ext):
                os.remove(all_files_dict[ext][i])
                print(f"Deleted {all_files_dict[ext][i]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check and delete extra files in a directory based on file types.")
    parser.add_argument("--folder_path", help="Path to the directory containing files to check.")
    parser.add_argument("--file_types", type=str, help="File types to check separated by commas (e.g. jpg,txt,json,xml).")
    
    args = parser.parse_args()
    
    folder_path = args.folder_path
    file_types = ['.' + ext.strip() for ext in args.file_types.split(',')]
    
    check_and_delete_extras(folder_path, file_types)
