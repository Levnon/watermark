# coding:utf-8
from scipy.ndimage import measurements
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, send_from_directory
import os
import cv2
from werkzeug.utils import  secure_filename
import time

from numpy import  *
import subprocess
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
from subprocess import PIPE
from numpy import *
from scipy.ndimage import measurements
import face_recognition
from PIL import Image
import os
import matplotlib.pyplot as plt
from scipy.ndimage import filters
from PIL import Image, ImageDraw
import face_recognition


def translate_video(input_path):
    str_output = './static/output.mp4'
    str_cmd = '"./ffmpeg/bin/ffmpeg.exe"  -i ' + input_path + '  -b 50000 -s 426*240  ' + str_output

    p = subprocess.Popen(str_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderror = p.communicate()
    print(stdout,stderror)
    return  str_output

#将图片序列转换成视频
def images_ToVideo(imagePath,FPS):
    images_path = imagePath+'/image%d.jpg'
    #print(images_path)
    fps = str(FPS)
    str_cmd = '"./ffmpeg/bin/ffmpeg.exe" -f image2 -i ' + images_path + ' -r ' + fps + ' -pix_fmt yuv420p  ./static/output.mp4'
    p = subprocess.Popen(str_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderror = p.communicate()
    print(stdout, stderror)
    #print("success")
#将RGB图片转变为HSV空间
def RGB2HSV(img):
    return cv2.cv2.cvtColor(img,cv2.cv2.COLOR_RGB2HSV)

#将RGB图片变成灰度图片
def RGB2Gray(img):
    return cv2.cv2.cvtColor(img,cv2.cv2.COLOR_RGB2GRAY)

#直方图均衡化
def equal_histogram(img):
    img = RGB2Gray(img)
    return cv2.cv2.equalizeHist(img)

#canny边缘检测
def Canny(img):
    img = RGB2Gray(img)
    img = cv2.cv2.GaussianBlur(img, (3, 3), 0)
    canny = cv2.cv2.Canny(img, 50, 150)
    return canny

def save_image(img,i):
    cv2.cv2.imwrite('./static/image{}.jpg'.format(i), img)
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

    def processor(self, process_Code, img):
        if process_Code == 'hsv':
            process_out =RGB2HSV(img)
        elif process_Code == 'gray':
            process_out = RGB2Gray(img)
        elif process_Code == 'equal':
            process_out = equal_histogram(img)
        elif process_Code == 'canny':
            process_out = Canny(img)
        return process_out
    def processing(self, code):
        frame_count = self.video.frame_count

        for i in range(frame_count):
            img = self.video.getFrame()
            #print('1')
            img_out = self.processor(code, img)
            #print('2')
            save_image(img_out, i)
            #print('3')
            #print('3')

        images_ToVideo(self.image_path, self.FPS)
        return self.image_path+"/output.mp4"
def exeeee3(pic):
    jobs_image = face_recognition.load_image_file("static/jobs.jpg")
    obama_image = face_recognition.load_image_file("static/obama.jpg")
    yyqx_image=face_recognition.load_image_file("static/yyqx.jpg")
    linyi_image=face_recognition.load_image_file("static/linyi.jpg")
    unknown_image = face_recognition.load_image_file("static/"+pic)

    jobs_encoding = face_recognition.face_encodings(jobs_image)[0]
    obama_encoding = face_recognition.face_encodings(obama_image)[0]
    yyqx_encodeing=face_recognition.face_encodings(yyqx_image)[0]
    linyi_encoding=face_recognition.face_encodings(linyi_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([jobs_encoding, obama_encoding,yyqx_encodeing,linyi_encoding], unknown_encoding)
    labels = ['jobs', 'obama','yyqx','linyi']

    #print('results:' + str(results))
    for i in range(0, len(results)):
        if results[i] == True:
            #print('The person is:' + labels[i])
            ppp=labels[i]

    return  ppp

def exeeee2(pic):
    im = array(Image.open("static/"+pic).convert('L'))
    plt.figure()
    plt.imshow(im)
    t = str(int(time.time()))
    name = r'./static/' + t + '.jpg'
    plt.savefig(name)
    return name
def exeeee1(pic):
    model = VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None)
    # model.summary()
    filepath = 'static/'+pic
    img = image.load_img(filepath, target_size=(224, 224))
    # print(img)
    x = image.img_to_array(img)
    # print(x.shape)
    x = np.expand_dims(x, axis=0)
    # print(x)
    preds = model.predict(preprocess_input(x))
    results = decode_predictions(preds, top=5)[0]
    #for result in results:
        #print(result[0])
    return results[0]
def rotate(img):
    pil=Image.open("static/"+img)
    box=(1000,0,2000,2000)
    region=pil.crop(box)
    region=region.transpose(Image.ROTATE_180)
    pil.paste(region,box)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.imshow(pil)
    plt.savefig(name)
    return name

def nagetive(img):
    im=array(Image.open("static/"+img))
    im2=255-im
    plt.figure()
    plt.imshow(im2)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.savefig(name)
    return name


def dim(img):
    im=array(Image.open("static/"+img).convert('L'))
    im2=filters.gaussian_filter(im,5)
    plt.figure()
    plt.imshow(im2)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.savefig(name)
    return name

def segmentation(img):
    im=array(Image.open('static/'+img))
    im=array(Image.open('static/'+img).convert('L'))
    im=1*(im<128)
    labels,nbrobjects=measurements.label(im)
    plt.figure()
    plt.imshow(im)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.savefig(name)
    return name
def code(string1):
    watermark=''
    for i in '{0:08b}'.format(len(string1)):
        for j in range(0,5):
            watermark+=i
    for i in string1:
        bindata='{0:08b}'.format(ord(i))
        for j in bindata:
            for k in range(0,5):
                watermark+=j
    return watermark
def produceImage(file_in, width, height, file_out):
    image = Image.open(file_in)
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    resized_image.save(file_out)
def encode(img_path, string1, res_path):
    string2=code(string1)
    produceImage(img_path, 512, 512, img_path)
    img_s = cv2.cv2.imread(img_path)

    img_v=cv2.cv2.cvtColor(img_s,cv2.cv2.COLOR_BGR2YCrCb)
    y=img_v[:,:,0]
    cr=img_v[:,:,1]
    cb=img_v[:,:,2]
    m,n=y.shape
    index=0
    hdata = np.vsplit(y,n/8) # 垂直分成高度为8的块
    for i in range(0, n//8):
        blockdata = np.hsplit(hdata[i],m/8)
        #垂直分成高度为8的块后,再水平切成长度是8的块, 也就是8x8的块
        for j in range(0, m//8):
            block = blockdata[j]
            #print("block[{},{}] data \n{}".format(i,j,blockdata[j]))
            y1 = cv2.cv2.dct(block.astype(np.float32))
            if(index<len(string2)):
                if string2[index]=='1':
                    if y1[0,3]<y1[7,7]:
                        y1[0,3],y1[7,7]=y1[7,7],y1[0,3]
                if string2[index]=='0':
                    if y1[0,3]>y1[7,7]:
                        y1[0,3],y1[7,7]=y1[7,7],y1[0,3]
                index+=1
            imgarray=cv2.cv2.idct(y1)
            for ii,iii in zip(range(8*i,8*(i+1)),range(0,8)):
                for jj,jjj in zip(range(8*j,8*(j+1)), range(0,8)):
                    y[ii,jj]=imgarray[iii,jjj]
            #print("dct data\n{}".format(Yb))
    img_v[:,:,0]=y
    img_v[:,:,1]=cr
    img_v[:,:,2]=cb
    img= cv2.cv2.cvtColor(img_v,cv2.cv2.COLOR_YCrCb2BGR)
    cv2.cv2.imwrite(res_path,img)

def ccode(img,watermark):
    string1=watermark
    t=str(int(time.time()))
    name=r'./static/'+t+'.bmp'
    imgg='./static/'+img
    encode(imgg, string1, name)
    return name


def decode(img_path):
    img_s = cv2.cv2.imread("static/"+img_path)
    img_v = cv2.cv2.cvtColor(img_s, cv2.cv2.COLOR_BGR2YCrCb)
    y = img_v[:, :, 0]
    m, n = y.shape
    index = 0
    hdata = vsplit(y, n / 8)  # 垂直分成高度为8的块
    char_bin_string = ''
    length_bin_string = '0b'
    code = ''
    for i in range(0, n // 8):
        blockdata = np.hsplit(hdata[i], m / 8)
        # 垂直分成高度为8的块后,在水平切成长度是8的块, 也就是8x8的块
        for j in range(0, m // 8):
            block = blockdata[j]
            # print("block[{},{}] data \n{}".format(i,j,blockdata[j]))
            y1 = cv2.cv2.dct(block.astype(np.float32))
            if y1[0, 3] > y1[7, 7]:
                char_bin_string += '1'
            if y1[0, 3] < y1[7, 7]:
                char_bin_string += '0'
    for i in range(0, 8):
        for j in range(i * 5, (i + 1) * 5):
            if char_bin_string[j] == '1':
                index += 1
        if index > 2:
            length_bin_string += '1'
            code += '1'
        else:
            length_bin_string += '0'
            code += '0'
        index = 0
    watermark = ''

    lenth = int(length_bin_string, 2)
    for i in range(0, lenth):
        char_string = '0b'
        for j in range(8 * (i + 1), 8 * (i + 1) + 8):
            for k in range(j * 5, (j + 1) * 5):
                if char_bin_string[k] == '1':
                    index += 1
            if index > 2:
                char_string += '1'
                code += '1'
            else:
                char_string += '0'
                code += '0'
            index = 0
        char = chr(int(char_string, 2))
        watermark += char

    #print(watermark)
    return watermark

def identify(pic):
    image = face_recognition.load_image_file("static/"+pic)
    face_landmarks_list = face_recognition.face_landmarks(image)

    print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)
    for face_landmarks in face_landmarks_list:
        # Print the location of each facial feature in this image


        for facial_feature in face_landmarks.keys():
            d.line(face_landmarks[facial_feature], width=5)
    # Show the picture
    t = str(int(time.time()))
    name = r'./static/' + t + '.jpg'
    pil_image.save(name)
    return  name


def quanlian(pic):
    image = face_recognition.load_image_file("static/"+pic)
    srcImage = cv2.imread("static/"+pic)
    face_locations = face_recognition.face_locations(image)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))

    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print(
            "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                  right))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(srcImage, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("demo", srcImage)
        t = str(int(time.time()))
        name = r'./static/' + t + '.jpg'
        cv2.imwrite(name,srcImage)
        return  name
app = Flask(__name__)
# 设置静态文件缓存过期时间


@app.route('/')
def index():
    return redirect("/upload")

# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
  while(1):
    if request.method == 'POST':
        f = request.files['file']
        basepath=os.path.dirname(__file__)
        #print(basepath)
        #upload_path=os.path.join(basepath,'static',secure_filename(f.filename))
        x=basepath+'/static/'+f.filename
        f.save(x)
        #img = cv2.imread(basepath+f.filename)
        #str_tm = './static/' + f.filename
        #cv2.imwrite(basepath, img)
        #img = cv2.imread('file')
        #str_tm = './static/' + f.filename
        #cv2.imwrite(str_tm, img)
        pic=f.filename
        #print(pic)
        user_input = request.form.get("wanted")
        #print(user_input)
        watermark=request.form.get("mywatermark")
        if user_input=='物体识别':

             ppp=exeeee1(pic)
             return render_template('wutishibie.html', pic=pic, ppp=ppp)
        if user_input=='人脸识别':
            ppp=exeeee3(pic)
            return render_template('renlianshibie.html', pic=pic, ppp=ppp)
        
        if user_input=='灰度图':
           ppp=exeeee2(pic)
           return   render_template('huidutu.html',pic=pic,ppp=ppp)
        if user_input=='部分旋转':
            ppp=rotate(pic)
            return  render_template('huidutu.html',pic=pic,ppp=ppp)
        if user_input=='负片':
            ppp=nagetive(pic)
            return  render_template('fupian.html',pic=pic,ppp=ppp)
        if user_input=='高斯模糊':
            ppp=dim(pic)
            return render_template('gaosimohu.html', pic=pic, ppp=ppp)
        if user_input=='图像分割':
            ppp=segmentation(pic)
            return render_template('tuxiangqiege.html', pic=pic, ppp=ppp)
        if user_input=='图像水印嵌入':
            ppp=ccode(pic,watermark)

            #print(ppp)
            return render_template('tuxiangshuiyin.html',pic=pic,ppp=ppp)
        if user_input=='图像水印解码':
            ppp=decode(pic)
            #print(ppp)
            return render_template('shuiyinjiema.html', pic=pic, ppp=ppp)
        if user_input=='人脸轮廓识别':
            ppp=identify(pic)
            return render_template('lunkuoshibie.html',pic=pic,ppp=ppp)
        if user_input=='圈出人脸':
            ppp=quanlian(pic)
            return render_template('quanchurenlian.html',pic=pic,ppp=ppp)
        if user_input=='视频灰度处理':
            videoProcess = Video_processing("static/"+pic, 30)
            print(pic)
            ppp=videoProcess.processing("gray")
            #print(ppp)
            return  render_template('shipinhuiduchuli.html',pic=pic,ppp=ppp)
        if user_input=='视频边缘化处理':
            videoProcess = Video_processing("static/" + pic, 30)
            # print(pic)
            ppp = videoProcess.processing("canny")
            # print(ppp)
            return render_template('shipinhuiduchuli.html', pic=pic, ppp=ppp)
        if user_input=='视频均衡化处理':
            videoProcess = Video_processing("static/" + pic, 30)
            # print(pic)
            ppp = videoProcess.processing("equal")
            # print(ppp)
            return render_template('shipinhuiduchuli.html', pic=pic, ppp=ppp)
        if user_input=='视频色彩空间转换':
            videoProcess = Video_processing("static/" + pic, 30)
            # print(pic)
            ppp = videoProcess.processing("hsv")
            # print(ppp)
            return render_template('shipinhuiduchuli.html', pic=pic, ppp=ppp)
    return render_template('index.html')






if __name__ == '__main__':
    # app.debug = True
    app.run()
#host='0.0.0.0',port="5001"
