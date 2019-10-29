import cv2
import subprocess
from subprocess import PIPE
from scipy.ndimage import measurements
import os
from numpy import *
import time
import matplotlib.pyplot as plt
from scipy.ndimage import filters
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
from PIL import Image, ImageDraw
#import face_recognition
import cv2
def translate_video(input_path):
    str_output = './output.mp4'
    str_cmd = '"./ffmpeg/bin/ffmpeg.exe"  -i ' + input_path + '  -b 50000 -s 640x360  ' + str_output

    p = subprocess.Popen(str_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderror = p.communicate()
    print(stdout,stderror)
    return  str_output

#将图片序列转换成视频
def images_ToVideo(imagePath,FPS):
    images_path = imagePath+'/image%d.jpg'
    fps = str(FPS)
    str_cmd='ffmpeg -f image2 -i ' + images_path + ' -r '+fps+' -pix_fmt yuv420p output.mp4'

    p = subprocess.Popen(str_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderror = p.communicate()
    print(stdout, stderror)

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

#图像部分旋转
def rotate(img):    
    pil=Image.open(img)
    box=(1000,0,2000,2000)
    region=pil.crop(box)
    region=region.transpose(Image.ROTATE_180)
    pil.paste(region,box)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.imshow(pil)
    plt.savefig(name)
    return name
#负片效果
def nagetive(img):    
    im=array(Image.open(img))
    im2=255-im
    plt.figure()
    plt.imshow(im2)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.savefig(name)
    return name
#模糊
def dim(img):
    im=array(Image.open(img).convert('L'))
    im2=filters.gaussian_filter(im,5)
    plt.figure()
    plt.imshow(im2)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.savefig(name)
    return name
#变成灰度图片
def P2Gray(img):
    im=array(Image.open(img).convert('L'))
    plt.figure()
    plt.imshow(im)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.savefig(name)
    return name
#图像分割
def segmentation(img):
    im=array(Image.open(img))
    im=array(Image.open(img).convert('L'))
    im=1*(im<128)
    labels,nbrobjects=measurements.label(im)
    plt.figure()
    plt.imshow(im)
    t=str(int(time.time()))
    name=r'./static/'+t+'.jpg'
    plt.savefig(name)
    return name
#物品识别
def shibie(img):
    model = VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None)
    img = image.load_img(img, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(preprocess_input(x))
    results = decode_predictions(preds, top=5)[0]
    for result in results:
        print(result)
def ccode(img,string1):
    t=str(int(time.time()))
    name=r'./static/'+t+'.bmp'
    encode(img, string1, name)
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

def encode(img_path, string1, res_path):
    string2=code(string1)
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
def decode(img_path):
    img_s = cv2.cv2.imread(img_path)
    img_v=cv2.cv2.cvtColor(img_s,cv2.cv2.COLOR_BGR2YCrCb)
    y=img_v[:,:,0]
    m,n=y.shape
    index=0
    hdata = np.vsplit(y,n/8) # 垂直分成高度为8的块
    char_bin_string = ''
    length_bin_string = '0b'
    code=''
    for i in range(0, n//8):
        blockdata = np.hsplit(hdata[i],m/8)
        #垂直分成高度为8的块后,在水平切成长度是8的块, 也就是8x8的块
        for j in range(0, m//8):
            block = blockdata[j]
            #print("block[{},{}] data \n{}".format(i,j,blockdata[j]))
            y1 = cv2.cv2.dct(block.astype(np.float32))
            if y1[0,3]>y1[7,7]:
                char_bin_string += '1'
            if y1[0,3]<y1[7,7]:
                char_bin_string += '0'
    for i in range(0,8):
        for j in range(i*5,(i+1)*5):
            if char_bin_string[j]=='1':
                index+=1
        if index>2:
            length_bin_string+='1'
            code+='1'
        else:
            length_bin_string+='0'
            code+='0'
        index=0
    watermark=''

    lenth = int(length_bin_string, 2)
    for i in range(0,lenth):
        char_string = '0b'
        for j in range(8 * (i + 1), 8 * (i + 1) + 8):
            for k in range(j*5,(j+1)*5):
                if char_bin_string[k]=='1':
                    index+=1
            if index>2:
                char_string+='1'
                code+='1'
            else:
                char_string+='0'
                code+='0'
            index=0
        char = chr(int(char_string, 2))
        watermark += char    
            
    print(watermark)
    return watermark

