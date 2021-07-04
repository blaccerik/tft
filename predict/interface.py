import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        # configure the grid

        self.start = 0
        self.root = root
        # self.sb.grid(column=0, row=0)

        frame = tk.Frame(root, bg="green")
        frame.grid(column=0, row=0)

        self.canvas = tk.Canvas(frame, bg="yellow", width=100)
        # self.canvas2.grid(row=0, column=0)

        self.canvas.pack(side=tk.LEFT)
        #
        vsb = tk.Scrollbar(frame, command=self.canvas.yview)
        vsb.pack(side=tk.LEFT, fill="y")

        # frame3 = tk.Frame(self.canvas2, width=40, height=20)

        self.canvas.configure(yscrollcommand=vsb.set)
        self.canvas.bind('<Configure>', self.configure_left)
        #
        frame2 = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=frame2, anchor='nw')

        self.champ_list = []
        self.champ_list_values = []
        for i in range(30):
            info = tk.Label(frame2, text="text")
            info.grid(column=0, row=i)
            off = tk.IntVar()
            off.set(1)
            label = tk.Checkbutton(frame2, variable=off)
            label.bind("<Button-1>", self.click_champ)
            label.grid(column=1, row=i)
            self.champ_list.append(label)
            self.champ_list_values.append(False)


        frame2 = tk.Frame(root)
        frame2.grid(row=0, column=1)

        self.canvas2 = tk.Canvas(frame2, bg="yellow", width=100)
        # self.canvas2.grid(row=0, column=0)

        self.canvas2.pack(side=tk.LEFT)
        #
        vsb2 = tk.Scrollbar(frame2, command=self.canvas2.yview)
        vsb2.pack(side=tk.LEFT, fill="y")

        # frame3 = tk.Frame(self.canvas2, width=40, height=20)

        self.canvas2.configure(yscrollcommand=vsb2.set)
        self.canvas2.bind('<Configure>', self.configure_right)
        #
        frame3 = tk.Frame(self.canvas2)
        self.canvas2.create_window((0,0), window=frame3, anchor='nw')

        self.item_list = []
        self.item_list_values = []
        for i in range(30):
            # info = tk.Label(frame3, text="text")
            # info.grid(column=0, row=i)

            label = tk.Label(frame3, text="text: 0")
            label.grid(column=0, row=i)
            # label.pack()
            label.bind("<Button-1>", self.right_click_item)
            label.bind("<Button-3>", self.left_click_item)
            self.item_list.append(label)
            self.item_list_values.append(0)

        res = tk.Button(root, text="Res", command=self.res)
        res.grid(row=1, column=0)

    def configure_right(self, event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas2.configure(scrollregion=self.canvas2.bbox('all'))

    def configure_left(self, event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def click_champ(self, event):
        a = self.champ_list.index(event.widget)
        b = self.champ_list_values[a]
        if b:
            self.champ_list_values[a] = False
        else:
            # now is checked
            print(a)
            self.champ_list_values[a] = True

    def left_click_item(self, event):
        # print(event.widget)
        # print(self.item_dict)
        a = self.item_list.index(event.widget)
        b = self.item_list_values[a]
        if b != 9:
            self.item_list_values[a] = b + 1
            self.item_list[a]["text"] = f"text: {b + 1}"
        # a = self.label["text"]
        # self.label['text'] = a - 1

    def right_click_item(self, event):

        a = self.item_list.index(event.widget)
        b = self.item_list_values[a]
        if b != 0:
            self.item_list_values[a] = b - 1
            self.item_list[a]["text"] = f"text: {b - 1}"

    def res(self):
        print(self.item_list_values)
        print(self.champ_list_values)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()