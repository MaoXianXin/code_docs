# 转换YOLO标注到VOC格式的Python脚本文档

## 概述
本脚本用于将YOLO格式的标注文件转换为VOC (Pascal Visual Object Classes) 格式。这对于在不同的机器学习框架间迁移数据集或进行数据增强等任务非常有用。脚本支持命令行参数输入，便于批处理和集成到其他工作流程中。

## 功能
- 加载YOLO格式的类别列表。
- 检测和解析YOLO格式的标注文件。
- 查找与YOLO标注文件对应的图像文件。
- 将YOLO标注转换为VOC格式的坐标。
- 生成VOC格式的XML标注文件。

## 使用前提
- Python环境已安装。
- 已安装`PIL`库用于图像处理。
- 标注文件和图像文件位于同一目录或指定目录下。

## 参数说明
- `--folder`：包含YOLO txt文件的目录的路径。
- `--classes`：包含YOLO类别的文件路径（通常是classes.txt）。

## 使用方法
运行脚本前，请确保已经安装了所有必要的依赖项，并且YOLO标注文件及对应的图像文件已准备好。

命令行示例：
```shell
python convert_yolo_to_voc.py --folder /path/to/yolo/files --classes /path/to/classes.txt
```

## 代码结构

### 导入模块
```python
import os
import re
from PIL import Image
import argparse
```

### 主要函数

#### `load_classes(file_path)`
加载类别列表。

#### `is_number(n)`
检查一个字符串是否可以转换为浮点数。

#### `find_matching_image(base_file_name, search_dir)`
在指定目录中查找与YOLO标注文件对应的图像文件。

#### `convert_yolo_to_voc(line, classes, img_width, img_height)`
将一行YOLO格式的标注转换为VOC格式的坐标。

#### `process_yolo_file(yolo_file, classes)`
处理单个YOLO标注文件，生成VOC格式的XML文件。

#### `main(args)`
解析命令行参数并处理整个目录的YOLO标注文件。

### 脚本的工作流
1. 解析命令行参数。
2. 加载类别列表。
3. 更改工作目录到包含YOLO文件的目录。
4. 遍历目录中的每个YOLO文件并进行处理。
5. 打印完成转换的消息。

## 输出格式
输出为XML格式的VOC标注文件，每个YOLO标注文件对应一个XML文件。

## 注意事项
- 脚本假设图像为三通道彩色图像（RGB）。
- 如果无法找到对应的图像文件，将不会生成VOC标注文件。
- 类别ID应从0开始，连续编号。

## 示例
以下是一个转换后的VOC标注文件的简单示例：

```xml
<annotation>
    <folder>XML</folder>
    <filename>image1.jpg</filename>
    <path>/path/to/image1.jpg</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>1920</width>
        <height>1080</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>person</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>100</xmin>
            <ymin>200</ymin>
            <xmax>400</xmax>
            <ymax>600</ymax>
        </bndbox>
    </object>
</annotation>
```

请根据实际情况调整脚本参数和路径。如果有任何问题或需要进一步的帮助，请联系脚本作者。