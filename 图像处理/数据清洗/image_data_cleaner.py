import os
import shutil
import csv
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor
import threading

"""
图像数据清洗流程:
先判断文件后缀是否为常见格式，如果不是则删除，如果是则往下一步走
读取文件开头，判断是不是常见图片格式开头，如果不是则删除，如果是则往下一步走
判断是否存在exif参数，如果存在则转正图像
把图像转换成RGB格式
读取整个图像文件，判断是否损坏
获取整个图像文件，判断是否大小是否过大
"""

# 定义基础参数
source_dir = '/home/mao/datasets/测试源数据清洗代码/2018'
destination_dir = '/home/mao/datasets/测试源数据清洗代码/2018_processed'
metadata_file = 'metadata.csv'
log_file = 'cleaning_log.txt'
max_file_size = 5242880 # 定义过大文件的大小阈值

def log_message(message, is_exception=False, file_path=None):
    """
    Logs a message to the log file. If the message is an exception, it formats the message
    accordingly.

    Args:
    message (str): The message to be logged.
    is_exception (bool): A flag to indicate if the message is an exception.
    file_path (str, optional): The file path associated with the exception, if any.
    """
    formatted_message = message
    if is_exception and file_path:
        formatted_message = f"Exception for {file_path}: {message}"
    
    with open(log_file, 'a') as log:
        log.write(formatted_message + '\n')


# 检查目标文件夹是否存在，如果不存在则创建
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# 创建或清空元数据文件
with open(metadata_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['New Path', 'Original Path', 'File Size'])


def is_image_corrupted(filepath):
    try:
        with Image.open(filepath) as img:
            img.load()  # load() is a PIL function that checks if the file is broken
            return False
    except Exception as e:
        return True


def process_and_save_as_jpeg(file_path):
    """
    Processes a single image file. It checks for supported image formats (JPG, JPEG, PNG, BMP),
    handles Exif data, converts the image to JPEG, and saves it. Deletes the original file if it's 
    not in a supported format or if the name/format changes after conversion.

    Args:
    file_path (str): The path of the image file to be processed.
    """
    # Image format signatures for JPG, PNG, and BMP
    jpg_signature = b'\xFF\xD8\xFF'
    png_signature = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    bmp_signature = b'\x42\x4D'
    tif_signature_le = b'II\x2A\x00'  # Little endian TIFF
    tif_signature_be = b'MM\x00\x2A'  # Big endian TIFF

    filename = os.path.basename(file_path)
    base_dir = os.path.dirname(file_path)
    name, ext = os.path.splitext(filename)


    with open(file_path, 'rb') as f:
        header = f.read(8)  # Read enough bytes to cover all formats

    # Check for supported formats
    if header.startswith(jpg_signature) or header.startswith(png_signature) or header.startswith(bmp_signature) or header.startswith(tif_signature_le) or header.startswith(tif_signature_be):
        with Image.open(file_path) as img:
            # Handle Exif data
            if hasattr(img, '_getexif'):
                exif = img._getexif()
                if exif:
                    img = ImageOps.exif_transpose(img)

            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Save as JPEG
            new_file_path = os.path.join(base_dir, name + '.jpg')
            img.save(new_file_path, 'JPEG')

            if file_path != new_file_path:
                os.remove(file_path)

        print(f'Successfully processed and saved {filename} as JPEG.')
        return new_file_path
    else:
        # Delete the file if it's not a supported image format
        os.remove(file_path)
        log_message(f'The file {filename} was not a supported image format and has been deleted.')
        return None


# 创建线程锁
log_lock = threading.Lock()
metadata_lock = threading.Lock()

def process_file(file_tuple):
    root, file, file_count = file_tuple
    original_path = os.path.join(root, file)
    new_filename = "{:09d}".format(file_count) + "_" + file  # 修改这里
    new_path = os.path.join(destination_dir, new_filename)

    # 尝试处理每个文件
    try:
        # 检查文件后缀是否为图片格式
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')):
            # 拷贝文件到指定目录并加前缀
            shutil.copy(original_path, new_path)

            # 转换非jpg和非RGB图片
            new_path = process_and_save_as_jpeg(new_path)

            if not new_path:
                return
            
            # 检查图片是否损坏
            if is_image_corrupted(new_path):
                os.remove(new_path)
                raise Exception(f"File {new_filename} is corrupted and has been removed.")

            # 获取并记录文件大小
            file_size = os.path.getsize(new_path)

            # 检查文件是否过大
            if file_size > max_file_size:
                os.remove(new_path)
                raise Exception(f"File {new_filename} is too large and has been removed.")

            # 记录到元数据文件
            with metadata_lock:
                with open(metadata_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([new_path, original_path, file_size])

            with log_lock:
                log_message("Processed and copied: " + original_path)
        else:
            # 如果不是图片格式则删除
            os.remove(original_path)
            with log_lock:
                log_message("Deleted non-image file: " + original_path)
    
    except Exception as e:
        with log_lock:
            if os.path.exists(original_path):
                os.remove(original_path)
            if os.path.exists(new_path):
                os.remove(new_path)
            log_message(str(e), is_exception=True, file_path=original_path)


# 创建一个线程池
file_count = 1
with ThreadPoolExecutor(max_workers=15) as executor:
    file_tuples = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_tuples.append((root, file, file_count))
            file_count += 1

    # 将文件处理任务分配给线程池
    executor.map(process_file, file_tuples)
        

# 完成日志记录
log_message("Data cleaning process completed.")