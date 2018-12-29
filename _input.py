import multiprocessing
from key_board import keyboard
import time
import BotController

class Session_Thread(multiprocessing.Process):
    """
    This is for inputting hotkeys and 'bot' commands to virtual xbox controller api
    """

    def __init__(self, args=None):
        super().__init__(target=self.key_listener)
        # queue for getting info from 1st process
        self.q1, self.q2, self.joy_n = args

        # Set up the GUI part
        self.joy = BotController.VXBOX_Device(self.joy_n)

        self.running = True
        self.playing = False
        self.hks_on = False
        self.rest = True
        # ignore action interval (set to False at end of loops)
        self.iai = False
        #holds all hotkeys
        self.hotkeys = []
        self.hk_names = []
        #holds all action strings
        self.strings = []
        self.pending = []
        # variable for making sure client process has been informed
        self.client_informed = False
        # Start the periodic call in the GUI to check if the queue contains
    def check_for_vbus(self):
        if self.joy.isVBusExists() == False:
            self.q2.put({'vbusnotexist': False})
        else:
            return

    def processIncoming(self):
        # unpack data from queue

        # may need to find a more robust way of doing this. Test for speed
        #begin = time.time()
        while self.q1.qsize():
            try:
                info = self.q1.get(0)
                if info is not None:
                    # True or False
                    try:
                        self.cfg = info['cfg']
                    except Exception as e:
                        pass
                        #print(e)

                    try:
                        self.joycfg = info['joycfg']
                    except Exception as e:
                        pass

                    try:
                        self.playing = info['playing']

                        if self.playing == True:
                            self.rest = False
                            #print"self.playing = True")
                            #if self.strings == []:
                            self.strings = info['actlist']
                        else:
                            self.rest = True
                            #print"self.playing = False")
                            self.strings = []

                        self.client_informed = True
                        self.pending = []

                    except Exception as e:
                        pass
                        #print("PLAYING EXCEPTION: ", e)

                    try:
                        n = int(info['joy'])
                        #print("joy number: ", n)
                        if n != self.joy_n:
                            self.joy = BotController.VXBOX_Device(n)

                    except Exception as e:
                        pass

                    try:
                        self.settings = info['settings']
                        self.fps = int(self.settings['fps'])
                        self.start_delay_t = float(self.settings['start delay'])
                        self.act_int_t = float(self.settings['ADI'])
                        self.defaultdir = self.settings['default direction']
                    except Exception as e:
                        #print("SETTINGS: ", e)
                        pass
                    try:
                        self.custom_delays = info['delay tuners']
                        #print"new custom delays: ", self.custom_delays)
                        self.fps = int(self.custom_delays['fps'])
                        self.act_int_t = float(self.custom_delays['ADI'])
                        print("action interval: {}; custom delays: {}".format(self.act_int_t, self.custom_delays))
                    except Exception as e:
                        #print("custom delay error: ", e)
                        pass

                    try:
                        self.hks_on = info['hks on']
                    except Exception as e:
                        pass
                        # print("HKS ON: ", e)
                    try:
                        self.facing = info['facing']
                    except Exception as e:
                        #print("FACING: ", e)
                        pass
                    try:
                        if info['hks on'] == True:
                            # throw error if bus driver doesn't exist
                            self.check_for_vbus()
                            # turn on controller
                            self.joy.TurnOn()

                            for k,v in self.cfg.items():
                                hk = v['Hotkey']
                                try:
                                    string = eval(v['String'])
                                except:
                                    string = v['String']
                                notation = v['Notation']

                                if hk not in ["None", "'None'"] and string not in ["None", "'None'"] and hk != None and string != None and hk not in self.hk_names:
                                    try:
                                        key = keyboard.add_hotkey(str(hk), self.perform_hk, args=(notation,string))
                                        #print"appending {} to list".format(hk))
                                        self.hk_names.append(hk)
                                        self.hotkeys.append(key)
                                    except:
                                        pass

                            if 'play hotkey' not in self.hk_names:
                                print("play hotkey added")
                                v = self.settings['play hotkey']
                                key = keyboard.add_hotkey(str(v), self.toggle_play)
                                self.hk_names.append('play hotkey')
                                self.hotkeys.append(key)

                            if 'switch sides hotkey' not in self.hk_names:
                                v = self.settings['switch sides hotkey']
                                key = keyboard.add_hotkey(str(v), self.switch_sides)
                                self.hk_names.append('switch sides hotkey')
                                self.hotkeys.append(key)

                            # if 'increase tuner hotkey' not in self.hk_names:
                            #     v = self.settings['increase tuner hotkey']
                            #     #print'increase tuner appended')
                            #     key = keyboard.add_hotkey(str(v), self.increase_tuner)
                            #     self.hk_names.append('increase tuner hotkey')
                            #     self.hotkeys.append(key)
                            #
                            # if 'decrease tuner hotkey' not in self.hk_names:
                            #     v = self.settings['decrease tuner hotkey']
                            #     #print'decrease tuner appended')
                            #     key = keyboard.add_hotkey(str(v), self.decrease_tuner)
                            #     self.hk_names.append('decrease tuner hotkey')
                            #     self.hotkeys.append(key)
                            #
                            # if 'next tuner hotkey' not in self.hk_names:
                            #     v = self.settings['next tuner hotkey']
                            #     #print'increase adi hk appended')
                            #     key = keyboard.add_hotkey(str(v), self.next_tuner)
                            #     self.hk_names.append('next tuner hotkey')
                            #     self.hotkeys.append(key)
                            #
                            # if 'previous tuner hotkey' not in self.hk_names:
                            #     v = self.settings['previous tuner hotkey']
                            #     #print'previous tuner hk appended')
                            #     key = keyboard.add_hotkey(str(v), self.prev_tuner)
                            #     self.hk_names.append('previous tuner hotkey')
                            #     self.hotkeys.append(key)


                            for k,v in self.joycfg.items():
                                hk = v['Hotkey']
                                try:
                                    string = eval(v['String'])
                                except:
                                    string = v['String']

                                notation = v['Notation']

                                if hk not in ["None", "'None'"] and string not in ["None", "'None'"] and hk != None and string != None and hk not in self.hk_names:
                                    try:
                                        key = keyboard.add_hotkey(str(hk), self.perform_hk, args=(notation,string))
                                        self.hk_names.append(hk)
                                        self.hotkeys.append(key)
                                    except:
                                        pass

                        else:
                            #print"hks off")
                            # turn off controller
                            self.joy.TurnOff()

                            # unbind hotkeys
                            for k in self.hotkeys:
                                try:
                                    keyboard.remove_hotkey(k)
                                except:
                                    pass
                            # empty containers
                            self.strings = []
                            self.hotkeys = []
                            self.hk_names = []
                            self.pending = []
                    except Exception as e:
                        print("HKS: ", e)
                        #pass


            except Exception as e:
                msg = "{}: {}".format(type(e).__name__, e.args)
                #printmsg)

        # end = time.time()
        # print("P2 Process Incoming speed: ", end - begin)

    def endApplication(self):
        self.running = False

    def update_queue(self, info):
        if self.running == False:
            quit()

        # place info on client process' queue
        self.q2.put(info)

    def key_listener(self):
        """This loop runs while client process is alive."""

        self.t = 0
        while self.running:

            if self.playing == True:

                self.start_delay()
                for string in self.strings:
                    #print"string: ", string)
                    self.parse_action(string)
                    try:
                        self.joy.action_interval(self.act_int_t, ignore=self.iai)
                    except Exception as e:
                        print("ACTION INTERVAL ERROR: ", e)
                        #pass

            self.iai = False

            # check for msg from client every 0.2 seconds
            if self.playing == False:
                if self.t % 200 == 0:
                    self.processIncoming()
                    if self.t >= 10000000:
                        self.t = 0

                self.t += 1


    def perform_hk(self, notation, string):
        info = {'user input': (notation, string)}
        self.update_queue(info)
        # give main process time to pause the sequence
        if self.playing == True:
            time.sleep(0.3)
        self.parse_action(string, hk=True)

    def parse_action(self, string, hk=False):

        if (self.facing == 'R' and self.defaultdir == 'L') or (self.facing == 'L' and self.defaultdir == 'R'):
            flipx = True
        else:
            flipx = False

        # only execute action if the hks are on (they are on whenever controller is on)
        if self.hks_on == True:
            if hk == False:
                #((notation, string))
                try:
                    iterstring = eval(string[1])
                except Exception as e:
                    iterstring = string[1]


                if iterstring in list(self.custom_delays):
                    f = self.custom_delays[iterstring]
                    t = float(f)
                    print("iterstring: {}, t: {}".format(iterstring, t))
                    #print"f = {}; delay for: {}".format(f,t))
                    self.joy.delay_for(t)
                    return

                try:
                    for iter, a in enumerate(iterstring):
                        #print"a: ", a)
                        self.processIncoming()
                        # print("(AUTO) a: {}".format(a))
                        if a in list(self.settings) and a != 'j_f' and 'delay' not in a:
                            # print("{} settings: {}".format(a, self.settings[a]))
                            cfg = self.settings[a]
                        elif a == 'j_f':
                            cfg = self.fps
                            print("fps: ", cfg)
                        elif 'delay' in a:
                            a, t = a.split("(")
                            cfg = float("".join(list(t)[0:-1]))
                            print("delay: {}, t: {}".format(a, cfg))
                        else:
                            cfg = None

                        if self.rest == False:
                            getattr(self.joy, str(a))(cfg, flipx=flipx)


                        info = {'action': a}
                        self.update_queue(info)

                    if a == 'i_a_i':
                        self.iai = True
                except Exception as e:
                    #print("ITERSTRING ERROR: ", e)
                    pass

            else:
                iterstring = string
                # print("(HK) iterstring: ", iterstring)
                for a in iterstring:
                    # load configs from settings to pass as arg
                    # print("(HK) a: ", a)
                    if a in list(self.settings) and a != 'j_f' and 'delay' not in a:
                        # print("{} settings: {}".format(a, self.settings[a]))
                        cfg = self.settings[a]
                    elif a == 'j_f':
                        cfg = self.fps
                        print("fps: ", cfg)
                    elif 'delay' in a:
                        a, t = a.split("(")
                        cfg = float("".join(list(t)[0:-1]))
                        print("delay: {}, t: {}".format(a, cfg))
                    else:
                        cfg = None
                    # execute the action
                    getattr(self.joy, str(a))(cfg)

                    # inform main process
                    info = {'hk action': a}
                    self.update_queue(info)

                if a == 'i_a_i':
                    self.iai = True


    def start_delay(self):

        # inform client process that action is starting from beginning
        self.processIncoming()
        info = {'start over': True}
        self.update_queue(info)

        whol = int(self.start_delay_t)
        #print"whol: ", whol)
        xtra = self.start_delay_t - whol
        #print("whol: {}, xtra: {}".format(whol, xtra))
        #print"xtra: ", xtra)
        for i in range(whol):
            # print("processIncoming")
            self.processIncoming()
            if self.playing == False:
                #print"SELF.PLAYING = FALSE ")

                return
            time.sleep(0.5)

            self.processIncoming()
            if self.playing == False:
                #print"SELF.PLAYING = FALSE ")
                return
            time.sleep(0.5)

        time.sleep(xtra)



    def toggle_play(self):
        # play/pause
        if self.playing == True and self.client_informed == True:
            self.client_informed = False
            self.joy.neutral('bla')
            self.rest = True
            #print"toggle_play: self.playing = false")
            info = {'playing': False}
            self.update_queue(info)

        elif self.playing == False and self.client_informed == True:
            self.client_informed = False
            self.rest = False
            self.joy.neutral('bla')
            #print"toggle_play: self.playing = true")
            info = {'playing': True}
            self.update_queue(info)



    def switch_sides(self):
        #Left/right
        if self.facing == 'R':
            self.facing = 'L'
        else:
            self.facing = 'R'

        info = {'facing': self.facing}
        self.update_queue(info)
    #
    # def increase_tuner(self):
    #     #print"increase tuner")
    #     info = {'command': 'increase tuner'}
    #     self.update_queue(info)
    #
    # def decrease_tuner(self):
    #     #print"decrease tuner")
    #     info = {'command': 'decrease tuner'}
    #     self.update_queue(info)
    #
    # def next_tuner(self):
    #     #print"next tuner")
    #     info = {'command': 'next tuner'}
    #     self.update_queue(info)
    #
    # def prev_tuner(self):
    #     #print"prev tuner")
    #     info = {'command': 'previous tuner'}
    #     self.update_queue(info)
