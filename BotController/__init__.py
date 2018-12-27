import sys
import os
from ctypes import *
import time

dll_path = os.path.dirname(__file__) + os.sep + "vXboxInterface.dll"

try:
    vj = cdll.LoadLibrary(dll_path)
except OSError:
    sys.exit("Unable to load controller SDK DLL. Ensure that {} is present".format("vXboxInterface.dll"))

class VXBOX_Device(object):
    def __init__(self, rID=None):
        self.id = rID
        self.is_on = False

    def a_d(self, cfg, flipx=None):
        result = vj.SetBtnA(self.id, True)
        if result == False:
            return False
        else:
            return True

    def a_u(self, cfg, flipx=None):
        result = vj.SetBtnA(self.id, False)
        if result == False:
            return False
        else:
            return True

    def b_d(self, cfg, flipx=None):
        result = vj.SetBtnB(self.id, True)
        if result == False:
            return False
        else:
            return True

    def b_u(self, cfg, flipx=None):
        result = vj.SetBtnB(self.id, False)
        if result == False:
            return False
        else:
            return True

    def x_d(self, cfg, flipx=None):
        result = vj.SetBtnX(self.id, True)
        if result == False:
            return False
        else:
            return True

    def x_u(self, cfg, flipx=None):
        result = vj.SetBtnX(self.id, False)
        if result == False:
            return False
        else:
            return True

    def y_d(self, cfg, flipx=None):
        result = vj.SetBtnY(self.id, True)
        if result == False:
            return False
        else:
            return True

    def y_u(self, cfg, flipx=None):
        result = vj.SetBtnY(self.id, False)
        if result == False:
            return False
        else:
            return True

    def rb_d(self, cfg, flipx=None):
        result = vj.SetBtnRB(self.id, True)
        if result == False:
            return False
        else:
            return True

    def rb_u(self, cfg, flipx=None):
        result = vj.SetBtnLB(self.id, False)
        if result == False:
            return False
        else:
            return True

    def lb_d(self, cfg, flipx=None):
        result = vj.SetBtnLB(self.id, True)
        if result == False:
            return False
        else:
            return True

    def lb_u(self, cfg, flipx=None):
        result = vj.SetBtnLB(self.id, False)
        if result == False:
            return False
        else:
            return True

    def start_d(self, cfg, flipx=None):
        state = True
        result = vj.SetBtnStart(self.id, state)
        if result == False:
            return False
        else:
            return True

    def start_u(self, cfg, flipx=None):
        state = False
        result = vj.SetBtnStart(self.id, state)
        if result == False:
            return False
        else:
            return True

    def back_d(self, cfg, flipx=None):
        result = vj.SetBtnBack(self.id, True)
        if result == False:
            return False
        else:
            return True

    def back_u(self, cfg, flipx=None):
        result = vj.SetBtnBack(self.id, False)
        if result == False:
            return False
        else:
            return True

    def rt_d(self, cfg, flipx=None):
        result = vj.SetTriggerR(self.id, True)
        if result == False:
            return False
        else:
            return True

    def rt_u(self, cfg, flipx=None):
        result = vj.SetTriggerR(self.id, False)
        if result == 0:
            return False
        else:
            return True

    def lt_d(self, cfg, flipx=None):
        result = vj.SetTriggerL(self.id, True)
        if result == False:
            return False
        else:
            return True

    def lt_u(self, cfg, flipx=None):
        result = vj.SetTriggerL(self.id, False)
        if result == 0:
            return False
        else:
            return True

    def dpu_d(self, cfg, flipx=None):
        result = vj.SetDpadUp(self.id)
        if result == False:
            return False
        else:
            return True

    def dpu_u(self, cfg, flipx=None):
        return vj.SetDpadOff(self.id)

    def dpr_d(self, cfg, flipx=None):
        if flipx == True:
            result = vj.SetDpadLeft(self.id)
        else:
            result = vj.SetDpadRight(self.id)

        if result == False:
            return False
        else:
            return True

    def dpr_u(self, cfg, flipx=None):
        return vj.SetDpadOff(self.id)

    def dpl_d(self, cfg, flipx=None):
        if flipx == True:
            vj.SetDpadRight(self.id)
        else:
            result = vj.SetDpadLeft(self.id)
        if result == False:
            return False
        else:
            return True

    def dpl_u(self, cfg, flipx=None):
        return vj.SetDpadOff(self.id)

    def dpd_d(self, cfg, flipx=None):
        result = vj.SetDpadDown(self.id)
        if result == False:
            return False
        else:
            return True

    def dpd_u(self, cfg, flipx=None):
        return vj.SetDpadOff(self.id)


    def la_dr(self, cfg, flipx=None):
        if flipx == True:
            return self.la(cfg, flipx=flipx)
        return self.la(cfg)

    def la_r(self, cfg, flipx=None):
        if flipx == True:
            return self.la(cfg, flipx=flipx)
        return self.la(cfg)

    def la_ur(self, cfg, flipx=None):
        if flipx == True:
            return self.la(cfg, flipx=flipx)
        return self.la(cfg)

    def la_l(self, cfg, flipx=None):
        if flipx == True:
            return self.la(cfg, flipx=flipx)
        return self.la(cfg)

    def la_ul(self, cfg, flipx=None):
        if flipx == True:
            return self.la(cfg, flipx=flipx)
        return self.la(cfg)

    def la_u(self, cfg, flipx=None):
        return self.la(cfg)

    def la_dl(self, cfg, flipx=None):
        if flipx == True:
            return self.la(cfg, flipx=flipx)
        return self.la(cfg)

    def la_d(self, cfg, flipx=None):
        return self.la(cfg)

    def la_n(self, cfg, flipx=None):
        result = vj.SetAxisY(self.id, 0)
        result = vj.SetAxisX(self.id, 0)
        return result


    def ra_dr(self, cfg, flipx=None):
        if flipx == True:
            return self.ra(cfg, flipx=flipx)
        return self.ra(cfg)

    def ra_r(self, cfg, flipx=None):
        if flipx == True:
            return self.ra(cfg, flipx=flipx)
        return self.ra(cfg)

    def ra_ur(self, cfg, flipx=None):
        if flipx == True:
            return self.ra(cfg, flipx=flipx)
        return self.ra(cfg)

    def ra_dr(self, cfg, flipx=None):
        if flipx == True:
            return self.ra(cfg, flipx=flipx)
        return self.ra(cfg)

    def ra_ul(self, cfg, flipx=None):
        if flipx == True:
            return self.ra(cfg, flipx=flipx)
        return self.ra(cfg)

    def ra_u(self, cfg, flipx=None):
        return self.ra(cfg)

    def ra_dl(self, cfg, flipx=None):
        if flipx == True:
            return self.ra(cfg, flipx=flipx)
        return self.ra(cfg)

    def ra_d(self, cfg, flipx=None):
        return self.ra(cfg)

    def ra_l(self, cfg, flipx=None):
        if flipx == True:
            return self.ra(cfg, flipx=flipx)
        return self.ra(cfg)

    def ra_n(self, cfg, flipx=None):
        result = vj.SetAxisRy(self.id, 0)
        result = vj.SetAxisRx(self.id, 0)
        return result

    def j_f(self, fps, flipx=None):
        beg = time.time()
        #print("begin time: ", beg)
        s = int(fps) / 1000
        time.sleep(s)
        end = time.time()
        # print("j_f time: ", end - beg)
        return


    def la(self, state, flipx=False):
        if isinstance(state, tuple):
            hexx, hexy = state[0], state[1]
        elif isinstance(state, str):
            hexx, hexy = eval(state)
        else:
            # print("la not a string or tuple: {}".format())
            return False

        result = vj.SetAxisY(self.id, hexy)

        if result == False:
            # print("bad result: hexy = {}".format(hexy))
            return False

        xval = hexx if flipx == False else -hexx
        result = vj.SetAxisX(self.id, xval)

        if result == False:
            # print("bad result: xval = {}".format(xval))
            return False

        return True

    def ra(self, state, flipx=False):
        if isinstance(state, tuple):
            hexx, hexy = state[0], state[1]
        elif isinstance(state, str):
            hexx, hexy = eval(state)
        else:
            return False

        result = vj.SetAxisRy(self.id, hexy)

        if result == False:
            return False

        xval = hexx if flipx == False else -hexx
        result = vj.SetAxisRx(self.id, xval)

        if result == False:
            return False

        return True



    def delay_for(self, t):
        begin = time.time()
        time.sleep(t)
        end = time.time()
        # print("delay_for runtime: ", end - begin)

    def neutral(self, cfg, flipx=None):
        vj.SetBtnA(self.id,False)
        vj.SetBtnB(self.id,False)
        vj.SetBtnX(self.id,False)
        vj.SetBtnY(self.id,False)
        vj.SetBtnRB(self.id,False)
        vj.SetBtnLB(self.id,False)
        vj.SetBtnStart(self.id,False)
        vj.SetBtnBack(self.id,False)
        vj.SetTriggerR(self.id,0)
        vj.SetTriggerL(self.id,0)
        vj.SetDpadOff(self.id)
        vj.SetAxisX(self.id,0)
        vj.SetAxisY(self.id,0)
        vj.SetAxisRx(self.id,0)
        vj.SetAxisRy(self.id,0)

    def i_a_i(self, yes):
        pass


    def action_interval(self, t, ignore=False):
        if ignore == True:
            return
        # by default
        # sleep between every action so there are spaces b/w inputs (configurable in settings.txt)
        begin = time.time()
        time.sleep(t)
        end = time.time()
        # print("action interval runtime: ", end - begin)

    # i, i2p, act, cfg, flipx, t, fps
    # listener = input.Session_Thread(args=(q1, q2, root.port))
    # listener.daemon = True
    # listener.start()

    def procrast(self, st, a, cfg, fx):
        time.sleep(st)
        getattr(self, str(a))(cfg, flipx=fx)

    def isControllerOwned(self, cfg):
        return self.isControllerOwned(self.id)

    def isControllerExists(self, cfg):
        return self.isControllerExists(self.id)

    def TurnOff(self):
        try:
            self.is_on = False
            vj.UnPlug(self.id)
            return True
        except:
            return False

    def TurnOn(self):
        try:
            vj.PlugIn(self.id)
            self.is_on = True
            return True
        except:
            # print("controller already on or taken")
            return False

    def reset(self, cfg):
        self.TurnOff(self.id)
        # print("RESETTING...")
        time.sleep(3)
        return self.TurnOn(self.id)


    def __del__(self):
        # print("DEL")
        # free up the controller before losing access
        self.TurnOff()

    def isVBusExists(self):
        result = vj.isVBusExists(self.id)

        if result == False:
            return False
        else:
            return True

    def isControllerOwned(self, n):
        return vj.isControllerOwned(n)

    def isControllerExists(self, n):
        return vj.isControllerExists(n)

    def GetNumEmptyBusSlots(self, n):
        return vj.GetNumEmptyBusSlots(UCHAR * nSlots)
