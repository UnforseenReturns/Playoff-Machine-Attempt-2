import tkinter as tk

root = tk.Tk()
root.title("Test Window")
root.geometry("300x200")
label = tk.Label(root, text="If you see this, tkinter is working!")
label.pack(pady=20)
root.mainloop()