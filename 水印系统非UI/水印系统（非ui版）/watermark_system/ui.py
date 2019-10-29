#!/usr/bin/python
# -*- coding: UTF-8 -*-
 




import tkinter
window = tkinter.Tk()       # 用Tk()方法创建主窗口
window.title(string = '水印系统')
background = tkinter.Label(window,text = '水印系统')
background.pack(side = 'top' ,fill = 'both',ipadx=50,ipady=50,expand=0)           #pack()方法用来设置窗口位置,大小等选项
# the first frame
framel = tkinter.Frame(window,relief='raised',borderwidth=4)
framel.pack(side = 'top' , fill = 'both', ipadx=10, ipady=10,expand=0)
tkinter.Button(framel,text = ('embed')).pack(side='left',padx=10,pady=10)
#bt1.command=tkinter.Tk()
tkinter.Button(framel,text = 'extract').pack(side='left',padx=10,pady=10)

tkinter.Button(window,text=("关闭"),command= window.quit).pack(side='bottom')
window.mainloop()
