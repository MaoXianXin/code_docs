import os
import torch
from PIL import Image
import open_clip
import pickle
import argparse

"""
python generate_embeddings.py \
    --image_path /home/mao/datasets/支票要素定位/20240320-1274-最新训练样本/images \
    --embeddings_path /home/mao/datasets/支票要素定位/train_images-1274.pkl \
    --model_name ViT-H-14-quickgelu \
    --pretrained_version dfn5b \
    --ext .jpg
"""

class EmbeddingGenerator:
    def __init__(self, model_name, pretrained_version, ext=".jpg"):
        self.ext = ext
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained_version)
        self.model = self.model.cuda()  # Transfer the model to GPU

    def _get_all_images(self, path):
        """Recursively fetches all images with the given extension from the specified path."""
        return [os.path.join(root, fname) 
                for root, dirs, files in os.walk(path) 
                for fname in files if fname.endswith(self.ext)]

    def generate_embeddings(self, image_paths):
        """Generate normalized embeddings for each image."""
        embeddings = {}
        for image_path in image_paths:
            image = self.preprocess(Image.open(image_path)).unsqueeze(0).cuda()  # Transfer to GPU
            with torch.no_grad(), torch.cuda.amp.autocast():
                image_features = self.model.encode_image(image)
                image_features /= image_features.norm(dim=-1, keepdim=True)
            embeddings[image_path] = image_features.cpu()
        return embeddings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and save embeddings for images.")
    parser.add_argument("--image_path", type=str, required=True, help="Directory of images to process.")
    parser.add_argument("--embeddings_path", type=str, required=True, help="File path to save the embeddings.")
    parser.add_argument("--model_name", type=str, default="xlm-roberta-base-ViT-B-32", help="Model name to use.")
    parser.add_argument("--pretrained_version", type=str, default="laion5b_s13b_b90k", help="Pretrained version to use.")
    parser.add_argument("--ext", type=str, default=".jpg", help="Image file extension to look for.")

    args = parser.parse_args()

    generator = EmbeddingGenerator(model_name=args.model_name, pretrained_version=args.pretrained_version, ext=args.ext)
    all_images = generator._get_all_images(args.image_path)
    embeddings = generator.generate_embeddings(all_images)

    with open(args.embeddings_path, 'wb') as handle:
        pickle.dump(embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Embeddings generated and saved to {args.embeddings_path}")
