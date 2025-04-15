import tkinter as tk

window=tk.Tk()
window.title("Word Search Grid")
window.config(bg="white")

frm_b=tk.Frame(window, width=100, height=100, bg="pink")
frm_b.pack(padx=10, pady=10)

label=tk.Label(frm_b, text="", width=100, height=50, bg="white", relief="raised")
label.pack(padx=5, pady=5)






window.mainloop()


























