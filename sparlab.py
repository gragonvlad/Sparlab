import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk
import time
from custom import CustomNotebook
import updater
import _input
from multiprocessing import Queue, freeze_support
import webbrowser
from docs import PopupDoc


SAVE_FILE_NAME = 'config.txt'
DATAPATH = '%s\\Sparlab' %  os.environ['APPDATA']
DPFILES = DATAPATH + "\\" + "files.txt"

# default text files if file pointer not functional
FILES = os.path.join(r".\config", "files.txt")
DEFAULT = os.path.join(r".\config", "defaults.txt")

__version__ = '1.0.2'



#ff4242
TITLE_FONT = ("Verdana", 24)
LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)
HELP_FONT = ("Verdana", 7)
ICON = os.path.join(r'.\\plugins\\images', "sparlab_logo.ico")


# FR_IMG = os.path.join(f'.\\plugins\\images', 'fr.jpg')
# FL_IMG = os.path.join(f'.\\plugins\\images', 'fl.jpg')

class App(tk.Tk):

    def point_to_files(self, edic):
        """
        Re-points to files user wants to use, on user's commit in File Pointer config panel
        edic is an evaluated dictionary from the panel's textbox
        """
        self.files = DATAPATH + "\\" + "files.txt"
        with open(self.files, "w") as f:
            f.write(str(edic))


        self.gamefile = DATAPATH + "\\" + edic["game file"]
        self.joyfile = DATAPATH + "\\" + edic["joy file"]
        self.settingsfile = DATAPATH + "\\" + edic["settings file"]

        # game functions
        filename = "game.txt"
        path = DATAPATH
        cfg = os.path.join(path, filename)
        print("path: {}, filename: {}".format(path, filename))
        with open(cfg, 'r') as f:
            self.cfg = eval(f.read())
            f.close()

        # joy functions
        filename = "joy.txt"
        path = DATAPATH
        joycfg = os.path.join(path, filename)
        with open(joycfg, "r") as f:
            # string to python dict
            self.joy_cfg = eval(f.read())
            f.close()

        # settings
        filename = "settings.txt"
        path = DATAPATH
        settings = os.path.join(path, filename)
        with open(settings, "r") as f:
            # string to python dict
            self.settings = eval(f.read())
            f.close()

        # set stringvars
        self.joytype = self.settings['joy type']
        self.fps = int(self.settings['fps'])
        self.action_interval_t = float(self.settings['ADI'])
        self.port = int(self.settings["joy port"])
        self.default_dir = self.settings['default direction']


    def __init__(self, q1, q2):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Sparlab")
        tk.Tk.iconbitmap(self, default=ICON)

        self.geometry('{}x{}'.format(500, 200))
        self.configure(background="#ffffff")

        self.q1 = q1
        self.q2 = q2


        # load defaults

        # Defaults will exist whether new or used
        with open(DEFAULT, 'r') as f:
            content = eval(f.read())
            SETTINGS = content["Settings"]
            JOY = content["Joy Functions"]
            GAME = content["Game Functions"]
            f.close()

        # if this folder doesn't exist, create it along with storing copies of default settings & functions
        if not os.path.exists(DATAPATH):
            with open(FILES, 'r') as f:
                files = eval(f.read())
                f.close()
            os.makedirs(DATAPATH)
            self.files = files
            for iter, p in enumerate([[self.files['game file'], "gamefile", GAME], [self.files['joy file'], "joyfile", JOY], [self.files['settings file'], "settingsfile", SETTINGS]]):
                path, filename = os.path.split(p[0])
                print("path: {}; filename: {}".format(path, filename))
                fp = r"{}\{}".format(DATAPATH, path)
                print("fp: ", fp)
                entire = fp + "\\" + filename

                # if the path to the text file does not exist, only check on first iteration
                if not os.path.exists(fp) and iter == 0:
                    # make the directory
                    os.makedirs(fp)

                with open(os.path.join(fp, filename), "w") as f:
                    f.write(str(p[2]))
                    f.close()

                setattr(self, p[1], entire)

                # create files.txt in folder. This is what will be overwritten by user
            with open(DPFILES, "w") as f:
                f.write(str(self.files))




        # folder exists, so check for the data path files.txt, it should be there if user hasn't deleted it.
        else:
            try:
                with open(DPFILES, "r") as f:
                    self.files = eval(f.read())
                    self.gamefile = self.files["game file"]
                    self.joyfile = self.files["joy file"]
                    self.settingsfile = self.files["settings file"]
            except Exception as e:
                print(e)
                with open(DPFILES, "w") as f:
                    f.write(str(self.files))
                    f.close()
                with open(DPFILES, "r") as f:
                    content = f.read()
                    self.files = eval(f.read())
                    self.gamefile = self.files["game file"]
                    self.joyfile = self.files["joy file"]
                    self.settingsfile = self.files["settings file"]



        # game functions

        path = DATAPATH
        filename = "game.txt"
        cfg = os.path.join(path, filename)
        print("path: {}, filename: {}".format(path, filename))
        with open(cfg, 'r') as f:
            self.cfg = eval(f.read())
            f.close()

        # joy functions

        path = DATAPATH
        filename = "joy.txt"
        joycfg = os.path.join(path, filename)
        with open(joycfg, "r") as f:
            # string to python dict
            self.joy_cfg = eval(f.read())
            f.close()

        # settings
        filename = "settings.txt"
        path = DATAPATH
        settings = os.path.join(path, filename)
        with open(settings, "r") as f:
            # string to python dict
            self.settings = eval(f.read())
            f.close()


        self.playing = False
        self.hks_on = False
        self.frames = []

        # set stringvars
        self.joytype = self.settings['joy type']
        self.fps = int(self.settings['fps'])
        self.action_interval_t = float(self.settings['ADI'])
        self.port = int(self.settings["joy port"])
        self.default_dir = self.settings['default direction']
        self.dir = self.settings['default direction']
        try:
            self.gametitle = self.settings['game title']
        except:
            self.gametitle = "Game"
        self.joy_is_on = False

        try:
            self.delay_tuners = {i:tk.StringVar(value=0.0) for i in eval(self.settings['Delay Tuners'])}
        except:
            self.delay_tuners = {i:tk.StringVar(value=0.0) for i in self.settings['Delay Tuners']}

        self.togglelabs = []
        # current tuner index (increases by 1 when 'next tuner' is called and decreases when 'previous tuner' is called )
        self.cti = 0
        # mapping of panel types ("Settings", "Game Functions", etc.) to toplevel frames. None if none opened
        # if user tries opening a panel and the type has one mapped, it will refocus the opened frame

        self.add_tab()
        self.create_top_menu()
        # periodically check for updates in queue
        self.processIncoming()
        self.check_for_update(booting=True)


    def processIncoming(self):
        while self.q2.qsize():
            try:
                info = self.q2.get(0)
                #print("info from session: ", info)
                if info != None:
                    try:
                        cmd = info['command']
                        if cmd == 'next tuner':
                            #print("q2 next tuner")
                            self.next_tuner()
                        elif cmd == 'previous tuner':
                            #print("q2 previous tuner")
                            self.previous_tuner()
                        elif cmd == 'increase tuner':
                            #print("q2 increase tuner")
                            self.increase_tuner()
                        elif cmd == 'decrease tuner':
                            #print("q2 decrease tuner")
                            self.decrease_tuner()
                    except Exception as e:
                        # print(e)
                        pass

                        #print(msg)

                    try:
                        facing = info['facing']
                        if self.dir != facing:
                            self.toggle_direction()
                    except:
                        pass

                    try:
                        vbusnotexist = info['vbusnotexist']
                        messagebox.showerror(title="Error", message="No virtual bus driver was found on your system.")
                    except:
                        pass
                    try:
                        playing = info['playing']
                        if playing == False:
                            #print("q2 pause")
                            self.pause()
                        elif playing == True:
                            #print("q2 play")
                            self.play()
                    except Exception as e:
                        msg = "{}: {}".format(type(e).__name__, e.args)
                        #print(msg)

                    try:
                        hk_act = info['hk action']
                        #print("hotkey: ", hk_act)
                    except Exception as e:
                        pass

            except Exception as e:
                msg = "{}: {}".format(type(e).__name__, e.args)
                #print("Q2 EXCEPTION: ", msg)

        self.after(200, self.processIncoming)

    def retrieve_data(self):
        """Load config data from data folder"""
        # settings variables. Attempt to load from path, if that fails, value them '--'
        try:
            # load sequences dict from path
            with open(DATAPATH + f"\\{self.save_file_name}", "r") as f:
                loaded = f.read()
                SparLab_data = eval(loaded)

        except Exception as e:
            #print("522: ", e)
            SparLab_data = self.get_default_data()

        return SparLab_data



    def add_tab(self, name = None):
        """ Each Sparsheet is a tab with a built-in text editor and assigned hotkey"""

        self.note = CustomNotebook(self)

        # app always opens on this sheet
        self.new_file(name=name)
        self.note.pack(fill='both', expand=1)


    def get_img_name(self, target):
        """return img name"""
        try:
            img = self.cfg['xbox bindings'][target]['icon']
        except:
            img = None
        return img


    def create_top_menu(self):
        """ Menu at top of app """

        # temporarily disabled: edit, redo, cut, paste functionality (basically whole edit menu)
        #'Edit': (editmenu, [('Undo', None, self.get_hk('undo')), ('Redo', None, self.get_hk('redo')),('Cut', self.cut_text, self.get_hk('cut')), ('Copy', self.copy_text, self.get_hk('copy')),
         #('Paste', self.paste_text, self.get_hk('paste'))]),

        self.menu = tk.Menu(self, tearoff=False)
        self.config(menu=self.menu)
        filemenu = tk.Menu(self, tearoff=False)
        editmenu = tk.Menu(self, tearoff=False)
        helpmenu = tk.Menu(self, tearoff=False)

        self.submenus = {'File': (filemenu, [('New', self.new_file,None ), ('Open', self.open_file, None),
                        ('Play', self.play, None), ('Toggle Joy State', self.toggle_controller, None), ('Flip X Axis ', self.toggle_direction, None),
                        ('Save', self.save_as, None),
                        ('Exit', self.destroy, None)]), 'Edit': (editmenu, [('Edit', self.panel, "File Pointer")]),

                        'Help': (helpmenu, [('Documentation', self.view_documentation, None),
                         ('FAQ', self.view_faq, None), ("HK Sheet", self.panel, "HK Sheet"),
                         ('Check for Update', self.check_for_update, None)])}

# menu commands disabled when Welcome tab is selected
# cboxcallback

        for k, v in self.submenus.items():
            self.menu.add_cascade(label=k, menu=v[0])
            if k in ['File', 'Help']:
                for i in v[1]:

                    # acc = i[2]
                    arg = i[2]

                    if i[0] in ['Play']:
                        stat = 'disabled'
                    else:
                        stat = 'normal'

                    command = lambda func=i[1], a=arg: self.menu_command(func, a)
                    v[0].add_command(label=i[0], command=command, state=stat)




    def menu_command(self, func, arg):
        if arg == None:
            func()
        else:
            func(arg)


    def pack_top_buttons(self, tab):
        """Buttons to be displayed above sparsheets"""

        #tab_id = self.note.tabs()
        actbtns = []
        imgs = []
        fixbtnframe = tk.Frame(tab)
        fixbtnframe.pack(side='bottom', anchor='s', fill='x')
        btnframe = tk.Frame(tab)
        btnframe.pack(side='top', anchor='n', fill='x')

        # self.img = Image.open(image[0])
        # w, h = self.img.size
        # btn_img = ImageTk.PhotoImage(self.img.resize(image[1]))
        # imgs.append(btn_img)

        # "Settings", "Joy Functions", "Game Functions",
        self.panelbtn = ttk.Combobox(btnframe, width=30, values=["Flip X Axis", "Toggle Joy State", "File Pointer", "HK Sheet", "Documentation", "FAQ"], state='readonly')

        self.panelbtn.bind("<<ComboboxSelected>>", lambda e: self.cboxcallback(e))
        self.panelbtn.pack(side='right', anchor='ne')

        self.initButton = btn = ttk.Button(fixbtnframe, text = "Play", width=8, command=lambda: self.play(), state='normal' if self.joy_is_on else 'disabled')
        self.initButton.pack(side='right', anchor='e')

        stat = "Joy State:  On" if self.joy_is_on else "Joy State: Off"
        self.joystatuslab = tk.Label(btnframe, text="{}".format(stat))
        # btn = ttk.Button(btnframe, text = "Toggle Joy State", command=lambda: self.toggle_controller(joystatuslab))
        # btn.pack(side='right', anchor="ne")
        self.joystatuslab.pack(side='left', anchor="ne")

        stat = 'X Axis: Flipped' if ((self.dir == 'L' and self.default_dir == 'R')  or (self.dir == 'R' and self.default_dir == 'L')) else 'X Axis:  Normal'
        self.dirstatuslab = tk.Label(btnframe, text=stat)
        # self.toggledirbtn = ttk.Button(btnframe, text="Flip X Axis ", command=lambda lab=self.dirstatuslab: self.toggle_direction())
        # self.toggledirbtn.pack(side='right', anchor="ne")
        self.dirstatuslab.pack(side='left', anchor="ne", padx=15)

        # adjusting fps on main screen


        self.fpsvar = tk.StringVar(value=str(self.fps))
        self.fpstuner = tk.Spinbox(fixbtnframe, to=1000, from_=0, textvariable=self.fpsvar, width=4, command=lambda: self.tune_var())
        l = tk.Label(fixbtnframe, text='fps', width=5, font='Verdana 10', bg='#ff4242')
        l.pack(side='left', anchor='nw')

        self.togglelabs.append(l)
        self.delay_tuners['fps'] = self.fpsvar
        self.fpstuner.pack(side='left', anchor='nw')
        # adjusting action interval time on main screen
        self.aivar = tk.StringVar(value=str(self.action_interval_t))
        self.aituner = tk.Spinbox(fixbtnframe, to=1000, from_=0, textvariable=self.aivar, increment=0.1, width=4, command=lambda: self.tune_var())
        l = tk.Label(fixbtnframe, text='ADI', width=4, font='Verdana 10')
        l.pack(side='left', anchor='nw', padx=5)

        self.delay_tuners['ADI'] = self.aivar
        self.togglelabs.append(l)
        self.aituner.pack(side='left', anchor='nw')
        # self.hk_sheet_btn = ttk.Button(btnframe, text="HK Sheet", command=lambda: self.hks_popup())
        # self.hk_sheet_btn.pack(side='right', anchor="ne")

        # get dict of all tuners

        #Delay Tuners: ['!', '@', '#', '$']

        # self.delay_tuners = {i:tk.StringVar(value=0.0) for i in self.settings['Delay Tuners'] }
        # append to togglelabs

        for notation, var in self.delay_tuners.items():
            if notation not in ['fps', 'ADI']:
                l = tk.Label(fixbtnframe, text=notation, width=2, font='Verdana 10')
                l.pack(side='left', anchor='n', padx=10)

                self.togglelabs.append(l)
                tk.Spinbox(fixbtnframe, to=100.0, from_=0.0, textvariable=var, increment=0.1, width=4, command=lambda: self.tune_var()).pack(side='left', anchor='n')



    def tune_var(self):
        dt = {k:float(v.get()) for k,v in self.delay_tuners.items()}
        self.q1.put({'delay tuners': dt})


    def previous_tuner(self):
        self.togglelabs[self.cti].config(bg=self.cget('bg'))
        self.cti = self.cti - 1 if self.cti > 0 else len(self.togglelabs) - 1
        self.togglelabs[self.cti].config(bg='#ff4242')

    def next_tuner(self):
        self.togglelabs[self.cti].config(bg=self.cget('bg'))
        self.cti = self.cti + 1 if self.cti < len(self.togglelabs) - 1 else 0
        self.togglelabs[self.cti].config(bg='#ff4242')

    def increase_tuner(self):
        tunerkey = self.togglelabs[self.cti].cget('text')
        #print"tunerkey: ", tunerkey)
        tunervar = self.delay_tuners[tunerkey]
        oldval = float(tunervar.get()) if tunerkey != 'fps' else int(tunervar.get())
        #print"oldval: ", oldval)
        newval = round(oldval + 0.1, 1) if tunerkey != 'fps' else oldval + 1
        # newval unrounded
        nv_ur = oldval + 0.1 if tunerkey != 'fps' else oldval + 1
        self.delay_tuners[tunerkey].set(str(newval))
        #print"newval: ", newval)
        dt = {k:float(v.get()) for k,v in self.delay_tuners.items()}
        self.q1.put({'delay tuners': dt})
        # if tunerkey == 'fps':
        #     self.settings['fps'] = nv_ur
        #     self.settings['j_f'] = nv_ur
        #     self.q1.put({'settings', self.settings})
        # elif tunerkey == 'ADI':
        #     print("new ADI equals: ", nv_ur)
        #     self.settings['ADI'] = nv_ur
        #     self.q1.put({'settings', self.settings})


    def decrease_tuner(self):
        tunerkey = self.togglelabs[self.cti].cget('text')
        #print"tunerkey: ", tunerkey)
        tunervar = self.delay_tuners[tunerkey]
        oldval = float(tunervar.get()) if tunerkey != 'fps' else int(tunervar.get())
        #print"oldval: ", oldval)
        newval = round(oldval - 0.1, 1) if tunerkey != 'fps' else oldval - 1
        # newval unrounded
        nv_ur = oldval - 0.1 if tunerkey != 'fps' else oldval - 1
        self.delay_tuners[tunerkey].set(str(newval))
        #print"newval: ", newval)
        dt = {k:float(v.get()) for k,v in self.delay_tuners.items()}
        self.q1.put({'delay tuners': dt})
        # if tunerkey == 'fps':
        #     self.settings['fps'] = nv_ur
        #     self.settings['j_f'] = nv_ur
        #     self.q1.put({'settings', self.settings})
        # elif tunerkey == 'ADI':
        #     self.settings['ADI'] = nv_ur
        #     self.q1.put({'settings', self.settings})


    def cboxcallback(self, event):
        selection = event.widget.get()
        if selection == "Toggle Joy State":
            self.toggle_controller()
        elif selection == "Flip X Axis":
            self.toggle_direction()

        elif selection == "Documentation":
            self.view_documentation()
        elif selection == "FAQ":
            self.view_faq()
        else:
            self.panel(selection)


    def dnd_end(self, target, event):
        pass


    def new_file(self, name=None, source=None, text=None):
        #print("new file")
        tab = tk.Frame(self.note)
        self.pack_top_buttons(tab)
        n = len(self.frames)

        name = f"sparsheet{n}" if name == None else name
        self.note.add(tab, text = name, compound='top')

        self.note.select(self.note.tabs()[-1])
        self.current_tab = tab

        txt = tk.Text(tab, background="#ffffff", height=10)
        txt.source = source

        self.current_tb = txt

        txt.pack(fill='both', expand=1, side='top', anchor='n')



        if text == None:
            txt.insert("1.0", "[]")
        else:
            #print"TEXT WHEN OPENED: ", text)
            txt.insert("1.0", text)


        self.helplab = tk.Label(tab)
        self.helplab.pack(side="bottom", anchor='sw')

        self.frames.append([name, txt, source])
        # add joy status & bot facing direction labels
        tab.textbox = txt

        return tab

    def decrease_ranks(self, event, tab):
        pass


    def get_cursor_pos(self, box):
        return box.index(tk.INSERT)


    def tipKeyDown(self, event):
        pos=event.widget.index('current')
        #printpos)
        pos=event.widget.index('insert')
        #printpos)


    def open_file(self):
        def readFile(filename):
            f = open(filename, "r")
            text = f.read()
            return text

        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        #path = filedialog.askdirectory()
        fl = dlg.show()

        if fl != '':
            docname = fl.split("/")[-1].split(".")[0]
            tab = self.new_file(name=docname, source=fl, text=readFile(fl))


    def toggle_controller(self):

        if self.joy_is_on == True:
            self.hks_on = False
            self.initButton.config(state='disabled')

            self.joy_is_on = False
            self.joystatuslab.config(text="Joy State: Off")

            info = {'playing': False, 'hks on': False}
            self.q1.put(info)

        else:
            self.joystatuslab.config(text="Joy State:  On")
            self.initButton.config(state='normal')
            # ensure listener process is MORE informed when controller is turned ON vs off
            info = {'playing': False, 'hks on': True, 'joy': self.port, 'settings': self.settings, 'cfg': self.cfg, 'facing': self.dir, 'joycfg': self.joy_cfg}
            self.q1.put(info)
            self.joy_is_on = True

    def toggle_direction(self):
        imgs = []
        if self.dir == 'R':
            self.dir = 'L'
        else:
            self.dir = 'R'

        info = {'facing': self.dir}
        self.q1.put(info)

        stat = 'X Axis: Flipped' if ((self.dir == 'L' and self.default_dir == 'R')  or (self.dir == 'R' and self.default_dir == 'L')) else 'X Axis:  Normal'

        #print"stat: {}; self.dir: {}; self.default_dir: {}".format(stat, self.dir, self.default_dir))

        self.dirstatuslab.config(text=stat)


    # def view_settings(self, type):
    #     #print("type: ", type)
    #     self.panel(type)


    def play(self):
        textbox = self.get_current_tabs_textbox()

        self.initButton.config(text = "Pause", command=lambda: self.pause())
        #self.initButton.image = btn_img

        #sorted_acts = sorted(canvas.find_all(), lambda x: x.)

        self.lasttxt = textbox.get("1.0", "end").splitlines()[0]

        if self.playing == False:
            self.playing = True

            #self.load_settings_functions()

            # split by space
            moveslist = self.lasttxt.split(" ")
            actlist = []

            leftbracketpassed = False
            rightbracketpassed = False

            #print"DELAY TUNERS: ", self.delay_tuners)

            for i in moveslist:
                # pre configs: predelays

                for ind, _d in enumerate(list(self.delay_tuners)):
                    #print"ind: {}; _d: {}".format(ind, _d))
                    if i == _d:
                        actlist.append((None, None, _d))


                for k,v in self.cfg.items():
                    if i == '[': leftbracketpassed = True
                    if '[' in list(i) and leftbracketpassed == False:
                        i = "".join(list(i)[1:])
                        #print"i when leftbracketpassed: ", i)
                        leftbracketpassed = True

                    if i == ']': rightbracketpassed = True
                    if ']' in list(i) and rightbracketpassed == False:
                        i = "".join(list(i)[0:-2])
                        #print"i when rightbracketpassed: ", i)
                        rightbracketpassed = True


                    if v["String"] != None and v["Notation"] == i and leftbracketpassed == True:
                        actlist.append((self.cfg[k]["Notation"], self.cfg[k]["Image"], self.cfg[k]["String"]))

                        if rightbracketpassed == True:
                            break


                if rightbracketpassed == True:
                    break

            dt = {k:float(v.get()) for k,v in self.delay_tuners.items()}
            #print'dt: ', dt)
            #print"ACTLIST: ", actlist)




            info = {'playing': True, 'hks on': True, 'settings': self.settings, 'actlist': actlist,'cfg': self.cfg, 'facing': self.dir, 'delay tuners': dt}

            self.q1.put(info)


        #self.overlay.pack(expand=True, fill='both')


    # callback for when button is released off of save/ cancel buttons

    def load_settings_functions(self):
        """Temp replacement for Settings, this function will be ran every time user
            presses play or presses 'load settings + functions'"""

        with open(SETTINGS, 'r') as f:
            settings = f.read()
            f.close()

        # string to python dict
        self.settings = eval(settings)

        path, filename = os.path.split(self.gamefile)
        listoffolders = path.split("\\")
        self.gametitle = listoffolders[-1]
        cfg = os.path.join(path, filename)
        with open(cfg, 'r') as f:
            self.cfg = eval(f.read())
            f.close()

        path, filename = os.path.split(self.joyfile)
        joycfg = os.path.join(path, filename)
        with open(joycfg, "r") as f:
            # string to python dict
            self.joy_cfg = eval(f.read())
            f.close()



    def panel(self, stype):
        pd_map = {
                    'HK Sheet': 'view_hotkeys',
                    'File Pointer': 'edit_dict',
                    }

        togmap = {'Flip X Axis': 'toggle_direction', 'Toggle Joy State': 'toggle_controller'}


        """Settings & function panels temporarily replaced with load_settings_functions until better solution found"""
        # stype can be 'game', 'joy' or 'Settings'
        # if stype in ['Game Functions', 'Settings', 'Joy Functions']:
        #     try:
        #         if self.open_panels[stype] == None:
        #             self.open_panels[stype] = SettingsWindow(self, stype)
        #             self.open_panels[stype].create_fill_canvas(self.cfg, stype)
        #             self.open_panels[stype].protocol("WM_DELETE_WINDOW", lambda s=stype: self.none_thyself(s, self.open_panels[s]))
        #         else:
        #             self.lift(self.open_panels[stype])
        #     except KeyError as e:
        #         self.open_panels[stype] = SettingsWindow(self, stype)
        #         self.open_panels[stype].create_fill_canvas(self.cfg, stype)
        #         self.open_panels[stype].protocol("WM_DELETE_WINDOW", lambda s=stype: self.none_thyself(s, self.open_panels[s]))


        info = {'joytype': self.joytype, 'gametitle': self.gametitle}
        dicts = {'Settings': self.settings, 'Joy Functions': self.joy_cfg, 'Game Functions': self.cfg, "File Pointer": self.files}

        if stype == 'HK Sheet':
            hksheet = PopupDoc(self, stype)
            getattr(hksheet, 'view_hotkeys')(dicts, info)
        else:
            popup = PopupDoc(self, stype)
            getattr(popup, pd_map[stype])(dicts[stype])




    def commit_changes(self, tp, settext):
        try:
            del self.open_panels[tp].map
            del self.open_panels[tp].orig
            self.open_panels[tp].grab_release()
            self.open_panels[tp].destroy()
            self.open_panels[tp].canvas.destroy()
            del self.open_panels[tp]
        except Exception as e:
            #print("COMMIT CHANGES EXCEPTION: ", e)
            pass
        if tp == 'Game Functions':
            self.cfg = settext
            info = {'cfg': self.cfg}

            with open(self.gamefile, "w") as f:
                f.write(str(self.cfg))
                f.close()

        elif tp == 'Joy Functions':
            self.joy_cfg = settext
            info = {'joycfg': self.joy_cfg}

            with open(self.joyfile, "w") as f:
                f.write(str(self.joy_cfg))
                f.close()

        elif tp == 'Settings':
            self.settings = settext
            info = {'settings': self.settings}

            with open('.\\config\\settings.txt', "w") as f:
                f.write(str(self.settings))
                f.close()

        self.q1.put(info)



    def view_documentation(self):
        webbrowser.open('https://www.umensch.com/forums/', new=2)

    def view_faq(self):
        webbrowser.open('https://www.umensch.com/forums/', new=2)




    def pause(self):
        if self.playing == True:
            self.initButton.config(text='Play', command=lambda: self.play())

            #print("testing pause script")
            self.playing = False

            info = {'playing': False}

            self.q1.put(info)


    def save_as(self):
        #print"save test")
        tab = self.get_current_tab()
        txtbox = self.get_current_tabs_textbox()
        txt = txtbox.get("1.0", tk.END).splitlines()
        txt = "\n".join(txt)
        #print"split line text: ", txt)
        #src = self.frames[tab][-1]
        name = self.frames[tab][0]
        # check if there is source for the text box, if yes, write to source else pull up Save As window
        ftypes = [('Text files', '*.txt'), ('All files', '*')]

        f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=ftypes, title=name if name != None else self.current_tab.text)

        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        try:
            with open(f, "w") as file:
                file.write(txt)
                file.close()
        except FileNotFoundError as e:
            pass


    # def copy_text(self):
    #     textbox = self.get_current_tabs_textbox()
    #     try:
    #         assert textbox != None
    #     except:
    #         return
    #
    #     textbox.clipboard_clear()
    #     # after returning selected, determine if its text or image, if image: get the image's function w/ self.config
    #     textbox.clipboard_append(textbox.selection_get())
    #     return textbox
    #
    # def cut_text(self):
    #     textbox = self.copy_text()
    #     text_box.delete("sel.first", "sel.last")
    #
    # def paste_text(self):
    #     textbox = self.get_current_tabs_textbox()
    #     textbox.insert(tk.INSERT, textbox.clipboard_get())

    def get_current_tabs_textbox(self):

        # get status of 'current' tab, kill it if dead.
        #current tab id
        return self.frames[self.note.index(self.note.select())][1]


    def get_current_tab(self):
        return self.note.index(self.note.select())


    def check_for_update(self, booting=False):
        res, link, v = updater.check_for_update(str(__version__))
        if res == True:

            yn = messagebox.askyesno(title="New Update Available", message="Would you like to visit our downloads page to download Sparlab version {}?".format(v))
            if yn == True:
                webbrowser.open('https://www.umensch.com/downloads/', new=2)
            else:
                return

        else:
            if booting == False:
                messagebox.showinfo(title="", message="No update is currently available.")

if __name__ == '__main__':
    freeze_support()
    q1 = Queue()
    q2 = Queue()

    root = App(q1, q2)
    listener = _input.Session_Thread(args=(q1, q2, root.port))
    listener.daemon = True
    listener.start()
    root.mainloop()
