# coding:utf-8
import os
import time
import datetime
import re

try:
    import configparser as cp
except Exception:
    import ConfigParser as cp


error_level = 2


# Change color of light.
def chg_light_to_green(obj, instance):
    obj.itemconfig(instance, fill='green')


def chg_light_to_red(obj, instance):
    obj.itemconfig(instance, fill='red')


def encode_utf8(str):
    return str.encode(encoding="utf-8")


def msg_out(obj_msg_out, str):
    obj_msg_out.insert('insert', str)


def sand_glass(seconds, obj_msg_out=None):
    print("    ", end='')
    if obj_msg_out:
        msg_out(obj_msg_out, '    ')
    for i in range(seconds - 1):
        if obj_msg_out:
            msg_out(obj_msg_out, '.')
        print('.', end='')
        time.sleep(1)
    if obj_msg_out:
        msg_out(obj_msg_out, '\n')
    print('\n')


def deco_OutFromFolder(func):
    strOriFolder = os.getcwd()

    def _deco(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as E:
            # print(func.__name__, E)
            pass
        finally:
            os.chdir(strOriFolder)

    return _deco

# def deco_message_output(func):
#     def _deco(self, *args, **kwargs):
#         def __deco(self, *args, **kwargs):
#             try:
#                 return func(self, *args, **kwargs)
#             except Exception as E:
#                 print(func.__name__, E)
#         return
#     return _deco


def deco_Exception(func):

    def _deco(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as E:
            print(func.__name__, E)

    return _deco


def time_now_folder():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def time_now_to_show():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def is_Warning(intValue, data):
    '''
    data is int or a tuple
    '''
    if isinstance(data, int):
        print('<>')
        if intValue > data:
            return True
    else:
        if intValue >= data[1]:
            return 2
        elif intValue >= data[0]:
            return 1
        else:
            return 0


def is_trace_level(num):
    if num in (1, 2, 3):
        return True


def is_IP(strIP):
    reIP = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if reIP.match(strIP):
        return True


def is_IP_list(lstIP):
    return all(map(is_IP, lstIP))


def is_file(strFileName):
    if os.path.isfile(strFileName):
        return True
    else:
        return False


def is_folder(strDirName):
    if os.path.isdir(strDirName):
        return True
    else:
        return False


def is_port(intPortNum):
    if type(intPortNum) == int:
        return True
    if type(intPortNum) == str:
        if intPortNum.isdigit():
            if type(eval(intPortNum)) == int:
                return True
    return False


def ShowErr(*argvs):
    '''
    Four argv:
    ClassName, FunctionName, MessageGiven, MessageRaised
    '''
    if error_level == 1:
        print(str('''
----------------------------------------------------------------------------
|*Error message:                                                           |
|    Error message: {:<55}|
|        {:<66}|
----------------------------------------------------------------------------\
'''.format(argvs[2], err_msg=(argvs[3] if argvs[3] else ''))))
    elif error_level == 2:
        pass
    elif error_level == 3:
        print(str('''
----------------------------------------------------------------------------
|*Error message:                                                           |
|    Class name :   {:<55}|
|    Function name: {:<55}|
|    Error message: {:<55}|
|        {:<66}|
----------------------------------------------------------------------------\

'''.format(argvs[0], argvs[1], argvs[2], err_msg=(argvs[3] if argvs[3] else ''))))


def make_dir(strFolder):
    if strFolder:
        if os.path.exists(strFolder):
            pass
        else:
            try:
                os.makedirs(strFolder)
            except Exception as E:
                print('Create folder "{}" fail with error:\n\t"{}"'.format(
                    strFolder, E))


def GotoFolder(strFolder):

    def _mkdir():
        if strFolder:
            if os.path.exists(strFolder):
                return True
            else:
                try:
                    os.makedirs(strFolder)
                    return True
                except Exception as E:
                    print('Create folder "{}" fail with error:\n\t"{}"'.format(
                        strFolder, E))

    if _mkdir():
        try:
            os.chdir(strFolder)
            return True
        except Exception as E:
            print('Change to folder "{}" fail with error:\n\t"{}"'.format(
                strFolder, E))


class TimeNow(object):

    def __init__(self):
        self._now = time.localtime()

    def y(self):  # Year
        return (self._now[0])

    def mo(self):  # Month
        return (self._now[1])

    def d(self):  # Day
        return (self._now[2])

    def h(self):  # Hour
        return (self._now[3])

    def mi(self):  # Minute
        return (self._now[4])

    def s(self):  # Second
        return (self._now[5])

    def wd(self):  # Day of the Week
        return (self._now[6])

# delete unnecessary module and unnecessary function


if __name__ == '__main__':
    pass
