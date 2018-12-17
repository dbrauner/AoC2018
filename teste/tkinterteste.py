# display_text.py
from tkinter import Tk, Label

root = Tk()

if __name__ == '__main__':
    # Create a label as a child of root window

    a = ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa>\n" +
         "####################>>>>>>>>>>>>>>>>>>>>>>>")

    my_text = Label(root, text=a)
    my_text.pack()
    my_text = Label(root, text=a)
    my_text.pack()

    root.mainloop()
