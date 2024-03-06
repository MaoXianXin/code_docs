import os
import argparse


class FileHandler:
    def __init__(self):
        pass
    
    @staticmethod
    def get_files_in_folders(folder_list, file_exts=None, keyword=None):
        file_list = []
        for folder_path in folder_list:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if (file_exts is None or any(file.endswith(ext) for ext in file_exts)) and (keyword is None or keyword in file):
                        file_list.append(os.path.join(root, file))
        return file_list

    @staticmethod
    def get_common_files(files_A, files_B):
        """
        从给定的两个文件列表中找出共有的文件名（不考虑路径和后缀）。
    
        参数:
            files_A (list): 第一个文件全路径列表。
            files_B (list): 第二个文件全路径列表。
    
        返回:
            list: 共有文件的全路径列表。
        """
        file_name_A = set(os.path.splitext(os.path.basename(file))[0] for file in files_A)
        file_name_B = set(os.path.splitext(os.path.basename(file))[0] for file in files_B)
        
        common_files_A = [file for file in files_A if os.path.splitext(os.path.basename(file))[0] in file_name_B]
        common_files_B = [file for file in files_B if os.path.splitext(os.path.basename(file))[0] in file_name_A]
    
        return common_files_A, common_files_B

    @staticmethod
    def remove_files(file_list):
        for file in file_list:
            os.remove(file)
        print("All specified files have been removed.")

def main(args):
    handler = FileHandler()
    files_A = handler.get_files_in_folders(args.folder_list_A)
    files_B = handler.get_files_in_folders(args.folder_list_B)

    common_files_A, common_files_B = handler.get_common_files(files_A, files_B)
    print(len(common_files_A))

    handler.remove_files(common_files_A)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process folders to find and delete common files.")
    
    # 使用 nargs="+" 来接受多个文件夹作为参数列表
    parser.add_argument("--folder_list_A", type=str, nargs="+", required=True, help="List of source directories for folder A")
    parser.add_argument("--folder_list_B", type=str, nargs="+", required=True, help="List of source directories for folder B")
    
    args = parser.parse_args()
    main(args)