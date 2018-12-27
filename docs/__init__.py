import tkinter as tk




class PopupDoc(tk.Toplevel):
    def __init__(self, master, type):
        super().__init__(master)
        self.geometry('{}x{}'.format(800, 800))
        self.wm_title(type)
        self.lift(master)

        self.master = master
        self.type = type

        geomap = {'HK Sheet': "400x400", "Game Functions": "800x600", "Joy Functions": "800x600", "Settings": "800x600", "File Pointer": "400x200"}

        self.geometry(geomap[type])



    def view_hotkeys(self, hotkeys, info):


        forbidden = ["None", None, ""]


        settings = {}
        tolookfor = ["play hotkey", "switch sides hotkey", "next tuner hotkey", "previous tuner hotkey", "increase tuner hotkey", "decrease tuner hotkey"]
        for k,v in hotkeys["Settings"].items():
            if k in tolookfor:
                settings[k] = v

        joyfunc = {}
        for k,v in hotkeys["Joy Functions"].items():
            if v["Hotkey"] not in forbidden and v["Hotkey"] not in forbidden and v["String"] not in forbidden:
                joyfunc[k] = v["Hotkey"]

        gamefunc = {}
        for k,v in hotkeys["Game Functions"].items():
            if v["Hotkey"] not in forbidden and v["Hotkey"] not in forbidden and v["String"] not in forbidden:
                gamefunc[k] = v["Hotkey"]


        gametitle = info['gametitle']
        joytype = info['joytype']

        # textbox for main keys
        mainhkbox = tk.Text(self, width=8, height=5, state='normal')
        mainhkbox.pack(anchor='nw', side='top', padx=5, pady=5, fill='x')
        mainhkbox.insert("1.0", str(settings))
        mainhkbox.config(state='disabled')

        joyhkbox = tk.Text(self, width=8, height=5, state='normal')
        joyhkbox.pack(anchor='ne', side='top', padx=5, pady=5, fill='x')
        joyhkbox.insert("1.0", str(joyfunc))
        joyhkbox.config(state='disabled')

        gamehkbox = tk.Text(self, width=16, height=5, state='normal')
        gamehkbox.pack(anchor='s', side='top', padx=5, pady=5, fill='x')
        gamehkbox.insert("1.0", str(gamefunc))
        gamehkbox.config(state='disabled')

        tk.Button(self, text="Cancel", command=lambda: self.destroy()).pack(side='bottom', anchor='s', pady=5)

    def edit_dict(self, d):
        # d is self.settings
        self.mainbox = tk.Text(self)
        self.mainbox.pack(fill='both', expand=1, side="top")
        self.mainbox.insert("1.0", str(d))

        cancelbtn = tk.Button(self, text="Cancel", command=lambda: self.destroy())
        cancelbtn.pack(side='bottom', anchor='sw', pady=5)

        commitbtn = tk.Button(self, text="Commit", command=lambda: self.commit())
        commitbtn.pack(side='bottom', anchor='sw', pady=5)


    def commit(self):
        newdtext = self.mainbox.get("1.0", "end")
        #try evaluating dictionary, if error, let user know and keep window up. If they can't figure out syntax, they don't need to be changing the settings until they are simplified
        # or they learn the syntax
        #try:
        e_newd = eval(newdtext)
        self.master.point_to_files(e_newd)
        self.destroy()
        #except Exception as e:
        #    tk.messagebox.showerror(title="Error", message="{}".format(e))
        #    return
