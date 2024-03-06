# 技术文档：文件整理脚本

## 概述

本脚本提供了一个自动化工具，用于在指定目录中检查和删除不匹配的文件。它特别适用于需要维护一致文件集的场景，例如，当一个目录下的图片、文本、JSON和XML文件需要按名称成对出现时。

## 版本信息

- Author: mao
- Version: 0.1
- Language: 中文
- Date: 2024-03-06

## 功能描述

该脚本具有以下功能：
1. 递归搜索指定目录下的文件。
2. 筛选出具有特定扩展名的文件。
3. 检查不同文件类型间是否存在名称匹配。
4. 删除没有匹配名称的文件。

## 环境要求

- Python 3.x
- OS: 适用于任何支持Python的操作系统。

## 使用说明

### 安装

无需特别安装步骤，确保Python环境已正确安装。

### 参数配置

脚本接受以下命令行参数：

- `--folder_path`: 检查文件的目录路径。
- `--file_types`: 需要检查的文件扩展名，以逗号分隔（例如：jpg,txt,json,xml）。

### 运行脚本

在命令行中，导航到脚本存放的目录，并运行以下命令：

```shell
python script_name.py --folder_path "path/to/directory" --file_types "jpg,txt,json,xml"
```

请将 `script_name.py` 替换为实际的脚本文件名，`path/to/directory` 替换为目标文件夹的路径。

## 注意事项

- 在删除文件前，请确保已备份重要数据。
- 脚本将递归遍历指定目录，处理大量文件时可能需要较长时间。
- 删除操作不可逆，请谨慎使用。

## 示例

假设您有一个名为 `Documents` 的文件夹，里面包含多种类型的文件，您只希望保留名称相匹配的 `jpg` 和 `txt` 文件。您可以这样运行脚本：

```shell
python script_name.py --folder_path "C:/Users/mao/Documents" --file_types "jpg,txt"
```

执行后，`Documents` 文件夹中所有不匹配的 `jpg` 和 `txt` 文件将被删除。

## 代码结构

```python
import os
import argparse

def get_files_from_directory(directory, extension):
    # ...

def check_and_delete_extras(folder_path, file_types):
    # ...

if __name__ == "__main__":
    # ...
```

- `get_files_from_directory`: 递归获取指定扩展名的文件。
- `check_and_delete_extras`: 检查文件名匹配并删除多余文件。
- 命令行接口: 接受用户输入的参数。

## 作者信息

- 名称: mao
- 联系方式: [mao@example.com](mailto:mao@example.com)

---

请仔细检查这份文档，确保它满足您的需求。如果有任何需要修改或添加的地方，请通知我以便进行相应的更新。