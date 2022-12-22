import tkinter as tk
from tkinter import simpledialog


win = tk.Tk()
win.geometry("100x50")

def take_user_input_for_something():
    user_input = simpledialog.askstring("Введите силу тока")
    if user_input != "":
        print(user_input)

menubar = tk.Menu(win)
dropDown = tk.Menu(menubar, tearoff = 0)
dropDown.add_command(label = "Do something", command=take_user_input_for_something)

# this entry field is not really needed her.
# however I noticed you did not define this widget correctly
# so I put this in to give you an example.
my_entry = tk.Entry(win)
my_entry.pack()

menubar.add_cascade(label = "Drop Down", menu = dropDown)
win.config(menu = menubar)

win.mainloop()