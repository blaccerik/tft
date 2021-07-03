import tkinter as tk
from tkinter import ttk


class App:
    def __init__(self, root):
        # configure the grid

        self.start = 0
        self.root = root
        # self.sb.grid(column=0, row=0)

        frame = tk.Frame(root)
        frame.grid(column=0, row=0)


        # canvas = tk.Canvas(frame)
        # canvas.grid(row=0, column=0, sticky="news")
        #
        # # Link a scrollbar to the canvas
        # vsb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        # vsb.grid(row=0, column=1, sticky='ns')
        # canvas.configure(yscrollcommand=vsb.set)


        text = tk.Text(frame, width=40, height=20)
        text.grid(column=0, row=0)

        vsb = tk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky='ns')

        # tk.Scrollbar(text, orient="vertical")
        # text.pack(side="top", fill="both", expand=True)
        self.chkbuttons = [tk.Checkbutton(text="checkbutton %s" % i, padx=0, pady=0, bd=0)
                           for i in range(49)]
        for cb in self.chkbuttons:
            text.window_create("end", window=cb)
            text.insert("end", "\n")
            cb.bind("<Button-1>", self.selectstart)
            # cb.bind("<Shift-Button-1>", self.selectrange)

        # root.geometry("240x100")
        # root.title('Login')
        # root.resizable(0, 0)
        # root.columnconfigure(0, weight=1)
        # root.columnconfigure(1, weight=5)

        # username
        # username_label = ttk.Label(root, text="Username:")

        # self.CheckVar = tk.IntVar(value=0)
        #
        # username_label = ttk.Checkbutton(root, text="checkbutton", variable=self.CheckVar, command=self.click_me)
        # username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        #
        # username_entry = ttk.Entry(root)
        # username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
        #
        # # password
        # password_label = ttk.Label(root, text="Password:")
        # password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        #
        # password_entry = ttk.Entry(root, show="*")
        # password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
        #
        # # login button
        login_button = ttk.Button(root, text="Results", command=self.click_me)
        login_button.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

    def click_me(self):
        print("aaa")

    def selectstart(self, event):
        self.start = self.chkbuttons.index(event.widget)
        print(event)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()