import torch
import pickle
import argparse
import shutil
import os

"""
python filter_images_by_embeddings.py \
    --embeddings_path /home/mao/datasets/支票要素定位/train_images-1274.pkl \
    --destination_path /home/mao/datasets/支票要素定位/filterBySimilarity \
    --similarity_threshold 0.9
"""

def filter_images_by_similarity(embeddings, similarity_threshold=0.85):
    embeddings_items = list(embeddings.items())
    samples = []
    while len(embeddings_items) > 0:
        current_image, current_embedding = embeddings_items.pop(0)
        samples.append(current_image)

        to_remove = [i for i, (_, embedding) in enumerate(embeddings_items)
                     if torch.mm(current_embedding.type(torch.float32), embedding.t().type(torch.float32)).item() > similarity_threshold]
        
        for index in sorted(to_remove, reverse=True):
            embeddings_items.pop(index)

    return samples

def copy_samples_to_destination(samples, destination_dir):
    """Copy filtered samples to the target directory."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for sample_image_path in samples:
        shutil.copy(sample_image_path, destination_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter images by similarity based on precomputed embeddings.")

    parser.add_argument("--embeddings_path", type=str, required=True, help="Path to the saved embeddings file.")
    parser.add_argument("--destination_path", type=str, required=True, help="Path to copy the filtered images to.")
    parser.add_argument("--similarity_threshold", type=float, default=0.85, help="Similarity threshold for filtering images.")

    args = parser.parse_args()

    with open(args.embeddings_path, 'rb') as handle:
        embeddings = pickle.load(handle)

    filtered_samples = filter_images_by_similarity(embeddings, args.similarity_threshold)

    print(f"Filtered {len(filtered_samples)} images")

    copy_samples_to_destination(filtered_samples, args.destination_path)
