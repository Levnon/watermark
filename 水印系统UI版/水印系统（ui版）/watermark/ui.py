#!/usr/bin/python
# -*- coding: UTF-8 -*-


import tkinter

def event1(str):
    m=''
    m=str
    print('yyyyy')
    return m

window = tkinter.Tk()       # 用Tk()方法创建主窗口
window.title(string = '水印系统')
background = tkinter.Label(window,text = '水印系统')
background.pack(side = 'top' ,fill = 'both',ipadx=50,ipady=50,expand=0)           #pack()方法用来设置窗口位置,大小等选项
# the first frame
framel1 = tkinter.Frame(window,relief='raised',borderwidth=4)
framel1.pack(side = 'top' , fill = 'both', ipadx=10, ipady=10,expand=0)
tkinter.Button(framel1,text = ('embed')).pack(side='left',padx=10,pady=10)
#bt1.command=tkinter.Tk()
framel2= tkinter.Frame(window,relief='raised',borderwidth=4)
framel2.pack(side = 'top' , fill = 'both', ipadx=10, ipady=10,expand=0)
tkinter.Button(framel2,text = ('extract'),command=lambda:event1('extract')).pack(side='right',padx=10,pady=10)
operate=''
#operate=framel1.bind("<ButtonPress-1>",func=event1('embed'))
#operate=framel2.bind("<Button-1>",func=event1('extract'))
#if tkinter.Button.bell():
#if operate=='':
#operate=framel2.bind(event2('extract'))
   #operate='extract'
tkinter.Button(window,text=("关闭"),command= window.quit).pack(side='bottom')
    #if tkinter.Button.bell():

      #  operate='extract'
window.mainloop()