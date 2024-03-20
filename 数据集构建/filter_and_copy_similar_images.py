# filter_and_copy_similar_images.py

import torch
import pickle
import argparse
import shutil
import os
from PIL import Image
import open_clip

# 给定一批错误样本，从预先计算好的embeddings中过滤出相似度在[0.96,0.98)的样本子集
"""
python filter_and_copy_similar_images.py \
    --embeddings_path /home/mao/datasets/支票要素定位/train_images-1274.pkl \
    --error_samples_path /home/mao/datasets/支票要素定位/error_samples \
    --destination_path /home/mao/datasets/支票要素定位/filterBySimilarity \
    --upper_similarity_threshold 0.98 \
    --lower_similarity_threshold 0.96 \
    --model_name ViT-H-14-quickgelu \
    --pretrained_version dfn5b
"""

def load_embeddings(embeddings_path):
    with open(embeddings_path, 'rb') as handle:
        return pickle.load(handle)

def generate_error_sample_embeddings(error_samples_path, model, preprocess):
    embeddings = {}
    for image_name in os.listdir(error_samples_path):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(error_samples_path, image_name)
            image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).cuda()  # Assuming you have GPU support
            with torch.no_grad(), torch.cuda.amp.autocast():
                image_features = model.encode_image(image)
                image_features /= image_features.norm(dim=-1, keepdim=True)
            embeddings[image_path] = image_features.cpu()
    return embeddings

def find_similar_samples(embeddings, error_sample_embeddings, lower_similarity_threshold, upper_similarity_threshold):
    similar_samples = set()
    for error_path, error_embedding in error_sample_embeddings.items():
        for img_path, img_embedding in embeddings.items():
            similarity = torch.mm(error_embedding.type(torch.float32), img_embedding.t().type(torch.float32)).item()
            if upper_similarity_threshold > similarity and similarity >= lower_similarity_threshold:
                similar_samples.add(img_path)
    return list(similar_samples)

def copy_samples_to_destination(samples, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for sample_image_path in samples:
        shutil.copy(sample_image_path, destination_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter and copy similar images based on embeddings.")
    parser.add_argument("--embeddings_path", type=str, required=True, help="Path to the saved embeddings file.")
    parser.add_argument("--error_samples_path", type=str, required=True, help="Directory of error sample images.")
    parser.add_argument("--destination_path", type=str, required=True, help="Path to copy the similar images to.")
    parser.add_argument("--upper_similarity_threshold", type=float, default=0.98, help="Upper similarity threshold for filtering images.")
    parser.add_argument("--lower_similarity_threshold", type=float, default=0.96, help="Lower similarity threshold for filtering images.")
    parser.add_argument("--model_name", type=str, default="ViT-B-32", help="Model name for error samples.")
    parser.add_argument("--pretrained_version", type=str, default="laion2b_s34b_b79k", help="Pretrained version for error samples.")

    args = parser.parse_args()

    # Load precomputed embeddings
    embeddings = load_embeddings(args.embeddings_path)

    # Generate model and preprocess for error sample generation
    model, _, preprocess = open_clip.create_model_and_transforms(
        model_name=args.model_name, 
        pretrained=args.pretrained_version
    )
    model = model.cuda()  # Transfer the model to GPU

    # Generate embeddings for the error samples
    error_sample_embeddings = generate_error_sample_embeddings(
        args.error_samples_path, 
        model, 
        preprocess
    )

    # Find similar images
    similar_samples = find_similar_samples(
        embeddings, 
        error_sample_embeddings, 
        args.lower_similarity_threshold,
        args.upper_similarity_threshold
    )

    print(f"Found {len(similar_samples)} similar images, copying to {args.destination_path}")

    # Copy the similar images to the destination directory
    copy_samples_to_destination(similar_samples, args.destination_path)
