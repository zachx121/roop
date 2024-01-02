#!/bin/bash
set -e
NAME=$2
S_IMG="heads/${NAME}.png"
# 遍历当前目录下的所有文件
for file in "$1"/*; do
    # 检查是否为文件
    if [ -f "$file" ]; then
        # 获取文件名（不带扩展名）
        filename="${file%.*}"
        # 获取文件扩展名
        extension="${file##*.}"
        # 构建输出文件名
        output="${filename}_${NAME}_swap.${extension}"
        echo "S_IMG: ${S_IMG} file: ${file} output: ${output}"
        # 执行 python 命令
        python run.py --execution-provider cuda -s $S_IMG -t ${file} -o ${output} --frame-processor face_swapper --execution-threads 20
    fi
done

