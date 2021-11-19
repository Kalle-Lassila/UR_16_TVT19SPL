import tkinter
from tkinter.constants import BOTTOM

root = tkinter.Tk()
root.title("Hello GUI!")
root.geometry('320x200')

lbl = tkinter.Label(root, text="This is a label")
lbl.grid()
txt = tkinter.Entry(root, width=10)
txt.grid(column=0,row=1)
def click():
    lbl.configure(text="bork")

btn = tkinter.Button(root, text = "click me", fg="red", command=click)
btn.grid(column=1, row=0)
















root.mainloop()