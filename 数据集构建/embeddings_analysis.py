# %%

# 可视化分析T-SNE降维

import pickle
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 步骤1: 加载嵌入数据
embeddings_path = '/home/mao/datasets/支票要素定位/有效样本-裁剪子图/filterBySimilarity.pkl'  # 请将此路径替换为你的实际嵌入文件路径
with open(embeddings_path, 'rb') as handle:
    embeddings_dict = pickle.load(handle)

# 步骤2: 数据预处理
# 将嵌入从字典转换为numpy数组，只取嵌入值，并确保每个嵌入都是一维的
embeddings_list = []
for path in embeddings_dict:
    embedding_tensor = embeddings_dict[path]
    embedding_numpy = embedding_tensor.squeeze().numpy()  # 使用squeeze()来降维
    embeddings_list.append(embedding_numpy)

embeddings = np.array(embeddings_list)  # 将列表转换为2维numpy数组


# 步骤3: 执行T-SNE降维
tsne = TSNE(n_components=2, perplexity=30.0, learning_rate=200.0, n_iter=1000, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings)

# 步骤4: 绘制散点图
plt.figure(figsize=(10, 10))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], marker='.')
plt.title('T-SNE Embeddings')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.show()

# 步骤5: 保存散点图
plt.savefig('tsne_embeddings.png')


# %%

# 计算embedding的方差、球面性等统计量. 确保数据的一致性和质量

import numpy as np
import pickle

# 加载嵌入数据
with open('/home/mao/datasets/支票要素定位/有效样本-裁剪子图/filterBySimilarity.pkl', 'rb') as f:
    embeddings_dict = pickle.load(f)

# 将嵌入字典转换为NumPy数组
embeddings = np.stack(list(embeddings_dict.values()))

# 确保嵌入是二维的
embeddings = embeddings.reshape(embeddings.shape[0], embeddings.shape[-1])

# 计算方差
variances = np.var(embeddings, axis=0)
total_variance = np.var(embeddings)

print(f"方差 per dimension: {variances}")
print(f"总方差: {total_variance}")

# 计算范数
norms = np.linalg.norm(embeddings, axis=1)

# 检查是否有范数为零的情况，并避免除以零
norms[norms == 0] = np.inf

# 规范化嵌入到单位范数
normalized_embeddings = embeddings / norms[:, np.newaxis]

# 再次计算范数，检查是否所有范数都接近1
normalized_norms = np.linalg.norm(normalized_embeddings, axis=1)
mean_norm = np.mean(normalized_norms)
std_norm = np.std(normalized_norms)

print(f"平均范数: {mean_norm}")
print(f"范数标准差: {std_norm}")

# %%

# 聚类分析: t-SNE with K-Means Clustering

import pickle
import numpy as np
from sklearn.preprocessing import Normalizer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# 加载embeddings
with open('/home/mao/datasets/支票要素定位/有效样本-裁剪子图/filterBySimilarity.pkl', 'rb') as f:
    embeddings = pickle.load(f)

# embeddings形状转换
embeddings = np.vstack([emb.squeeze() for emb in embeddings.values()])

# 归一化embeddings
normalizer = Normalizer()
embeddings_normalized = normalizer.fit_transform(embeddings)

# t-SNE降维
tsne = TSNE(n_components=2, random_state=42)
embeddings_reduced = tsne.fit_transform(embeddings_normalized)

# K-Means聚类
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(embeddings_reduced)

# 轮廓系数评估
silhouette_avg = silhouette_score(embeddings_reduced, clusters)
print(f'Silhouette Coefficient: {silhouette_avg:.4f}')

# 可视化t-SNE降维和聚类结果
plt.scatter(embeddings_reduced[:, 0], embeddings_reduced[:, 1], c=clusters, cmap='viridis', marker='.')
plt.colorbar()
plt.title('t-SNE with K-Means Clustering')
plt.xlabel('t-SNE feature 1')
plt.ylabel('t-SNE feature 2')
plt.show()

# %%

# 通过聚类进行典型样本抽样

import os
import shutil
from scipy.spatial import distance
import pickle
import numpy as np
from sklearn.preprocessing import Normalizer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 加载embeddings
with open('/home/mao/datasets/支票要素定位/有效样本-裁剪子图/filterBySimilarity.pkl', 'rb') as f:
    embeddings = pickle.load(f)

# 获取embeddings的路径
embeddings_paths = list(embeddings.keys())

# embeddings形状转换
embeddings = np.vstack([emb.squeeze() for emb in embeddings.values()])

# 归一化embeddings
normalizer = Normalizer()
embeddings_normalized = normalizer.fit_transform(embeddings)

# t-SNE降维
tsne = TSNE(n_components=2, random_state=42)
embeddings_reduced = tsne.fit_transform(embeddings_normalized)

# K-Means聚类
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(embeddings_reduced)

# 找到每个聚类中心
cluster_centers = kmeans.cluster_centers_

# 创建一个目录来存储选中的样本
selected_samples_dir = '/home/mao/datasets/支票要素定位/有效样本-裁剪子图/selected_samples'
os.makedirs(selected_samples_dir, exist_ok=True)


# 对每个聚类，找到最接近中心的样本
for i, center in enumerate(cluster_centers):
    # 计算该聚类中所有点到中心的距离
    distances = distance.cdist([center], embeddings_reduced[clusters == i], 'euclidean')
    # 找到最小距离的索引
    closest_index = np.argmin(distances)
    # 找到实际索引
    actual_index = np.where(clusters == i)[0][closest_index]
    # 获取对应的文件路径
    selected_image_path = embeddings_paths[actual_index]
    # 拷贝文件到指定目录
    shutil.copy(selected_image_path, os.path.join(selected_samples_dir, os.path.basename(selected_image_path)))

print(f"Selected samples are copied to {selected_samples_dir}")

# %%
