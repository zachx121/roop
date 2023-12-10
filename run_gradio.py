import gradio as gr
import subprocess
import os
import numpy as np
from PIL import Image

# 定义处理函数
def process_images(head_image, target_image, use_enhancer):
    # 保存上传的图片
    Image.fromarray(head_image).save("head.jpeg")
    Image.fromarray(target_image).save("target.jpeg")

    # 执行图像处理命令
    processor = "face_swapper face_enhancer" if use_enhancer else "face_swapper"
    command = "python run.py -s head.jpeg -t target.jpeg -o output.jpeg --frame-processor %s" % processor
    subprocess.run(command, shell=True)

    # 返回处理后的图像
    processed_image = np.array(Image.open("output.jpeg"))
    return processed_image


def process_videos(head_image, target_video_fp, use_enhancer):
    Image.fromarray(head_image).save("head.jpeg")
    print("target_video_fp is %s" % target_video_fp)
    # 执行图像处理命令
    processor = "face_swapper face_enhancer" if use_enhancer else "face_swapper"
    command = "python run.py -s head.jpeg -t %s -o output.mp4 --frame-processor %s" % (target_video_fp, processor)
    subprocess.run(command, shell=True)

    # 返回处理后的图像
    return "output.mp4"


# 创建Gradio界面
# 控制图片的比例
with gr.Blocks() as demo:
    gr.Markdown("图像处理界面")
    with gr.Row():
        head_image = gr.Image(label="上传 'head.jpeg' 图像").style(height=400)
        target_image = gr.Image(label="上传 'target.jpeg' 图像").style(height=400)
        target_video = gr.Video(label="上传视频", type="file").style(height=400)
    enhancer_checkbox = gr.Checkbox(label="启用 enhancer")
    with gr.Row():
        btn_image = gr.Button("处理图像")
        btn_video = gr.Button("处理视频")
    with gr.Row():
        output_image = gr.Image(label="处理后的图像").style(height=400)
        output_video = gr.Video(label="处理后的视频").style(height=400)

    btn_image.click(process_images,
                    inputs=[head_image, target_image, enhancer_checkbox],
                    outputs=output_image)

    btn_video.click(process_videos,
                    inputs=[head_image, target_video, enhancer_checkbox],
                    outputs=output_video)

# 启动Gradio界面
demo.launch(server_port=6006)