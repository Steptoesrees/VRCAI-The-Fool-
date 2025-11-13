import tkinter as tk

from tkinter import ttk


class TestWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)




root = tk.Tk()
test = TestWindow(root)
test.mainloop()