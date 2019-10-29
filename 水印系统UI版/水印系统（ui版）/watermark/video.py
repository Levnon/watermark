#!/bin/python
# -*- coding=utf8 - *-

import subprocess as sp 
import numpy
import cv2         
import numpy as np  
import string
import embed
#import extract
#新视频没有声音 提出很重复的水印 
def embed_video(input_video,string_info,out_put_video):
    command_read=['ffmpeg',
                  '-i',input_video,
                  '-f','image2pipe',#图像形式且专门放到管道里的形式
                  '-pix_fmt','yuv420p',#视频经常使用的像素方式#像素格式为yuv420p
                  '-c:v','rawvideo','-']#直接把结果放到stdout#原始像素点#'rawvideo',
                  #命令的参数，ffmpeg的读取视频参数
    pipe_read=sp.Popen(command_read,stdout=sp.PIPE,bufsize=10**8)#内存空间（管道的空间)
    
    #读取进程并把输出绑定在管道上（stdout)
    command_write=['ffmpeg',
                  '-y',#是否覆盖已存在的文件，默认覆盖
                  '-f','rawvideo',#以rawvideo读取
                  '-c:v','rawvideo',#编码形式
                  '-s','640*512',#分辨率
                  '-pix_fmt','yuv420p',
                  '-i','-',#从stdin输入
                  '-q:v'#量化级别为2，数字越小，量化级别越低，图像质量越好，级别为‘2’，几乎不压缩
                  ,'2',
                  out_put_video]#输出
    pipe_write=sp.Popen(command_write,stdin=sp.PIPE)
    #把结果绑定到stdin上
    raw_image=pipe_read.stdout.read(640*512*3)#得到输出的图片，第一帧
    while raw_image!=None and len(raw_image)!=0:#保证返回的是一个矩阵，矩阵有值
        image=numpy.fromstring(raw_image,dtype='uint8')#数据类型转换，把raw_image中的数据每八位转为整型
        image=image.reshape((512,640,3))#重新变成想要的三维矩阵
        pipe_read.stdout.flush()#清空前面的管道
        #
        # print(image)
        img_tmp=image[:512,:640,0]#取出Y分量
        #print(img_tmp)
        embed.embed_watermark(img_tmp,string_info)#嵌入水印的代码
        #print(imgg)
        #image[:512,:640,0]=imgg
        #print(image)
        pipe_write.stdin.write(image.tostring())#转回之前的格式
         
        raw_image=pipe_read.stdout.read(640*512*3)#下一帧

def extract_video(input_video):
    command_read=['ffmpeg',
                  '-i',input_video,
                  '-f','image2pipe',#图像形式且专门放到管道里的形式（
                  '-pix_fmt','yuv420p',#视频经常使用的像素方式#像素格式为yuv420p
                  '-c:v','rawvideo'#原始像素点
                  ,'-']#直接把结果放到stdout
                  #命令的参数，ffmpeg的读取视频参数
    pipe_read=sp.Popen(command_read,stdout=sp.PIPE,bufsize=10**8)#内存空间（管道的空间)
    #读取进程并把输出绑定在管道上（stdout)
    raw_image=pipe_read.stdout.read(640*512*3)#得到输出的图片，第一帧
    info=''
    while raw_image!=None and len(raw_image)!=0:#保证返回的是一个矩阵，矩阵有值
        image=numpy.fromstring(raw_image,dtype='uint8')#数据类型转换，把raw_image中的数据每八位转为整型
        image=image.reshape((512,640,3))#重新变成想要的三维矩阵
        pipe_read.stdout.flush()#清空前面的管道

        img_tmp=image[:512,:640,0]#取出Y分量
        str=embed.extract_watermark(img_tmp)
        info+=str
        raw_image=pipe_read.stdout.read(640*512*3)
    #print(info)



if __name__ == '__main__':
        #embed_video("my.mp4","myy.mp4")

        #print("嵌入成功！")
        extract_video("myy.mp4")
        print("提取成功！")
