import difflib
import tkinter as tk
import tkinter.font as tkFont
import time
# import numpy as np
# from tkinter import *
from PIL import ImageTk
from predict_best_comp import Predict
from static_data import Static
from screen import Screen
from Control import Control
from Items import Items
from Champions_pic import Champions_pic
from path_manager import Path

class App:
    def __init__(self, root):
        print("load 1/3")
        self.s = Static()
        self.s.adjust_comps()
        self.p = Predict(self.s)
        print("load 2/3")
        self.c = Control()
        self.screen = Screen(self.c)
        print("load 3/3")

        self.id_to_champ = self.s.id_to_champ
        self.id_to_item = self.s.id_to_item
        self.name_to_pic = {}

        p = Path()
        self.read_champions_pic(p)
        self.read_items(p)

        self.root = root

        # selectors
        frame = tk.Frame(self.root)
        frame.grid(column=0, row=0)
        # champions
        self.selected_champ = "aatrox"
        self.configure_champion_selector(frame)
        # # items
        self.selected_item = "bfsword"
        self.configure_item_selector(frame)

        # all champions "stats"
        self.frame_list_champions = []
        self.frame_list_items = []
        self.frame_dict_champions = {}
        self.frame_dict_items = {}
        test = ["snow3", "mistyrose3"]
        self.champion_dict = {}
        self.item_dict = {}
        self.font = tkFont.Font(family="Lucida Grande", size=7)
        for i in range(1, 9):

            frame = tk.Frame(self.root)
            frame.grid(column=0, row=i)
            if i == 1:
                text = "me"
            else:
                text = i - 1
            label = tk.Label(frame, bg=test[(i + 1) % 2], text=text, width=2, padx=7, pady=12, bd=2, font=self.font)
            label.grid(column=0, row=0)

            frame1 = tk.Frame(frame, bg=test[i % 2], width=390, height=40)
            frame1.grid(column=1, row=0)
            frame1.grid_propagate(False)
            frame1.bind("<Button-3>", self.click_on_champion_frame)
            self.frame_list_champions.append(frame1)
            self.champion_dict[i - 1] = {}
            self.frame_dict_champions[i - 1] = {}

            frame2 = tk.Frame(frame, bg=test[(i + 1) % 2], width=300, height=40)
            frame2.grid(column=2, row=0)
            frame2.grid_propagate(False)
            frame2.bind("<Button-3>", self.click_on_item_frame)
            self.frame_list_items.append(frame2)
            self.item_dict[i - 1] = {}
            self.frame_dict_items[i - 1] = {}

        # buttons
        # frame3l = tk.Frame(self.root, width=40, height=52)
        # frame3l.grid(column=0, row=10)
        frame3 = tk.Frame(self.root, width=720, height=53, bg="pink")
        frame3.grid(column=0, row=10)
        frame3.grid_propagate(False)

        button1 = tk.Button(frame3, width=30, text="Get Champs", command=self.press_button)
        button1.grid(column=0, row=0)
        # button1.grid_propagate(False)
        button2 = tk.Button(frame3, width=30, text="Calculate", command=self.press_button2)
        button2.grid(column=0, row=1)
        # button2.grid_propagate(False)

        self.inc_store = tk.IntVar()
        button3 = tk.Checkbutton(frame3, text="Inc store", variable=self.inc_store)
        button3.grid(column=1, row=0)
        self.only_me = tk.IntVar()
        button4 = tk.Checkbutton(frame3, text="Only me", variable=self.only_me)
        button4.grid(column=2, row=0)

        self.my_level = 1
        self.my_level_text = tk.StringVar()
        self.my_level_text.set("Level: 1")

        self.level_button = tk.Button(frame3, width=9, textvariable=self.my_level_text, relief=tk.RAISED)
        self.level_button.bind("<Button-1>", self.left_click_level)
        self.level_button.bind("<Button-3>", self.right_click_level)
        self.level_button.grid(column=1, row=1)

        # frame4 = tk.Frame(self.root, width=40, height=240)
        # frame4.grid(column=0, row=11)
        frame4 = tk.Frame(self.root, width=720, height=240)
        frame4.grid(column=0, row=11)
        frame4.grid_propagate(False)
        self.configure_screen(frame4)

    def right_click_level(self, event=None):
        if self.my_level != 9:
            event.widget.configure(relief=tk.SUNKEN)
            self.my_level += 1
            self.my_level_text.set(f"Level: {self.my_level}")
        self.level_button.after(100, lambda: self.level_button.config(relief=tk.SUNKEN))
        self.level_button.after(150, lambda: self.level_button.config(relief=tk.RAISED))

    def left_click_level(self, event=None):
        if self.my_level != 1:
            event.widget.configure(relief=tk.SUNKEN)
            self.my_level -= 1
            self.my_level_text.set(f"Level: {self.my_level}")
        self.level_button.after(100, lambda: self.level_button.config(relief=tk.SUNKEN))
        self.level_button.after(150, lambda: self.level_button.config(relief=tk.RAISED))

    def read_champions_pic(self, p):
        c = Champions_pic(p.path_champions_pic)
        for i in c.get_champion_list():
            self.name_to_pic[i[0]] = i[1]

    def read_items(self, p):
        i = Items(p.path_items_pic)
        for j in i.get_item_list():
            name = j[0]
            # print(name)
            if "s" in name:
                name = name[:-1]
                self.name_to_pic[self.s.id_to_item[int(name)]] = j[1]
            else:
                self.name_to_pic[int(name)] = j[1]

    def press_button(self):

        delay = 1  # seconds

        time.sleep(delay)
        # me, champ_dict, item_list = self.screen.main(store=self.inc_store.get())
        full_dict = self.screen.main(store=self.inc_store.get(), only_me=self.only_me.get(), show=False)
        for i in full_dict:
            if i == "me":
                champ_dict = full_dict["me"][0]
                item_list = full_dict["me"][1]
                number = 0
            else:
                champ_dict = full_dict[i][0]
                item_list = full_dict[i][1]
                number = i
            some = self.selected_champ
            for chap in champ_dict:
                amount = champ_dict[chap]
                self.selected_champ = chap
                self.add_champ_frame(number, def_value=amount)
            self.selected_champ = some

            item_dict = {i: item_list.count(i) for i in item_list}
            # print(item_dict)
            some = self.selected_item
            for item in item_dict:
                amount = item_dict[item]
                self.selected_item = self.s.id_to_item[item]
                self.add_item_frame(number, def_value=amount)
            # print(self.s.id_to_item, some)
            self.selected_item = some

    def press_button2(self):
        my_row = 0
        my_champs = {}
        all_champs = {}
        my_items = []
        for row in self.champion_dict:
            if row == my_row:
                # champs
                for i in self.champion_dict[row]:
                    nr = self.champion_dict[row][i]
                    if i in self.s.champ_to_id:
                        id = self.s.champ_to_id[i]
                        my_champs[id] = nr
                # items
                for i in self.item_dict[row]:
                    nr = self.item_dict[row][i]
                    for _ in range(nr):
                        my_items.append(i)
            for i in self.champion_dict[row]:
                nr = self.champion_dict[row][i]
                id = self.s.champ_to_id[i]
                if id in all_champs:
                    all_champs[id] += nr
                else:
                    all_champs[id] = nr
        top3 = self.p.predict_main(my_champs, all_champs, my_items, self.my_level, many=3)
        for i in range(3):
            frames = self.frame_list_screen[i]
            key = top3[i][1]
            self.add_comp_to_screen(key, frames, my_champs, my_items)
            # break
        # for i in self.p.s.comps:
        #     print(i, self.p.s.comps[i]["name"])
        self.p.same_length(top3)

    def click_on_champion_frame(self, event):
        nr = self.frame_list_champions.index(event.widget)
        self.add_champ_frame(nr)

    def click_on_item_frame(self, event):
        nr = self.frame_list_items.index(event.widget)
        self.add_item_frame(nr)

    def add_champ_frame(self, nr, def_value=1):
        champ_dict = self.champion_dict[nr]
        if self.selected_champ == "none":
            return
        elif self.selected_champ in champ_dict:
            return

        champ_dict[self.selected_champ] = def_value
        frame = self.frame_list_champions[nr]

        parent = tk.Frame(frame, width=30, height=40, bg="blue")
        parent.grid(column=len(champ_dict), row=0)
        parent.pack_propagate(False)

        # frame2 = tk.Frame(parent, bg="orange", width=30, height=30)
        # frame2 = tk.Label(parent, bg="orange", text=self.selected_champ, padx=12, pady=9, bd=0, font=self.font, width=1)
        if self.selected_champ in self.name_to_pic:
            frame2 = tk.Canvas(parent, width=30, height=30, highlightthickness=0)
            frame2.grid(column=0, row=0)
            frame2.grid_propagate(False)
            img = ImageTk.PhotoImage(image=self.name_to_pic[self.selected_champ])
            parent.img = img
            frame2.create_image(0, 0, anchor=tk.NW, image=img)
        else:
            frame2 = tk.Label(parent, bg="orange", text=self.selected_champ, padx=12, pady=9, bd=0, font=self.font, width=1)
            frame2.grid(column=0, row=0)
            frame2.grid_propagate(False)
        # frame2 = tk.Frame(parent, bg="orange", width=30, height=30)
        # frame2.grid(column=0, row=0)
        frame2.bind("<Button-1>", self.left_click_champ)
        frame2.bind("<Button-3>", self.right_click_champ)
        #
        label = tk.Label(parent, text=def_value, padx=12, pady=0, bd=0, font=self.font, width=1)
        label.grid(column=0, row=1)
        label.bind("<Button-1>", self.left_click_champ)
        label.bind("<Button-3>", self.right_click_champ)
        label.grid_propagate(False)

        self.frame_dict_champions[nr][parent] = self.selected_champ

    def add_item_frame(self, nr, def_value=1):
        item_dict = self.item_dict[nr]
        item_id = self.s.item_to_id[self.selected_item]
        if self.selected_item == "none":
            return
        elif item_id in item_dict:
            return

        item_dict[item_id] = def_value
        frame = self.frame_list_items[nr]

        parent = tk.Frame(frame, width=30, height=40, bg="yellow")
        parent.grid(column=len(item_dict), row=0)
        parent.pack_propagate(False)

        # frame2 = tk.Label(parent, bg="orange", text=self.selected_item, padx=12, pady=9, bd=0, font=self.font, width=1)
        # frame2.grid(column=0, row=0, sticky="W")

        frame2 = tk.Canvas(parent, width=30, height=30, highlightthickness=0)
        frame2.grid(column=0, row=0)
        frame2.grid_propagate(False)
        img = ImageTk.PhotoImage(image=self.name_to_pic[item_id])
        parent.img = img
        frame2.create_image(0, 0, anchor=tk.NW, image=img)
        # frame2 = tk.Frame(parent, bg="orange", width=30, height=30)
        # frame2.grid(column=0, row=0)
        frame2.bind("<Button-1>", self.left_click_champ)
        frame2.bind("<Button-3>", self.right_click_champ)

        frame2.bind("<Button-1>", self.left_click_item)
        frame2.bind("<Button-3>", self.right_click_item)
        #
        label = tk.Label(parent, text=def_value, padx=12, pady=0, bd=0, font=self.font, width=1)
        label.grid(column=0, row=1)
        label.bind("<Button-1>", self.left_click_item)
        label.bind("<Button-3>", self.right_click_item)
        label.grid_propagate(False)

        self.frame_dict_items[nr][parent] = item_id

        # name = parent._w
        # self.frame_dict[name] = {"count": 1, "obj": parent, "champ": self.selected_champ}


    def configure_champion_selector(self, frame):
        canvas = tk.Frame(frame, bg="red", width=420, height=25)
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

    def left_click_champ(self, event: tk.Event):
        nr = self.frame_list_champions.index(event.widget.master.master)
        parent = event.widget.master
        champ = self.frame_dict_champions[nr][parent]
        value = self.champion_dict[nr][champ] - 1
        if value == 0:
            del self.champion_dict[nr][champ]
            del self.frame_dict_champions[nr][parent]
            parent.grid_forget()
            parent.destroy()
            n = 0
            for frame in self.frame_dict_champions[nr]:
                frame.grid(column=n, row=0)
                n += 1
                # print(frame.gr)
        else:
            if "!canvas" in parent.children:
                parent.children["!label"]["text"] = value
            else:
                parent.children["!label2"]["text"] = value
            self.champion_dict[nr][champ] = value

    def right_click_champ(self, event):
        nr = self.frame_list_champions.index(event.widget.master.master)
        parent = event.widget.master
        champ = self.frame_dict_champions[nr][parent]
        value = self.champion_dict[nr][champ] + 1
        if value == 10:
            pass
        else:
            if "!canvas" in parent.children:
                parent.children["!label"]["text"] = value
            else:
                parent.children["!label2"]["text"] = value
            self.champion_dict[nr][champ] = value

    def left_click_item(self, event: tk.Event):

        nr = self.frame_list_items.index(event.widget.master.master)
        parent = event.widget.master
        item = self.frame_dict_items[nr][parent]
        value = self.item_dict[nr][item] - 1
        if value == 0:
            del self.item_dict[nr][item]
            del self.frame_dict_items[nr][parent]
            parent.grid_forget()
            parent.destroy()
            n = 0
            for frame in self.frame_dict_items[nr]:
                frame.grid(column=n, row=0)
                n += 1
        else:
            parent.children["!label"]["text"] = value
            self.item_dict[nr][item] = value

    def right_click_item(self, event):
        nr = self.frame_list_items.index(event.widget.master.master)
        parent = event.widget.master
        item = self.frame_dict_items[nr][parent]
        value = self.item_dict[nr][item] + 1
        if value == 10:
            pass
        else:
            parent.children["!label"]["text"] = value
            self.item_dict[nr][item] = value

    def configure_screen(self, frame):
        # self.frame_dict_screen = {}
        self.frame_list_screen = []
        test = ["red", "blue"]
        test2 = ["grey", "lightgrey"]
        for i in range(3):
            frame1 = tk.Frame(frame, bg=test[i % 2], width=720, height=80)
            frame1.grid(column=0, row=i)
            frame1.grid_propagate(False)
            # champions
            frame2 = tk.Frame(frame1, bg=test2[i % 2], width=300, height=80)
            frame2.grid(column=0, row=0)
            frame2.grid_propagate(False)
            # core items
            frame3 = tk.Frame(frame1, bg=test2[(i + 1) % 2], width=120, height=80)
            frame3.grid(column=1, row=0)
            frame3.grid_propagate(False)
            # extra items
            frame4 = tk.Frame(frame1, bg=test2[i % 2], width=300, height=80)
            frame4.grid(column=2, row=0)
            frame4.grid_propagate(False)
            self.frame_list_screen.append((frame2, frame3, frame4))


    def add_champ_card(self, lista, champs, frame, row):
        no = ["orange red", "orange"]
        yes = ["green", "lime"]

        for i in range(len(lista)):
            champ = lista[i]
            name = self.s.id_to_champ[champ]
            if champ in champs:
                parent = tk.Frame(frame, width=30, height=40, bg=yes[i % 2])
            else:
                parent = tk.Frame(frame, width=30, height=40, bg=no[i % 2])
            parent.grid(column=i, row=row)
            parent.pack_propagate(False)
            if name in self.name_to_pic:
                frame2 = tk.Canvas(parent, width=30, height=30, highlightthickness=0)
                frame2.pack()
                frame2.pack_propagate(False)
                img = ImageTk.PhotoImage(image=self.name_to_pic[name])
                parent.img = img
                frame2.create_image(0, 0, anchor=tk.NW, image=img)
            else:
                frame2 = tk.Label(parent, bg="azure", text=name, padx=12, pady=9, bd=0, font=self.font, width=1)
                frame2.pack()
                frame2.pack_propagate(False)
            # frame2.pack()
            # frame2.pack_propagate(False)

    def add_item_card(self, needed_items, needed_parts, items_copy, frame, item_to_champ_copy):
        no = ["orange red", "orange"]
        yes = ["green", "lime"]
        for i in range(len(needed_items)):
            item = needed_items[i]
            part1 = needed_parts[i * 2]
            part2 = needed_parts[i * 2 + 1]

            # name = self.s.id_to_item[item]
            name1 = self.s.id_to_item[part1]
            name2 = self.s.id_to_item[part2]
            add = False
            if item in items_copy:
                items_copy.remove(item)
                parent = tk.Frame(frame, bg=yes[i % 2], width=40, height=80)
                add = True
            else:
                parent = tk.Frame(frame, bg=no[i % 2], width=40, height=80)

            # huge card
            parent.grid(column=i, row=0)
            parent.pack_propagate(False)

            # label card
            champ = None
            for item_champ in item_to_champ_copy:
                if item_champ[0] == item:
                    champ = self.s.id_to_champ[item_champ[1]]
                    item_to_champ_copy.remove(item_champ)
                    break
            # frame7 = tk.Frame(parent, bg="cyan", width=40, height=20)
            frame7 = tk.Label(parent, text=champ, bg="azure", padx=17, pady=4, bd=0, font=self.font, width=1)
            frame7.pack(side="top")

            # # top card
            # # frame1 = tk.Frame(parent, bg="azure", width=30, height=30)
            # frame1 = tk.Label(parent, bg="azure", text=name, padx=12, pady=9, bd=0, font=self.font, width=1)
            # frame1.pack(side="top")
            frame2 = tk.Canvas(parent, width=30, height=30, highlightthickness=0)
            frame2.pack(side="top")
            frame2.pack_propagate(False)
            # print(self.name_to_pic)
            img = ImageTk.PhotoImage(image=self.name_to_pic[item])
            parent.img = img
            frame2.create_image(0, 0, anchor=tk.NW, image=img)

            # bottom card
            frame2 = tk.Frame(parent, bg="cyan", width=40, height=25)
            frame2.pack(side="bottom")

            if part1 in items_copy or add:
                if not add:
                    items_copy.remove(part1)
                frame3 = tk.Frame(frame2, bg=yes[0], width=20, height=25)
            else:
                frame3 = tk.Frame(frame2, bg=no[0], width=20, height=25)
            # # frame3 = tk.Label(parent, bg="yellow", text=name1, padx=1, pady=2, bd=0, font=self.font, width=3)
            frame3.pack(side="left")
            frame3.pack_propagate(False)

            if part2 in items_copy or add:
                if not add:
                    items_copy.remove(part2)
                frame4 = tk.Frame(frame2, bg=yes[1], width=20, height=25)
            else:
                frame4 = tk.Frame(frame2, bg=no[1], width=20, height=25)
            # frame4 = tk.Label(parent, bg="orange", text=name2, padx=1, pady=2, bd=0, font=self.font, width=3)
            frame4.pack(side="right")
            frame4.pack_propagate(False)

            # frame5 = tk.Frame(frame3, bg="azure", width=20, height=20)
            # frame5 = tk.Label(frame3, bg="azure", text=name1, padx=20, pady=4, bd=0, font=self.font, width=0)
            # frame5.pack(side="top")
            frame5 = tk.Canvas(frame3, width=20, height=20, highlightthickness=0)
            frame5.pack(side="top")
            # frame5.pack_propagate(False)
            img = ImageTk.PhotoImage(image=self.name_to_pic[name1])
            frame3.img = img
            frame5.create_image(0, 0, anchor=tk.NW, image=img)

            # frame6 = tk.Frame(frame4, bg="azure", width=20, height=20)
            # frame6 = tk.Label(frame4, bg="azure", text=name2, padx=20, pady=4, bd=0, font=self.font, width=0)
            # frame6.pack(side="top")
            frame6 = tk.Canvas(frame4, width=20, height=20, highlightthickness=0)
            frame6.pack(side="top")
            # frame5.pack_propagate(False)
            img = ImageTk.PhotoImage(image=self.name_to_pic[name2])
            frame4.img = img
            frame6.create_image(0, 0, anchor=tk.NW, image=img)

    def add_comp_to_screen(self, comp_key, frames, champs, items):
        comp = self.s.comps[comp_key]
        needed_champs = comp["needed_champs"]
        extra_champs = comp["extra_champs"]
        early_champs = comp["early_champs"]
        needed_items = comp["needed_items"]
        needed_parts = comp["needed_parts"]
        extra_items = comp["extra_items"]
        extra_parts = comp["extra_parts"]
        item_to_champ = comp["item_to_champ"]
        # print(needed_items)
        # print(needed_parts)
        # print(extra_items)
        # print(extra_parts)
        # print(items)
        # print(comp["name"])

        # prevent overlapping
        for frame in frames:
            for child in frame.winfo_children():
                child.destroy()

        # make lists
        lista = needed_champs.copy()
        lista.sort(key=lambda x: self.s.champ_id_to_tier[x])
        listb = early_champs.copy()
        listb.extend(extra_champs)
        listb.sort(key=lambda x: self.s.champ_id_to_tier[x])

        # core champs
        self.add_champ_card(lista, champs, frames[0], 0)
        # extra champs
        self.add_champ_card(listb, champs, frames[0], 1)
        # items
        items_copy = items.copy()
        item_to_champ_copy = item_to_champ.copy()
        self.add_item_card(needed_items, needed_parts, items_copy, frames[1], item_to_champ_copy)
        self.add_item_card(extra_items, extra_parts, items_copy, frames[2], item_to_champ_copy)

        # for i in range(len(extra_items)):
        #     item = extra_items[i]
        #     part1 = extra_parts[i * 2]
        #     part2 = extra_parts[i * 2 + 1]
        #     print(item)
        #     print(part1, part2)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()