#!/bin/bash

# 遇到任何错误时立即退出
set -e

# 加载配置文件（假设配置文件名为config.sh，位于脚本同级目录）
CONFIG_FILE="$(dirname "\$0")/config.sh"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "配置文件不存在: $CONFIG_FILE"
    exit 1
fi
source $CONFIG_FILE

# 定义路径
PREDEFINE_CLASSES_PATH="$DATASETS_PATH/支票要素定位/predefine_classes.txt"
WEIGHTS_PATH="$WORKSPACE_PATH/yolov5/runs/train/exp94/weights/best.pt"
SOURCE_PATH="$DATASETS_PATH/支票要素定位/有效样本-裁剪子图/测试"

# 定义需要检查的类别列表
CATEGORIES="--categories 年 --categories 月 --categories 日 --categories 号码上 --categories 号码下 --categories 出票人账号 --categories 小写金额"

# 检测
cd $YOLOV5_PATH
python detect.py \
    --weights $WEIGHTS_PATH \
    --source $SOURCE_PATH \
    --img $IMG_SIZE \
    --conf-thres $CONF_THRES \
    --device 0 \
    --save-txt \
    --name $PROCESS_NAME

# 后处理
DETECT_PATH="$YOLOV5_PATH/runs/detect/$PROCESS_NAME"
cd $DETECT_PATH

mkdir origin
mv ./*.jpg origin
mv ./labels/* origin
rm -rf ./labels

# 数据格式转换
cd $WORKSPACE_PATH/code_docs/yolov5/数据格式转换
python convert_yolo_to_voc.py \
    --folder $DETECT_PATH/origin \
    --classes $PREDEFINE_CLASSES_PATH

rm $DETECT_PATH/origin/*.txt

# 过滤误分类样本
cd $WORKSPACE_PATH/code_docs/数据集构建
python filter_misclassification_samples.py \
    --root_dir $DETECT_PATH/origin \
    --dest_dir $DETECT_PATH/filter_misclassification

cd $DETECT_PATH/filter_misclassification
if ls *.jpg 1> /dev/null 2>&1; then
    rm *.jpg
fi

# 文件拷贝
cd $WORKSPACE_PATH/code_docs/文件拷贝
python copy_common_named_files.py \
    --folder_list_A $SOURCE_PATH \
    --folder_list_B $DETECT_PATH/filter_misclassification \
    --target_path $DETECT_PATH/filter_misclassification

cd $DETECT_PATH/filter_misclassification
if ls *.xml 1> /dev/null 2>&1; then
    rm *.xml
fi

# 使用变量替代硬编码的类别参数
cd $WORKSPACE_PATH/code_docs/数据集构建
python filter_misdetection_samples.py \
    --root_dir "$DETECT_PATH/origin" \
    --dest_dir "$DETECT_PATH/filter_misdetection" \
    $CATEGORIES

cd $DETECT_PATH/filter_misdetection
if ls *.jpg 1> /dev/null 2>&1; then
    rm *.jpg
fi

cd $WORKSPACE_PATH/code_docs/文件拷贝
python copy_common_named_files.py \
    --folder_list_A $SOURCE_PATH \
    --folder_list_B $DETECT_PATH/filter_misdetection \
    --target_path $DETECT_PATH/filter_misdetection

cd $DETECT_PATH/filter_misdetection
if ls *.xml 1> /dev/null 2>&1; then
    rm *.xml
fi
