import os
import shutil
import argparse

"""
python copy_filtered_files_from_folders.py \
    --folder_list /path/to/folder1 /path/to/folder2 \
    --target_path /path/to/target \
    --file_exts .jpg .xml \
    --keyword some_keyword
"""

class FileOrganizer:
    def __init__(self, source_folders, target_path, file_exts=None, keyword=None):
        self.source_folders = source_folders
        self.target_path = target_path
        self.file_exts = file_exts
        self.keyword = keyword

    def get_files_in_folders(self):
        file_list = []

        for folder_path in self.source_folders:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if (self.file_exts == "None" or any(file.endswith(ext) for ext in self.file_exts)) and \
                       (self.keyword == "None" or self.keyword in file):
                        file_list.append(os.path.join(root, file))

        return file_list

    def ensure_target_path_exists(self):
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)

    def copy_files_to_target(self, files):
        for file in files:
            shutil.copy(file, self.target_path)

    def organize_files(self):
        files = self.get_files_in_folders()
        print(len(files))
        
        self.ensure_target_path_exists()
        self.copy_files_to_target(files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Organize files from multiple source folders to a target folder.")
    
    # 将命令行参数添加到argparse
    parser.add_argument('--folder_list', nargs='+', help="List of source folder paths.")
    parser.add_argument('--target_path', required=True, help="Path of the target folder.")
    parser.add_argument('--file_exts', nargs='+', default=None, help="File extensions to filter for.")
    parser.add_argument('--keyword', default=None, help="Keyword to filter filenames.")
    
    args = parser.parse_args()

    # 使用从命令行获取的参数创建FileOrganizer实例并执行
    organizer = FileOrganizer(args.folder_list, args.target_path, args.file_exts, args.keyword)
    organizer.organize_files()
