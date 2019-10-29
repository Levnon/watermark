# coding=utf-8
import cv2
import numpy as np
from PIL import Image

def main():
    name=input('请输入保存图片的名称：')
    decode( name)

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


if __name__ == '__main__':
    main()
