import gradio as gr
import subprocess
import os
import numpy as np
from PIL import Image

# 定义处理函数
def process_images(head_image, target_image):
    # 保存上传的图片
    Image.fromarray(head_image).save("head.jpeg")
    Image.fromarray(target_image).save("target.jpeg")

    # 执行图像处理命令
    command = "python run.py -s head.jpeg -t target.jpeg -o output.jpeg --frame-processor face_swapper face_enhancer"
    subprocess.run(command, shell=True)

    # 返回处理后的图像
    processed_image = np.array(Image.open("output.jpeg"))
    return processed_image

# 创建Gradio界面
# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("图像处理界面")
    with gr.Row():
        head_image = gr.Image(label="上传 'head.jpeg' 图像")
        target_image = gr.Image(label="上传 'target.jpeg' 图像")
    with gr.Row():
        button = gr.Button("处理图像")
    output_image = gr.Image(label="处理后的图像", shape=(500, 500))

    button.click(process_images, inputs=[head_image, target_image], outputs=output_image)

# 启动Gradio界面
demo.launch(server_port=6006)
