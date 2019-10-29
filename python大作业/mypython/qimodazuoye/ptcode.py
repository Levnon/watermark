# coding=utf-8
import cv2
import numpy as np
from PIL import Image
def main():
    photo=input('请输入图片名称：')
    watermark=input('请输入需嵌入水印：')
    name=input('请输入保存图片的名称：')
    encode(photo, watermark, name)

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
    print(m,n)
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

if __name__ == '__main__':
    main()