import os
import cv2
import albumentations as A
import argparse
from concurrent.futures import ThreadPoolExecutor

"""
代码运行示例:
python image_transformer.py \
    --source_dir /home/mao/datasets/固定版面清分子图Mask/固定版面清分-调整标注后-表格框/数据裁切-Mask/origin-jpg \
    --target_dir /home/mao/datasets/固定版面清分子图Mask/固定版面清分-调整标注后-表格框/数据裁切-Mask/origin-jpg_processed \
    --max_size 512 \
    --threads 4
"""

def get_image_transformations(max_size=640):
    """Return a composed transformation."""
    return A.Compose([
        A.LongestMaxSize(max_size=max_size),
    ])

def apply_transformation_to_image(image_path, transformation):
    """Load an image, apply the given transformation, and return the transformed image."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    transformed = transformation(image=image)
    return transformed["image"]

def save_transformed_image(image, output_path):
    """Save the given image to the specified output path."""
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

def process_single_image(source_path, target_path, transformation):
    """Process a single jpg image."""
    transformed_image = apply_transformation_to_image(source_path, transformation)
    save_transformed_image(transformed_image, target_path)

def process_images_in_directory(source_directory, target_directory, transformation, max_workers=8):
    """Process all jpg images in the source directory and save them in the target directory using multithreading."""
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    image_paths = []
    for root, _, files in os.walk(source_directory):
        for file in files:
            if file.endswith('.jpg'):
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_directory, file)
                image_paths.append((source_path, target_path))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda p: process_single_image(p[0], p[1], transformation), image_paths)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Transform images in a directory.")
    parser.add_argument("--source_dir", type=str, required=True, help="Path to the source directory containing images to be transformed.")
    parser.add_argument("--target_dir", type=str, required=True, help="Path to the target directory to save the transformed images.")
    parser.add_argument("--max_size", type=int, default=640, help="Max size for the LongestMaxSize transformation. Default is 640.")
    parser.add_argument("--threads", type=int, default=14, help="Number of threads to use. Default is 8.")
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    transform = get_image_transformations(max_size=args.max_size)
    process_images_in_directory(args.source_dir, args.target_dir, transform, max_workers=args.threads)
