#%%

import os
import pickle

def update_embeddings(embeddings_path):
    # 加载现有的embeddings
    with open(embeddings_path, 'rb') as handle:
        embeddings = pickle.load(handle)

    # 待删除的图片路径集合
    to_delete = []

    # 检测每个路径的图片是否存在
    for image_path in embeddings.keys():
        if not os.path.exists(image_path):
            to_delete.append(image_path)

    # 删除不存在的图片的embeddings
    for del_path in to_delete:
        del embeddings[del_path]

    # 保存更新后的embeddings
    with open(embeddings_path, 'wb') as handle:
        pickle.dump(embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Updated embeddings and removed {len(to_delete)} entries.")

# 调用函数，更新embeddings
# 请替换下面的路径为你的实际embeddings文件路径
embeddings_path = '/home/mao/datasets/支票要素定位/有效样本-裁剪子图/转账支票.pkl'
update_embeddings(embeddings_path)

# %%
