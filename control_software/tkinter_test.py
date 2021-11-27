#https://www.geeksforgeeks.org/dropdown-menus-tkinter/
# Import module
from tkinter import *
  
# Create object
root = Tk()
  
# Adjust size
root.geometry("200x200")
  
# Change the label text
def show():
    label.config(text=clicked.get())
  
# Dropdown menu options
options = [
        "192.168.100.10",
        "172.16.140.130",
        "172.16.177.128"
]
  
# datatype of menu text
clicked = StringVar()
  
# initial menu text
clicked.set("192.168.100.10")
  
# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()
  
# Create button, it will change label text
button = Button(root, text="select", command=show).pack()
  
# Create Label
label = Label(root, text=" ")
label.pack()
  
# Execute tkinter
root.mainloop()


##Scrolling terminal example
#import tkinter
# from tkinter import scrolledtext
# from tkinter.constants import INSERT
# window = tkinter.Tk()
# window.title("Scrolling terminal")
# output_box = scrolledtext.ScrolledText(window, wrap = tkinter.WORD, width = 41, height = 10, font = ("Times New Roman", 12))

# input_box = tkinter.Entry(width=40, font=("Times New Roman", 12))

# def handler(something):
#     input = input_box.get()
#     output_box.configure(state=tkinter.NORMAL)
#     input_box.delete(0,tkinter.END)
#     output_box.insert(INSERT, input+"\n")
#     output_box.configure(state=tkinter.DISABLED)


# output_box.grid(column=0, row=10)
# output_box.configure(state="disabled")
# input_box.grid(column=0,row=11)

# window.bind('<Return>', handler)
# window.mainloop()