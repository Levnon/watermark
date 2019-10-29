import tkinter
def getstr(): 
    if text.get() != '': 
        words = text.get() 
        label["text"] = words 


root = tkinter.Tk() 
root.title('主窗口') 
root.geometry('500x500') 
root.wm_attributes('-topmost', 1) 

text = tkinter.Entry(root, borderwidth=1, width=40) 
text.grid(row=1, column=1) 
label = tkinter.Label(root, text="您好") 
label.grid(row=2, column=1) 
comand = tkinter.Button(root, text="获取", command=getstr, width=10, height=2) 
comand.grid(row=3, column=1) 
root.mainloop()