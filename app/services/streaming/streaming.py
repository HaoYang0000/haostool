
import time
import threading
from io import BytesIO
import cv2
from PIL import ImageGrab, Image, ImageDraw
import os
os.environ['DISPLAY'] = ':0'

import pyautogui

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    def __init__(self):
        self.events = {}

    def wait(self):
        ident = get_ident()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None
    frame = None
    last_access = 0
    event = CameraEvent()

    def __init__(self):
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        BaseCamera.last_access = time.time()

        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()
            time.sleep(0)
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None

class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        # camera = cv2.VideoCapture(Camera.video_source)
        # if not camera.isOpened():
        #     raise RuntimeError('No camara is opened')

        while True:
            image = ImageGrab.grab()  # 获取屏幕数据
            x, y = pyautogui.position()
            draw = ImageDraw.Draw(image)
            draw.ellipse(
                xy=[(x-10,y-10), (x+10,y+10)],
                fill="red",
                outline="red"
            )
            
            # w, h = image.size
            image = image.resize((1366, 750), Image.ANTIALIAS)  # 图片缩放
            output_buffer = BytesIO()  # 创建二进制对象
            image.save(output_buffer, format='JPEG', quality=100)  # quality提升图片分辨率
            frame = output_buffer.getvalue()  # 获取二进制数据
            yield frame  # 生成器返回一张图片的二进制数据

# from PIL import ImageGrab
# import  numpy as np
# import  cv2

# class streaming:
#     fps = 20
#     start = 3  # 延时录制
#     end = 15  # 自动结束时间
    
#     curScreen = ImageGrab.grab()  # 获取屏幕对象
#     height, width = curScreen.size
    
#     video = cv2.VideoWriter('video02.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (height, width))
    
#     imageNum = 0
#     while True:
#         imageNum += 1
#         captureImage = ImageGrab.grab()  # 抓取屏幕
#         frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
    
#         # 显示无图像的窗口
#         cv2.imshow('capturing', np.zeros((1, 255), np.uint8))
    
#         # 控制窗口显示位置，方便通过按键方式退出
#         cv2.moveWindow('capturing', height - 100, width - 100)  
#         if imageNum > fps * start:
#             video.write(frame)
#         # 退出条件    
#         if cv2.waitKey(50) == ord('q') or imageNum > fps * end:
#             break
#     video.release()
#     cv2.destroyAllWindows()