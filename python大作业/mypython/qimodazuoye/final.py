import cv2
import VideoUtils as utils
from PIL import Image
import os
import matplotlib.pyplot as plt


class Video(object):
    """
    视频类
    video_path：视频路径
    _video_capture：opencv，VideoCapture实例
    frame_count：视频的帧数目
    frame_height：视频的高
    frame_weight：视频的宽
    """
    def __init__(self,file_path):
        self.video_path = file_path
        self.__video_capture = cv2.cv2.VideoCapture(file_path)
        self.frame_count = int(self.__video_capture.get(cv2.cv2.CAP_PROP_FRAME_COUNT))
        self.frame_height = self.__video_capture.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_weight = self.__video_capture.get(cv2.cv2.CAP_PROP_FRAME_WIDTH)

    #通过传入帧位置获取视频帧
    def getFrame_byPos(self,flag):
        self.__video_capture.set(cv2.cv2.CAP_PROP_POS_FRAMES,flag)
        _,img = self.__video_capture.read()

        return cv2.cv2.cvtColor(img,cv2.cv2.COLOR_BGR2RGB)
    #逐一读取视频帧
    def getFrame(self):
        _,img = self.__video_capture.read()

        return cv2.cv2.cvtColor(img,cv2.cv2.COLOR_BGR2RGB)
    #得到当前的帧位置
    def  getPos(self):
        return self.__video_capture.get(cv2.cv2.CAP_PROP_POS_FRAMES)


class Video_processing(object):
    """
    视频处理类
    video：视频类实例
    image_path：存放中间结果的文件夹
    """
    def __init__(self,src_video,fps):
        self.video = Video(file_path=src_video)
        self.FPS = fps
        self.image_path = './static'

    #处理器
    def processor(self,process_Code,img):
        if process_Code=='hsv':
            process_out = utils.RGB2HSV(img)
        elif process_Code=='gray':
            process_out = utils.RGB2Gray(img)
        elif process_Code=='equal':
            process_out = utils.equal_histogram(img)
        elif process_Code=='canny':
            process_out = utils.Canny(img)


        return process_out

    #视频处理函数
    def processing(self,code):
        frame_count = self.video.frame_count

        for i in range(frame_count):
            img = self.video.getFrame()
            img_out = self.processor(code,img)
            utils.save_image(img_out,i)

        utils.images_ToVideo(self.image_path,self.FPS)
if __name__ == '__main__':
    stype=input('请输入操作类型：')
    if stype=='图片':
        pname=input('请输入图片名称：')
        ttype=input('请输入图片操作类型：')
        if ttype=='旋转':
            utils.rotate(pname)
        elif ttype=='负片':
            utils.nagetive(pname)
        elif ttype=='模糊':
            utils.dim(pname)
        elif ttype=='灰度':
            utils.P2Gray(pname)
        elif ttype=='图像分割':
            utils.segmentation(pname)
        elif ttype=='物品识别':
            utils.shibie(pname)
        elif ttype=='嵌入水印':
            watermark=input('请输入嵌入的水印：')
            utils.ccode(pname,watermark)
        elif ttype=='水印解码':
            utils.decode(pname)
        else:
            print('错误，请重新输入')

    if stype=='视频':
        vname=input('请输入视频名称：')
        videoProcess = Video_processing(vname,24)
        ttype=input('请输入视频操作类型：')
        videoProcess.processing(ttype)