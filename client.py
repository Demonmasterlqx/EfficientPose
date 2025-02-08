import requests
import base64
import io
import numpy as np
import cv2

# 服务器接口地址
url = "http://localhost:8081/process"

# 要上传的图片路径
video_path = "/home/lqx/code/composeimagestovideo/build/material.mp4"  # 请确保该图片文件存在

def main():
    # 读取图片文件，并上传到服务端
    # with open(video_path, "rb") as f:
    #     files = {"file": f}
    #     response = requests.post(url, files=files)
    
    video=cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    videow=cv2.VideoWriter("result.mp4",cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    if video.isOpened==False:
        print("fail to open video")
        return
    
    while video.isOpened():
        ret, frame = video.read()
        if not ret :
            print("finish")
            break
        cv2.imwrite("image.jpg",frame)
        with open("image.jpg", "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files)
        if response.status_code == 200:
            # 解析 JSON 响应数据
            data = response.json()
            image_base64 = data.get("image_base64")
            boxes = data.get("boxes")
            scores = data.get("scores")
            labels = data.get("labels")
            rotations = data.get("rotations")
            translations = data.get("translations")
            
            print("响应中的 boxes:", boxes)
            print("响应中的 scores:", scores)
            print("响应中的 labels:", labels)
            print("响应中的 rotations:", rotations)
            print("响应中的 translations:", translations)
            
            # 将 Base64 编码的图片数据解码为二进制数据
            image_bytes = base64.b64decode(str(image_base64))

            print(len(image_base64))
            with open('.out', "w", encoding="utf-8") as f:
                f.write(image_base64)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None or image.size == 0:
                raise ValueError("解码图像失败，可能是 Base64 字符串无效或数据损坏。")
            videow.write(image)
            cv2.imshow("image",image)
            cv2.waitKey(10)
        else:
            print("请求失败，状态码：", response.status_code)
            print("错误信息：", response.text)
    videow.release()

if __name__ == "__main__":
    main()