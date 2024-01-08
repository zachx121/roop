#!/bin/bash
set -e
NAME=$2
S_IMG="heads/${NAME}.png"
# 遍历当前目录下的所有文件
for file in "$1"/*; do
    # 检查是否为文件
    if [ -f "$file" ]; then
        # 获取文件名（不带扩展名）
        f_dirname=$(dirname "$file")
        f_basename=$(basename "$file")
        output="${f_dirname}"/"${NAME}"_"${f_basename}"
        echo f_dirname: "${f_dirname}"
        echo f_basename: "${f_basename}"
        echo output: "${output}"

        # 执行 python 命令
        python run.py --execution-provider cuda -s "$S_IMG" -t "${file}" -o "${output}" --frame-processor face_swapper --execution-threads 15
    fi
done

