#!/bin/bash

# 遇到任何错误时立即退出
set -e

# 定义公共参数
PROCESS_NAME="data_analysis"
PREDEFINE_CLASSES_PATH="/home/mao/datasets/支票要素定位/predefine_classes.txt"
WEIGHTS_PATH="/home/mao/workspace/yolov5/runs/train/exp94/weights/best.pt"
SOURCE_PATH="/home/mao/datasets/支票要素定位/有效样本-裁剪子图/all-支票-现金支票-转账支票-filterBySimilarity"
IMG_SIZE=640
CONF_THRES=0.7

# 定义需要检查的类别列表
CATEGORIES="--categories 年 --categories 月 --categories 日 --categories 号码上 --categories 号码下 --categories 出票人账号 --categories 小写金额"

cd /home/mao/workspace/yolov5
python detect.py \
    --weights $WEIGHTS_PATH \
    --source $SOURCE_PATH \
    --img $IMG_SIZE \
    --conf-thres $CONF_THRES \
    --device 0 \
    --save-txt \
    --name $PROCESS_NAME

# 跳转到目标文件夹
cd /home/mao/workspace/yolov5/runs/detect/$PROCESS_NAME

# 创建一个名为origin的新文件夹
mkdir origin

# 移动所有jpg文件到origin文件夹
mv ./*.jpg origin

# 移动labels文件夹下的所有内容到origin文件夹
mv ./labels/* origin

# 删除labels文件夹
rm -rf ./labels

# 跳转到数据格式转换的脚本所在的目录
cd /home/mao/workspace/code_docs/yolov5/数据格式转换

# 运行python脚本进行格式转换
python convert_yolo_to_voc.py \
    --folder /home/mao/workspace/yolov5/runs/detect/$PROCESS_NAME/origin \
    --classes $PREDEFINE_CLASSES_PATH

# 删除origin文件夹中的所有txt文件
rm /home/mao/workspace/yolov5/runs/detect/$PROCESS_NAME/origin/*.txt

cd /home/mao/workspace/code_docs/数据集构建
python filter_misclassification_samples.py \
    --root_dir /home/mao/workspace/yolov5/runs/detect/$PROCESS_NAME/origin \
    --dest_dir /home/mao/workspace/yolov5/runs/detect/$PROCESS_NAME/filter_misclassification

# 使用变量替代硬编码的类别参数
python filter_misdetection_samples.py \
    --root_dir "/home/mao/workspace/yolov5/runs/detect/$PROCESS_NAME/origin" \
    --dest_dir "/home/mao/workspace/yolov5/runs/detect/$PROCESS_NAME/filter_misdetection" \
    $CATEGORIES