import gradio as gr
import subprocess
import os
import numpy as np
from PIL import Image
from datetime import datetime
from roop.utilities import get_temp_output_path,get_temp_directory_path,get_temp_frame_paths

NUM_THREADS_VIDEO = 20  # 8线程大概7.7G
FACE_SIM_DIST = 0.95  # default 0.85, 单人视频时可以把值调大让替换更稳定，避免某些帧没替换到
os.system("mkdir -p heads")
os.system("mkdir -p outputs")

# 定义处理函数
def process_images(head_image_fp, target_image_fp, use_enhancer, face_sim_dist):
    print("head_image_fp is %s" % head_image_fp)
    print("target_image_fp is %s" % target_image_fp)
    processor = "face_swapper face_enhancer" if use_enhancer else "face_swapper"
    prefix = os.path.basename(head_image_fp).split(".")[0]
    output_fname = f"{prefix}_" + ".".join(os.path.basename(target_image_fp).split(".")[:-1]) + "_swap.jpeg"
    command = "python run.py --execution-provider cuda " \
              f"-s '{head_image_fp}' " \
              f"-t '{target_image_fp}' " \
              f"-o '{output_fname}' " \
              f"--similar-face-distance {face_sim_dist} " \
              "--frame-processor %s" % processor
    subprocess.run(command, shell=True)

    # 返回处理后的图像
    return output_fname


# python run.py --execution-provider cuda -s head.jpeg -t target.mp4 -o output.mp4 --frame-processor face_swapper --execution-threads 20
def process_videos(head_image_fp, target_video_fp, use_enhancer, skip_nonswap_frame, use_many_faces, face_sim_dist):
    print("head_image_fp is %s" % head_image_fp)
    print("target_video_fp is %s" % target_video_fp)
    print("skip_nonswap_frame is %s" % skip_nonswap_frame)
    print("use_many_faces is %s" % use_many_faces)
    print("temp_output_path is %s" % get_temp_output_path(target_video_fp))
    print("temp_directory_path is %s" % get_temp_directory_path(target_video_fp))
    processor = "face_swapper face_enhancer" if use_enhancer else "face_swapper"
    prefix = os.path.basename(head_image_fp).split(".")[0]
    output_fname = f"{prefix}_" + ".".join(os.path.basename(target_video_fp).split(".")[:-1]) + "_swap.mp4"
    command = "python run.py --execution-provider cuda " \
              f"-s '{head_image_fp}' " \
              f"-t '{target_video_fp}' " \
              f"-o '{output_fname}' " \
              f"--similar-face-distance {face_sim_dist} " \
              f"--frame-processor {processor} " \
              f"--execution-threads {NUM_THREADS_VIDEO} "
    if skip_nonswap_frame:
        command += "--skip_nonswap_frame "
    if use_many_faces:
        command += "--many-faces "
    print("executing cmd: %s" % command)
    subprocess.run(command, shell=True)

    # 返回处理后的图像
    return output_fname


def process_dropdown_select(inp: gr.SelectData):
    # print(inp.selected,inp.target,inp.value,inp.index)
    imgs = [f"./heads/{i}" for i in os.listdir("./heads")
            if any(i.endswith(suffix) for suffix in ["jpeg", "png", "jpg"])]
    return gr.update(choices=imgs), inp.value


# 创建Gradio界面
# 控制图片的比例
with gr.Blocks() as demo:
    gr.Markdown("图像处理界面")
    with gr.Row():
        # 注意Image的type="filepath"时，拿到的是一个临时路径，basename都是image.png而不是原始文件名
        # 只有Video拿到的是上传文件的原始名称
        head_image_fp = gr.Image(label="上传 'head.jpeg' 图像", type="filepath").style(height=300)
        target_image_fp = gr.Image(label="上传 'target.jpeg' 图像", type="filepath").style(height=300)
        target_video = gr.Video(label="上传视频").style(height=300)
    with gr.Row():
        with gr.Column():
            img_choices = [f"./heads/{i}" for i in os.listdir("./heads")
                           if any(i.endswith(suffix) for suffix in ["jpeg", "png", "jpg"])]
            dropdown = gr.Dropdown(choices=img_choices, label="select heads")
        with gr.Column():
            with gr.Row():
                enhancer_checkbox = gr.Checkbox(label="启用 enhancer(面部占比大的时候——自拍、怼脸特写，建议启用)")
            with gr.Row():
                skip_nonswap_checkbox = gr.Checkbox(label="不保存没有实现替换的帧")
            with gr.Row():
                use_many_faces = gr.Checkbox(label="开启many_face（适用于多人或单人动作大的场景）")
            with gr.Row():
                face_sim_dist = gr.Number(value=FACE_SIM_DIST, label="参数 FACE_SIM_DIST(单人视频时可以把值调大让替换更稳定，避免某些帧没替换到)")
    with gr.Row():
        btn_image = gr.Button("处理图像")
        btn_video = gr.Button("处理视频")
    with gr.Row():
        output_image = gr.Image(label="处理后的图像", type="filepath").style(height=300)
        output_video = gr.Video(label="处理后的视频").style(height=300)

    # Listeners
    btn_image.click(process_images,
                    inputs=[dropdown, target_image_fp, enhancer_checkbox, face_sim_dist],
                    outputs=output_image)

    btn_video.click(process_videos,
                    inputs=[dropdown, target_video, enhancer_checkbox, skip_nonswap_checkbox, use_many_faces, face_sim_dist],
                    outputs=output_video)

    dropdown.select(process_dropdown_select, outputs=[dropdown, head_image_fp])

# 启动Gradio界面
demo.launch(server_port=6006)
