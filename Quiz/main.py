import tkinter as tk
from tkinter import ttk
from gui import hauptfenster

root = tk.Tk()
root.title("Modul 3 Quiz")
root.geometry("600x500")
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background=root.cget("background"))
style.configure("TFrame", background=root.cget("background"))
hauptfenster(root)
root.mainloop()