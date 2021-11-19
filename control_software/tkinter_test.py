import tkinter
from tkinter import scrolledtext
from tkinter.constants import INSERT
window = tkinter.Tk()
window.title("Scrolling terminal")
output_box = scrolledtext.ScrolledText(window, wrap = tkinter.WORD, width = 41, height = 10, font = ("Times New Roman", 12))

input_box = tkinter.Entry(width=40, font=("Times New Roman", 12))

def handler(something):
    input = input_box.get()
    output_box.configure(state=tkinter.NORMAL)
    input_box.delete(0,tkinter.END)
    output_box.insert(INSERT, input+"\n")
    output_box.configure(state=tkinter.DISABLED)


output_box.grid(column=0, row=10)
output_box.configure(state="disabled")
input_box.grid(column=0,row=11)

window.bind('<Return>', handler)
window.mainloop()