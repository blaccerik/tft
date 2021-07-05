import tkinter as tk
from tkinter import ttk
from predict_best_comp import Predict

class App:
    def __init__(self, root):

        p = Predict()

        # self.id_to_champ = p.id_to_champ
        # self.id_to_item = p.id_to_item

        self.p = p

        # configure the grid

        self.start = 0
        self.root = root
        # self.sb.grid(column=0, row=0)

        frame = tk.Frame(root)
        frame.grid(column=0, row=0)

        self.canvas = tk.Canvas(frame, bg="yellow", width=250)
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
        for i in range(59):
            champ = self.p.s.id_to_champ[i]
            info = tk.Label(frame2, text=champ)
            info.grid(column=0, row=i)
            # off = tk.IntVar()
            # off.set(0)
            label = tk.Checkbutton(frame2)
            label.bind("<Button-1>", self.click_champ)
            label.grid(column=1, row=i)
            self.champ_list.append(label)
            self.champ_list_values.append(False)


        frame2 = tk.Frame(root)
        frame2.grid(row=0, column=1)

        self.canvas2 = tk.Canvas(frame2, bg="yellow", width=250)
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
        self.item_list_values = {}
        # self.item_list_ids = []
        some_list = list(self.p.s.id_to_item.keys())
        for i in range(108):
            # info = tk.Label(frame3, text="text")
            # info.grid(column=0, row=i)
            item_id = some_list[i]
            name = self.p.s.id_to_item[item_id]
            label = tk.Label(frame3, text=f"{name}: {0}")
            label.grid(column=0, row=i)
            # label.pack()
            label.bind("<Button-1>", self.left_click_item)
            label.bind("<Button-3>", self.right_click_item)
            self.item_list.append(label)
            self.item_list_values[i] = {"name": name, "value": 0, "id": item_id}


        res = tk.Button(root, text="Result", command=self.res, padx=50)
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
            self.champ_list_values[a] = True

    def left_click_item(self, event):
        # print(event.widget)
        # print(self.item_dict)
        a = self.item_list.index(event.widget)
        b = self.item_list_values[a]
        value = b["value"]
        if value != 0:
            self.item_list_values[a]["value"] = value - 1
            self.item_list[a]["text"] = f"{b['name']}: {value - 1}"
        # a = self.label["text"]
        # self.label['text'] = a - 1

    def right_click_item(self, event):

        a = self.item_list.index(event.widget)
        b = self.item_list_values[a]
        value = b["value"]
        if value != 9:
            self.item_list_values[a]["value"] = value + 1
            self.item_list[a]["text"] = f"{b['name']}: {value + 1}"

    def res(self):
        lista = []
        for i in self.item_list_values:
            val = self.item_list_values[i]
            id = val["id"]
            value = val["value"]
            for j in range(value):
                lista.append(id)
        dicta = {}
        for i in range(len(self.champ_list_values)):
            if self.champ_list_values[i]:
                dicta[i] = 1
        top5 = self.p.predict_main(dicta,
                            lista,
                            5,
                            {},
                            [])
        same_length(top5)


def same_length(top5):
    print("score key  cs   ss   es  s ci cp ei ep si")
    for top in top5:
        scr = "{:2.3f}".format(top[0])
        key = "{:2}".format(top[1])
        a = "{:2.2f}".format(top[2])
        b = "{:2.2f}".format(top[3])
        c = "{:2.2f}".format(top[4])
        s = "{:2}".format(top[5])
        sa = "{:2}".format(top[6])
        sb = "{:2}".format(top[7])
        sc = "{:2}".format(top[8])
        sd = "{:2}".format(top[9])
        ss = "{:2}".format(top[10])
        print(scr, key, a,b,c,s,sa,sb,sc,sd,ss)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()