# XML到TXT转换器使用文档

## 概述

本文档描述了一个用于将XML标注文件转换为TXT格式的Python脚本。该脚本特别用于处理图像标注数据，将其转换为YOLO格式的标注，便于用于机器学习模型的训练。

## 版本信息

- 作者：mao
- 版本：0.1
- 语言：中文
- 描述：该脚本读取包含在XML文件中的图像标注数据，并将其转换为YOLO格式的TXT文件。

## 功能

1. 读取指定文件夹内的所有XML文件。
2. 解析每个XML文件，提取图像尺寸和标注的边界框。
3. 将边界框坐标转换为YOLO格式。
4. 根据提供的YAML文件中的类映射，将类名转换为类ID。
5. 生成TXT文件，其中包含转换后的YOLO格式标注。
6. 将图像文件、生成的TXT文件和原始XML文件分别移动到指定的子文件夹。

## 环境要求

- Python 3.x
- 需要的Python库：
  - xml.etree.ElementTree
  - os
  - glob
  - argparse
  - shutil
  - yaml

## 安装步骤

1. 确保Python 3.x已安装。
2. 安装PyYAML库，可以使用pip命令：`pip install pyyaml`。

## 使用说明

### 参数配置

脚本接受以下命令行参数：

- `--folder_path`：包含XML文件的文件夹路径。
- `--yaml_path`：包含类映射的YAML文件路径。

### 运行脚本

在命令行中，导航到脚本所在的文件夹，并运行以下命令：

```bash
python xml_to_txt_converter.py --folder_path "path/to/xml_folder" --yaml_path "path/to/yaml_file"
```

请将`"path/to/xml_folder"`和`"path/to/yaml_file"`替换为您的实际路径。

### 输出格式

脚本将在指定的文件夹路径中创建以下子文件夹：

- `images`：存放图像文件（.jpg）。
- `labels`：存放转换后的标注文件（.txt）。
- `xmls`：存放原始的XML文件。

每个TXT文件将包含对应图像的YOLO格式标注，格式如下：

```
<class_id> <x_center> <y_center> <width> <height>
```

其中，`<class_id>`是类别的索引，`<x_center>`和`<y_center>`是边界框中心点的相对坐标，`<width>`和`<height>`是边界框的相对宽度和高度。

## 示例

假设您的XML文件和YAML配置文件位于`/path/to/data`目录，您可以这样运行脚本：

```bash
python xml_to_txt_converter.py --folder_path "/path/to/data" --yaml_path "/path/to/data/classes.yaml"
```

运行后，您将在`/path/to/data`目录下看到新创建的`images`、`labels`和`xmls`文件夹。

## 注意事项

- 确保YAML文件格式正确，且包含一个`names`字段，该字段是一个字典，其键为类名，值为相应的类ID。
- XML文件需要按照Pascal VOC格式编写，其中包含`<size>`和`<object>`标签。

## 更新记录

- 0.1：初始版本，实现基本功能。

## 联系方式

如有疑问或需要支持，请联系作者mao。

---

请根据实际情况调整上述文档内容。如果有任何问题或需要进一步的帮助，请告知。