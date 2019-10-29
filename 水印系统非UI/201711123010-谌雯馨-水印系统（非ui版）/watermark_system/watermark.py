import argparse
import video
import audio
import LSB
import testfile 
import tkinter
#import tkMessageBox  
#请输入要进行的操作（不输入则为嵌入），以及要操作的文件的路径
watermark_str='anjing!'
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='数字水印系统:')
    #parser.add_argument('--type', metavar='type', type=str, help='处理文件的类型')
    parser.add_argument('--operate', metavar='operate', type=str, help='操作类型：embed为嵌入,extract为提取')
    parser.add_argument('input', metavar='input', type=str, help='输入文件')
    
    #print('请输入要进行的操作（不输入则为嵌入），以及要操作的文件的路径')
    args = parser.parse_args()
    type =testfile.test(args.input)
    #print(type)
    #print(args.input)
    #print(args.type)
    #print(args.operate)
    if args.operate!='extract':
        args.operate='embed'
    if type.find('video')!=-1:#返回的类型为视频
    #if type=='video':
        if args.operate=='embed':
            video.embed_video(args.input,watermark_str,'newvideo.mp4')
            print("嵌入视频成功")
        if args.operate=='extract':
            video.extract_video(args.input)

    if type.find('image')!=-1:#返回的类型包含图像
    #if type=='picture':
        if args.operate=='embed':
            LSB.embed(args.input,watermark_str)
            print('嵌入图像成功')
        if args.operate=='extract':
            LSB.extract(args.input)
           # print(watermark)
    

    if type.find('audio')!=-1:#返回的类型为音频
   # if type=='audio':
        if args.operate=='embed':
            audio.lsb_watermark(args.input,watermark_str,'cwxnew.wav')
            print('嵌入音频成功')
        if args.operate=='extract':
            audio.recover_lsb_watermark(args.input)