#!/bin/python
# -*- coding=utf8 - *-
#所有print函数均为实验中的步骤
import cv2
import numpy as np
#from PIL import Image（本来想用该库中的方法显示图片，后发现cv2中的imwrite函数更简单）
#watermark="Congratulations,guys!You're so clever!";#水印信息
#watermark_length=len(watermark);#水印长度
#watermark_length_binary='{:08b}'.format(watermark_length);#长度的二进制表示
#print(watermark_length_binary);


def embed(embed_path,watermark):
   watermark_length=len(watermark);#水印长度
   watermark_length_binary='{:08b}'.format(watermark_length);#长度的二进制表示
   im_array = cv2.cv2.imread(embed_path, cv2.cv2.IMREAD_GRAYSCALE)#加载灰度图像
   line_array=im_array.shape[0];#获取该数组的行数
   colum_array=im_array.shape[1];#获取该数组的列数
   im_array_flatten = im_array.flatten()#变成一维数组
   for i in range(0, 8):#获得前 8 个像素灰度值的最低位，并修改为水印长度
         new_im_array_flatten='{:08b}'.format(im_array_flatten[i]);#将灰度值转为二进制形式
         new_im_array_flatten=new_im_array_flatten[:7]+watermark_length_binary[i];#修改最低有效位
         #print(new_im_array_flatten);
         im_array_flatten[i]=int(new_im_array_flatten,2);#将修改后的二进制数改为十进制数
         #print(im_array_flatten[i]);
         #print(im_array_flatten);

  


   for i in range(watermark_length):#从0-水印长度
        ascii_str=ord(watermark[i]);#获得字符的ASCII码
        #print(ascii_str);
        str_binary='{:08b}'.format(ascii_str);#将ASCII码转为二进制
        #print(str_binary);
        k=0;
        for j in range(8 * (i + 1), 8 * (i + 1) + 8):#获取下8个像素值的最低有效位
             new_im_array_flatten='{:08b}'.format(im_array_flatten[j]);
             #print(new_im_array_flatten);
             #print(str_binary[k]);
             new_im_array_flatten=new_im_array_flatten[:7]+str_binary[k];
             k=k+1;
             #print(new_im_array_flatten);
             im_array_flatten[j]=int(new_im_array_flatten,2);#转为十进制
             
   




   last_array=im_array_flatten.reshape((line_array,colum_array));#将一维数组转为二维数组
   #cv2.cv2.imshow("The Picture With Watermark",last_array);#显示图片
   #cv2.cv2.waitKey(0);
   cv2.cv2.imwrite("cwxnew.png", last_array);#保存图片在根目录下


def extract(embed_path):
    im_array = cv2.cv2.imread(embed_path, cv2.cv2.IMREAD_GRAYSCALE)#加载灰度图像
    #print(im_array);
    im_array_flatten = im_array.flatten()#变成一维数组
    #print(im_array_flatten);
    length_bin_string = '0b'
    for i in range(0, 8):#获得前 8 个像素灰度值的最低位，并存在length_bin_string
        if im_array_flatten[i] & 1 == 0:
            #print(im_array_flatten[i]&1);
            length_bin_string += '0'
            
        else:
            length_bin_string += '1'
            #print(im_array_flatten[i]&1);
    


    watermark_length = int(length_bin_string, 2)#将二进制数据转换为十进制
    #print(watermark_length);
    watermark = ''#用来存储水印信息
    for i in range(watermark_length):#从0-水印长度
        char_bin_string = '0b'
        for j in range(8 * (i + 1), 8 * (i + 1) + 8):#获取下8个像素值的最低有效位
            if im_array_flatten[j] & 1 == 0:
                char_bin_string += '0'
            else:
                char_bin_string += '1'
    #char_bin_string存储水印信息各个字符的二进制
        char = chr(int(char_bin_string, 2))#将二进制数据转为字符串
        
        watermark += char
    
    print(watermark)
    #return watermark
      



if __name__ == '__main__':#主函数入口
        #embed('cwx.png','successfully!')
        extract('cwxnew.png')#使用cwx.bmp进行嵌入水印

         