import argparse
import video
import audio
import LSB
import testfile#进行文件类型测试
import tkinter
watermark_str='anjing!'
input=''
operate=''
def event1(str):
    m=''
    m=str
    global operate
    operate=str
    window.quit()
    #print('yyyyy')
    return m

def event2(shuru):
    global input
    input=shuru
    #window.quit()
    
    label["text"] ='当前文件为：'+ shuru+'，请选择操作为嵌入还是提取！'

def event3(shuru):
    global watermark_str
    watermark_str=shuru
    label["text"] ='当前水印信息为：'+ shuru
if __name__ == '__main__':
    window = tkinter.Tk()       # 用Tk()方法创建主窗口
    
    window.title(string = '水印系统')
    background = tkinter.Label(window,text = '水印系统',bg='light blue')
    background.pack(side = 'left' ,fill = 'both',ipadx=20,ipady=20
    ,expand=0)           #pack()方法用来设置窗口位置,大小等选项
    # the first frame
    framel1 = tkinter.Frame(window,relief='raised',borderwidth=4,bg='light blue')
    framel1.pack(side = 'top' , fill = 'x', ipadx=10, ipady=10,expand=0)
    tkinter.Button(framel1,text = ('嵌入'),bg='yellow',command=lambda:event1('embed')).pack(side='left',padx=10,pady=10)
    #bt1.command=tkinter.Tk()
    framel2= tkinter.Frame(window,relief='raised',borderwidth=4,bg='light blue')
    framel2.pack(side = 'top' , fill = 'x', ipadx=10, ipady=10,expand=0)
    
    tkinter.Button(framel2,text = ('提取'),bg='yellow',command=lambda:event1('extract')).pack(side='left',padx=10,pady=10)
    label = tkinter.Label(window, text="当前无输入文件,请在下面绿色文本框输入文件并提交！") 
    label.pack()
    #operate=framel1.bind("<ButtonPress-1>",func=event1('embed'))
    #operate=framel2.bind("<Button-1>",func=event1('extract'))
    #if tkinter.Button.bell():
    #if operate=='':
    #operate=framel2.bind(event2('extract'))
   #operate='extract'
    framel3= tkinter.Frame(window,relief='raised',borderwidth=4,bg='light blue')
    framel3.pack(side = 'top' , fill = 'both', ipadx=10, ipady=10,expand=0)
    tkinter.Button(window,text=("关闭"),bg='yellow',command= window.quit).pack(side='bottom')
    #if tkinter.Button.bell():

      #operate='extract'
    #root=tkinter.Tk()

    shuru=tkinter.Entry(window,text='输入',bg='light green')
   # var=tkinter.StringVar() 

    #tkinter.Entry(window,textvariable=var) #设置输入框对应的文本变量为var 
    anniu=tkinter.Button(window,text='提交',bg='yellow',command=lambda:event2(shuru.get()))
    shuru.pack()
    anniu.pack()
    shuru=tkinter.Entry(window,text='输入',bg='light green')
   # var=tkinter.StringVar() 
    
    window.mainloop()
   

    parser = argparse.ArgumentParser(description='数字水印系统:')
    #以下为命令行代码：：
    #parser.add_argument('--type', metavar='type', type=str, help='处理文件的类型')
    #parser.add_argument('--operate', metavar='operate', type=str, help='操作类型：embed为嵌入,extract为提取')
    #parser.add_argument('input', metavar='input', type=str, help='输入文件')
    #input='cwxnew.png'
    #args = parser.parse_args()
    #type =testfile.test(args.input)
    type =testfile.test(input)
    #print(type)
    #print(args.input)
    #print(args.type)
    #print(args.operate)
    if type.find('video')!=-1:#返回的类型为视频
    #if type=='video':
        #if args.operate=='embed':
        if operate=='embed':
            video.embed_video(input,watermark_str,'newvideo.mp4')
        if operate=='extract':
        #if args.operate=='extract':
            video.extract_video(input)

    if type.find('image')!=-1:#返回的类型包含图像
    #if type=='picture':
        if operate=='embed':
        #if args.operate=='embed':
            LSB.embed(input,watermark_str)
            print("embed!!!")
        #if args.operate=='extract':
        if operate=='extract':
            LSB.extract(input)
           # print(watermark)
    

    if type.find('audio')!=-1:#返回的类型为音频
   # if type=='audio':
        if operate=='embed':
        #if args.operate=='embed':
            audio.lsb_watermark(input,watermark_str,'cwxnew.wav')
        if operate=='extract':
        #if args.operate=='extract':
            audio.recover_lsb_watermark(input)