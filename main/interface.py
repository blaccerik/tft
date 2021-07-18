import difflib
import tkinter as tk
from tkinter import ttk
from predict_best_comp import Predict
from static_data import Static

class App:
    def __init__(self, root):
        self.s = Static()
        self.p = Predict(self.s)
        # self.id_to_champ = p.id_to_champ
        # self.id_to_item = p.id_to_item
        self.root = root
        # selectors
        frame = tk.Frame(self.root)
        frame.grid(column=0, row=0)
        # champions
        self.selected_champ = "aatrox"
        self.configure_champion_selector(frame)
        # # items
        self.selected_item = "none"
        self.configure_item_selector(frame)

        # all champions "stats"
        self.frame_list = []
        self.frame_dict = {}
        test = ["snow3", "mistyrose3"]
        test2 = ["yellow", "green", "blue"]
        self.player_dict = {}
        for i in range(1, 9):
            frame = tk.Frame(self.root)
            frame.grid(column=0, row=i)

            frame1 = tk.Frame(frame, bg=test[i % 2], width=390, height=50)
            frame1.grid(column=0, row=0)
            frame1.grid_propagate(False)
            frame1.bind("<Button-3>", self.click_on_champion_frame)
            self.frame_list.append(frame1)
            # self.handle_1_row_champions(frame1, i)

            frame2 = tk.Frame(frame, bg=test2[i % 3], width=300, height=50)
            frame2.grid(column=1, row=0)
            self.player_dict[i - 1] = {}
            self.frame_dict[i - 1] = {}

        # buttons
        frame = tk.Frame(self.root, width=690, height=50, bg="pink")
        frame.grid(column=0, row=10)
        frame.grid_propagate(False)
        button = tk.Button(frame, width=30, text="Result", command=self.press_button)
        button.grid()
        button.grid_propagate(False)

    def press_button(self):
        print(self.player_dict)
        champ = self.selected_champ
        self.selected_champ = "ashe"
        self.add_champ_frame(0, 3)
        self.selected_champ = champ

    def click_on_champion_frame(self, event):

        nr = self.frame_list.index(event.widget)
        self.add_champ_frame(nr)

    def add_champ_frame(self, nr, def_value=1):
        champ_dict = self.player_dict[nr]
        if self.selected_champ == "none":
            return
        elif self.selected_champ in champ_dict:
            return

        champ_dict[self.selected_champ] = def_value
        frame = self.frame_list[nr]

        parent = tk.Frame(frame, width=30, height=50, bg="yellow")
        parent.grid(column=len(champ_dict), row=0)
        parent.pack_propagate(False)

        frame2 = tk.Label(parent, bg="orange", text=self.selected_champ, width=4, padx=2, pady=5)
        frame2.grid(column=0, row=0, sticky="W")
        frame2.bind("<Button-1>", self.left_click_item)
        frame2.bind("<Button-3>", self.right_click_item)
        #
        label = tk.Label(parent, text=def_value, padx=13)
        label.grid(column=0, row=1)
        label.bind("<Button-1>", self.left_click_item)
        label.bind("<Button-3>", self.right_click_item)
        # label.grid_propagate(False)

        self.frame_dict[nr][parent] = self.selected_champ

        # name = parent._w
        # self.frame_dict[name] = {"count": 1, "obj": parent, "champ": self.selected_champ}


    def configure_champion_selector(self, frame):
        canvas = tk.Frame(frame, bg="red", width=390, height=25)
        canvas.grid(column=0, row=0)
        canvas.grid_propagate(False)

        prompt = tk.Label(canvas, text='Selected: ')
        prompt.grid(column=0, row=0)

        self.selected_champ_text = tk.StringVar()
        self.selected_champ_text.set(self.selected_champ)
        label = tk.Label(canvas, textvariable=self.selected_champ_text)
        label.grid(column=1, row=0)

        self.champion_entry = tk.Entry(canvas)
        self.champion_entry.bind('<Return>', self.update_selected_champ)  # binding the Return event with an handler
        self.champion_entry.grid(column=2, row=0)

        ok = tk.Button(canvas, text=' ? ', command=self.update_selected_champ)
        ok.grid(column=3, row=0)

    def update_selected_champ(self, event=None):
        value = self.champion_entry.get().lower()
        final = difflib.get_close_matches(value, self.s.champ_to_id)
        if len(final) == 0:
            self.selected_champ = "none"
        else:
            self.selected_champ = final[0]
        self.selected_champ_text.set(self.selected_champ)

    def configure_item_selector(self, frame):
        canvas = tk.Frame(frame, bg="orange", width=300, height=25)
        canvas.grid(column=1, row=0)
        canvas.grid_propagate(False)

        prompt = tk.Label(canvas, text='Selected: ', anchor="w")
        prompt.grid(column=0, row=0)

        self.selected_item_text = tk.StringVar()
        self.selected_item_text.set(self.selected_item)
        label = tk.Label(canvas, textvariable=self.selected_item_text)
        label.grid(column=1, row=0)

        self.item_entry = tk.Entry(canvas)
        self.item_entry.bind('<Return>', self.update_selected_item)  # binding the Return event with an handler
        self.item_entry.grid(column=2, row=0)

        ok = tk.Button(canvas, text=' ? ', command=self.update_selected_item)
        ok.grid(column=3, row=0)

    def update_selected_item(self, event=None):
        value = self.item_entry.get()
        final = difflib.get_close_matches(value, self.s.item_to_id, cutoff=0.3)
        if len(final) == 0:
            self.selected_item = "none"
        else:
            self.selected_item = final[0]
        self.selected_item_text.set(self.selected_item)

    def left_click_item(self, event: tk.Event):

        nr = self.frame_list.index(event.widget.master.master)
        parent = event.widget.master
        champ = self.frame_dict[nr][parent]
        value = self.player_dict[nr][champ] - 1
        if value == 0:
            del self.player_dict[nr][champ]
            del self.frame_dict[nr][parent]
            parent.grid_forget()
            parent.destroy()
            n = 0
            for frame in self.frame_dict[nr]:
                frame.grid(column=n, row=0)
                n += 1
                # print(frame.gr)
        else:
            parent.children["!label2"]["text"] = value
            self.player_dict[nr][champ] = value

    def right_click_item(self, event):
        nr = self.frame_list.index(event.widget.master.master)
        parent = event.widget.master
        champ = self.frame_dict[nr][parent]
        value = self.player_dict[nr][champ] + 1
        if value == 10:
            pass
        else:
            parent.children["!label2"]["text"] = value
            self.player_dict[nr][champ] = value

    # def res(self):
    #     lista = []
    #     for i in self.item_list_values:
    #         val = self.item_list_values[i]
    #         id = val["id"]
    #         value = val["value"]
    #         for j in range(value):
    #             lista.append(id)
    #     dicta = {}
    #     for i in range(len(self.champ_list_values)):
    #         if self.champ_list_values[i]:
    #             dicta[i] = 1
    #     top5 = self.p.predict_main(dicta,
    #                         lista,
    #                         many=5)
    #     for i in self.p.s.comps:
    #         print(i, self.p.s.comps[i]["name"])
    #     same_length(top5)


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
    # import tkinter as tk
    # import tkinter.messagebox as msg


    # def show(event=None):  # handler
    #     msg.showinfo('name', 'Your name is ' + inp.get())
    #
    #
    # m = tk.Tk()
    #
    # prompt = tk.Label(m, text='Name: ')
    # prompt.pack(fill='x', side='left')
    #
    # inp = tk.Entry(m)
    # inp.bind('<Return>', show)  # binding the Return event with an handler
    # inp.pack(fill='x', side='left')
    #
    # ok = tk.Button(m, text='GO', command=show)
    # ok.pack(fill='x', side='left')

    # m.mainloop()

    root = tk.Tk()
    app = App(root)
    root.mainloop()