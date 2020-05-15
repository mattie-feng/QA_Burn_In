# coding:utf-8

from __future__ import print_function
import sys
import time
import re
import Conn as conn
import Sundry as s
from collections import OrderedDict as odd

# <<<Config Field>>>
ip_engine_target = '10.203.1.4'
ip_engine_initiator = '10.203.1.5'

telnet_port = 23
FTP_port = 21
passwd = 'password'
trace_level_cfg = 2
firmware_file_name = 'fw.bin'

strTraceFolder = 'Trace'
strPCFolder = 'Current_Config'
strResultFolder = 'test_result'
lstPCCommand = ['vpd',
                'conmgr status',
                'mirror',
                'group',
                'map',
                'drvstate',
                'history',
                'sfp all']


def receive(message_output,
            light_obj_telnet,
            light_telnet,
            light_obj_FTP,
            light_FTP,
            mode,
            IP_Entered,
            license,
            version,
            speed
            ):

    def _entry_judge():
        if s.is_IP(IP_Entered) and license:
            return True
        elif not s.is_IP(IP_Entered):
            message_output.insert(
                'insert', '\n***Please type correct IP address.\n')
            sys.exit()
        elif not license:
            message_output.insert(
                'insert', '\n***Please type correct license code.\n')
            sys.exit()
        else:
            message_output.insert(
                'insert', '\n***Please check ip and(or) licenses.\n')
            sys.exit()

    solid_args = (
        message_output,
        light_obj_telnet,
        light_telnet,
        light_obj_FTP,
        light_FTP)
    if mode == 'target':
        if _entry_judge():
            config_target(IP_Entered, license, version, speed, solid_args)

    elif mode == 'initiator':
        if _entry_judge():
            config_initiator(IP_Entered, license, version, speed, solid_args)

    elif mode == 'start':
        start_test(version, solid_args)

    elif mode == 'status':
        get_test_status(version, solid_args)

    elif mode == 'result':
        get_test_result(version, solid_args)

    elif mode == 'reset':
        reset_all_engines(version, solid_args)


# Test Field

# def _get_max_serial_num(self):
#     def _get_serial_num(str_vpd_info):
#         re_serial_num = re.compile(r'(?<=Serial Number : )\d{8}')
#         return re_serial_num.search(str_vpd_info).group()
#     obj_engine_target = Action(ip_engine_target, telnet_port, passwd, FTP_port, version, solid_args)
#     obj_engine_initiator = Action(ip_engine_initiator, telnet_port, passwd, FTP_port, version, solid_args)
#     vpd_engine_target = obj_engine_target.strVPD
#     vpd_engine_initiator = obj_engine_initiator.strVPD
#     time.sleep(0.2)
#     del obj_engine_target
#     del obj_engine_initiator

# return max(int(_get_serial_num(vpd_engine_target)),
# int(_get_serial_num(vpd_engine_initiator)))

def start_test(version, solid_args):
    obj_msg_out = solid_args[0]
    obj_light_FTP = solid_args[3]
    instance_light_FTP = solid_args[4]

    objEngine = Action(
        ip_engine_initiator,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)
    s.msg_out(obj_msg_out, '  3. Start testing.\n')
    objEngine.start_test()
    time.sleep(1)
    del objEngine
    s.chg_light_to_red(obj_light_FTP, instance_light_FTP)


def get_test_status(version, solid_args):
    obj_msg_out = solid_args[0]
    # obj_light_telnet = solid_args[1]
    # instance_light_telnet = solid_args[2]
    obj_light_FTP = solid_args[3]
    instance_light_FTP = solid_args[4]
    objEngine = Action(
        ip_engine_initiator,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)
    s.msg_out(obj_msg_out, '  4. Start getting status.\n')
    s.msg_out(obj_msg_out, '  4.1 Status: %s.\n' % objEngine.get_status())
    time.sleep(1)
    del objEngine
    s.chg_light_to_red(obj_light_FTP, instance_light_FTP)


def get_test_result(version, solid_args):
    obj_msg_out = solid_args[0]
    # obj_light_telnet = solid_args[1]
    # instance_light_telnet = solid_args[2]
    obj_light_FTP = solid_args[3]
    instance_light_FTP = solid_args[4]
    objEngine = Action(
        ip_engine_initiator,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)
    s.msg_out(obj_msg_out, '  5. Start getting result.\n')
    objEngine.get_result()
    time.sleep(1)
    del objEngine
    s.chg_light_to_red(obj_light_FTP, instance_light_FTP)


def reset_all_engines(license, version, speed, solid_args):
    obj_msg_out = solid_args[0]
    # obj_light_telnet = solid_args[1]
    # instance_light_telnet = solid_args[2]
    obj_light_FTP = solid_args[3]
    instance_light_FTP = solid_args[4]

    def _reset_engine(ip_engine):
        s.msg_out(
            obj_msg_out,
            '    6.x Start resetting engine %s.\n' %
            ip_engine)
        objEngine = Action(
            ip_engine,
            telnet_port,
            passwd,
            FTP_port,
            version,
            solid_args)
        objEngine.reset_engine()
        time.sleep(1)
        s.msg_out(
            obj_msg_out,
            '    6.x Finish resetting engine %s.\n' %
            ip_engine)
        del objEngine
        s.chg_light_to_red(obj_light_FTP, instance_light_FTP)

    s.msg_out(obj_msg_out, '  6. Start resetting all engines.\n')
    _reset_engine(ip_engine_target)
    _reset_engine(ip_engine_initiator)


# Config Field
def _config_universal(mode, IP_Entered, license, version, speed, solid_args):
    obj_msg_out = solid_args[0]
    obj_light_telnet = solid_args[1]
    instance_light_telnet = solid_args[2]
    obj_light_FTP = solid_args[3]
    instance_light_FTP = solid_args[4]

    if mode == 'target':
        ip_engine = ip_engine_target
    elif mode == 'initiator':
        ip_engine = ip_engine_initiator

    objEngine = Action(
        IP_Entered,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)
    s.msg_out(obj_msg_out, '  0.1 Start changing FW.\n')
    # objEngine.change_FW(firmware_file_name)
    s.msg_out(obj_msg_out, '  0.1 Finish changing FW, Rebooting...\n')
    del objEngine

    objEngine = Action(
        IP_Entered,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)
    s.msg_out(obj_msg_out, '  0.2 Start restoring factory default.\n')
    objEngine.factory_default()
    time.sleep(0.25)
    del objEngine

    objEngine = Action(
        IP_Entered,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)
    solid_args[0].insert('insert', '  0.3 Start changing IP address.\n')
    objEngine.change_ip_address(ip_engine)
    time.sleep(0.25)
    del objEngine

    objEngine = Action(
        ip_engine,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)
    s.msg_out(obj_msg_out, '  0.4 Start changing UID.\n')
    objEngine.change_UID(mode)
    time.sleep(0.25)
    del objEngine

    objEngine = Action(
        ip_engine,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)

    s.msg_out(obj_msg_out, '  0.5 Start setting shutdown behaviour.\n')
    objEngine.shutdown_behaviour()

    s.msg_out(obj_msg_out, '  0.6 Start changing mode of FC ports.\n')
    objEngine.change_FC_mode('all', 'loop')

    s.msg_out(obj_msg_out, '  0.7 Start changing speed of FC ports.\n')
    objEngine.change_FC_speed('all', speed)

    s.msg_out(obj_msg_out, '  0.8 Start installing license.\n')
    objEngine.install_license(license)

    s.msg_out(obj_msg_out, '  0.9 Start syncing time of engine with system.\n')
    objEngine.sync_time()

    time.sleep(0.25)
    del objEngine
    time.sleep(1)


def config_target(IP_Entered, license, version, speed, solid_args):
    obj_msg_out = solid_args[0]
    obj_light_telnet = solid_args[1]
    instance_light_telnet = solid_args[2]
    # obj_light_FTP = solid_args[3]
    # instance_light_FTP = solid_args[4]

    _config_universal(
        'target',
        IP_Entered,
        license,
        version,
        speed,
        solid_args)

    objEngine = Action(
        ip_engine_target,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)

    s.msg_out(obj_msg_out, '  1.1 Start creating fake drives.\n')
    objEngine.create_fake_drive()

    s.msg_out(obj_msg_out, '  1.2 Start creating mirror and mapping.\n')
    objEngine.mirror_and_mapping()

    s.msg_out(obj_msg_out, '  1.3 Start registering initiators.\n')
    objEngine.register_initiator()

    # show info -- mirror and mapping.
    objEngine.show_mirror_and_mappting()

    # show info -- conmgr status.
    objEngine.show_conmgr_status()

    s.msg_out(obj_msg_out, '  1. Finish configuring target engine.\n')
    time.sleep(0.25)
    del objEngine
    s.chg_light_to_red(obj_light_telnet, instance_light_telnet)


def config_initiator(IP_Entered, license, version, speed, solid_args):
    obj_msg_out = solid_args[0]
    obj_light_telnet = solid_args[1]
    instance_light_telnet = solid_args[2]
    # obj_light_FTP = solid_args[3]
    # instance_light_FTP = solid_args[4]

    _config_universal(
        'initiator',
        IP_Entered,
        license,
        version,
        speed,
        solid_args)

    objEngine = Action(
        ip_engine_initiator,
        telnet_port,
        passwd,
        FTP_port,
        version,
        solid_args)
    s.msg_out(obj_msg_out, '  2.1 Start registering drives.\n')
    objEngine.register_drives()

    # show info -- conmgr status.
    objEngine.show_conmgr_status()

    s.msg_out(obj_msg_out, '  2. Finish configuring initiator engine.\n')
    time.sleep(0.25)
    del objEngine
    s.chg_light_to_red(obj_light_telnet, instance_light_telnet)


class Action():

    def __init__(self, strIP, intTNPort, strPassword,
                 intFTPPort, version, solid_args, intTimeout=3):
        self._host = strIP
        self._TNport = intTNPort
        self._FTPport = intFTPPort
        self._FTP_username = self.get_ftp_username(version)
        self._password = strPassword
        self._timeout = intTimeout

        # restore object and instance from solid_args
        self.message_output = solid_args[0]
        self.obj_light_telnet = solid_args[1]
        self.instance_light_telnet = solid_args[2]
        self.obj_light_FTP = solid_args[3]
        self.instance_light_FTP = solid_args[4]

        self._TN_Conn = None
        self._FTP_Conn = None
        self._TN_Connect_Status = None
        self._telnet_connect()
        self.AHStatus = self._TN_Conn.is_AH()
        self.strVPD = self._executeCMD('vpd')

    # version determines the value of FTP username
    def get_ftp_username(self, version):
        if version == 'loxoll':
            return 'adminftp'
        elif version == 'vicom':
            return 'ftpvicom'

    def _telnet_connect(self):
        s.msg_out(
            self.message_output,
            '0. Telnet Connecting to %s ...\n' %
            self._host)
        self._TN_Conn = conn.HAAPConn(self._host,
                                      self._TNport,
                                      self._password,
                                      self._timeout)
        self._TN_Connect_Status = self._TN_Conn.get_connection_status()
        if self._TN_Connect_Status:
            s.msg_out(
                self.message_output,
                '0. Telnet Connected to %s.\n' %
                self._host)
            s.chg_light_to_green(
                self.obj_light_telnet,
                self.instance_light_telnet)
        else:
            s.msg_out(
                self.message_output,
                '0. Telnet Connect to %s Failed!!!\n' %
                self._host)

    # @s.deco_Exception
    def _executeCMD(self, cmd):
        if self._TN_Connect_Status:
            return self._TN_Conn.exctCMD(cmd)

    def _FTP_connect(self):
        self._FTP_Conn = conn.FTPConn(self._host,
                                      self._FTPport,
                                      self._FTP_username,
                                      self._password,
                                      self._timeout)

    def _ftp(self):
        s.msg_out(
            self.message_output,
            '0. FTP Connecting to %s ...\n' %
            self._host)
        if self._FTP_Conn:
            connFTP = self._FTP_Conn
        else:
            self._FTP_connect()
            connFTP = self._FTP_Conn
        if connFTP:
            s.msg_out(
                self.message_output,
                '0. FTP Connected to %s.\n' %
                self._host)
            s.chg_light_to_green(self.obj_light_FTP, self.instance_light_FTP)
        else:
            s.msg_out(
                self.message_output,
                '0. FTP Connect to %s Failed!!!\n' %
                self._host)
        return connFTP

    def _telnet_write(self, str, time_out=0.5):
        str_encoded = s.encode_utf8(str)
        self._TN_Conn.Connection.write(str_encoded)
        time.sleep(time_out)

# Burn-in start,status,result
# Burn-in start
    def _put_burn_in_file(self, file_name_remote, file_name_local):
        obj_FTP = self._ftp()
        time.sleep(0.1)
        obj_FTP.PutFile(
            '/pmt',
            './IOG-3',
            file_name_remote,
            file_name_local,
            'asc')
        time.sleep(2)
        del obj_FTP
        s.chg_light_to_red(self.obj_light_FTP, self.instance_light_FTP)

    def _put_params(self):
        # Prepare test with putting 'params_new' file
        self._put_burn_in_file('params', 'params_new')

    def _put_command(self):
        # start test with putting 'command' file
        self._put_burn_in_file('command', 'command')

    def start_test(self):
        self._put_params()
        status_ready = self.get_status()
        print('---------got status', status_ready)
        if status_ready == 'Ready':
            s.msg_out(self.message_output, '    3.1 Ready to start testing.\n')
            self._put_command()
            time.sleep(2)
            status_started = self.get_status()
            if status_started == 'Testing':
                s.msg_out(self.message_output, '    3.2 Testing started.\n')
                print('Testing started.')
            else:
                print('Please check "command".')
        else:
            print('Please check "params".')


# Burn-in status

    def get_status(self):
        obj_FTP = self._ftp()
        obj_FTP.GetFile('/pmt', './IOG-3', 'status', 'status_file', 'asc')
        with open('./IOG-3/status_file') as f:
            status = f.read(10)
            print(status)
        # try:
        #     print('------begin open file')
        #     with open('./IOG-3/status_file') as f:
        #         status = f.read(10)
        #         print(status)
        # except Exception:
        #     print('Can not get status')
        s.chg_light_to_red(self.obj_light_FTP, self.instance_light_FTP)
        return status

# Burn-in result
    def _get_result_file(self):
        s.make_dir(strResultFolder)
        self.get_trace(strResultFolder, 1)
        obj_FTP = self._ftp()
        time.sleep(0.1)
        obj_FTP.GetFile('/pmt', strResultFolder, 'result', 'result')
        obj_FTP.GetFile('/pmt', strResultFolder, 'result.txt', 'result.txt')
        time.sleep(0.5)
        del obj_FTP
        s.chg_light_to_red(self.obj_light_FTP, self.instance_light_FTP)

    def get_result(self):
        status_complete = self.get_status()
        if status_complete == 'Complete':
            self._get_result_file()
            s.msg_out(self.message_output, '  5. Finish getting test result.')
        else:
            print('Test not complete, please retry later.')
            s.msg_out(
                self.message_output,
                '  ***5. Test not complete, please retry later.')
            sys.exit()
# Burn-in reset

    def reset_engine(self):
        self._executeCMD('uid 0')
        s.msg_out(
            self.message_output,
            '    6.1 Finish restoring UID Setting for engine %s.' %
            self._host)
        s.msg_out(
            self.message_output,
            '    6.2 Start Setting engine to factory default for engine %s.' %
            self._host)
        self.factory_default()
        s.msg_out(
            self.message_output,
            '    6.2 Finish Setting engine to factory default for engine %s.' %
            self._host)

# Opration to engine
# change firmware
    # @s.deco_Exception
    def change_FW(self, strFWFile):
        connFTP = self._ftp()
        time.sleep(0.25)
        connFTP.PutFile('/mbflash', './', 'fwimage', strFWFile)
        print('FW upgrade completed for {}, waiting for reboot...'.format(
            self._host))
        s.msg_out(
            self.message_output,
            '  0.1 Finish changing firmware, Rebooting...\n')
        s.chg_light_to_red(self.obj_light_telnet, self.instance_light_telnet)
        s.chg_light_to_red(self.obj_light_FTP, self.instance_light_FTP)
        s.sand_glass(45, self.message_output)

# reset to factory defaugit checkout -b dev(本地分支名称) origin/dev(远程分支名称)lt
    def factory_default(self):
        if self._TN_Conn.go_to_main_menu():
            self._telnet_write('f')
            self._TN_Conn.Connection.read_until(
                s.encode_utf8('Reset'), timeout=1)
            time.sleep(0.25)
            self._telnet_write('y')
            self._telnet_write('y')
            self._telnet_write('y')
            print('Finish restoring factory default, Reboot...\n')
            s.msg_out(
                self.message_output,
                '  0.2 Finish restoring factory default, Rebooting...\n')
            s.chg_light_to_red(
                self.obj_light_telnet,
                self.instance_light_telnet)
            s.sand_glass(20, self.message_output)

    def change_ip_address(self, new_ip_address):
        s.msg_out(
            self.message_output, '    0.3.1 changing IP from "%s" to "%s" ...\n' %
            (self._host, new_ip_address))
        print(
            'changing IP from "%s" to "%s" ...\n' %
            (self._host, new_ip_address))
        if self._TN_Conn.go_to_main_menu():
            self._telnet_write('6')
            self._TN_Conn.Connection.read_until(
                s.encode_utf8('interface'), timeout=2)
            time.sleep(0.2)
            self._telnet_write('e')
            self._telnet_write('a')
            self._TN_Conn.Connection.read_until(
                s.encode_utf8('new IP'), timeout=2)
            self._telnet_write(new_ip_address)
            self._telnet_write('\r')
            self._telnet_write('\r')

            self._TN_Conn.Connection.read_until(
                '<Enter> = done'.encode(
                    encoding="utf-8"), timeout=2)
            self._telnet_write('\r')
            # try:
            self._TN_Conn.Connection.read_until(
                s.encode_utf8('Coredump'), timeout=2)
            self._TN_Conn.Connection.write(s.encode_utf8('b'))
            self._TN_Conn.Connection.read_until(
                s.encode_utf8('Reboot'), timeout=1)
            time.sleep(0.4)
            self._TN_Conn.Connection.write(s.encode_utf8('y'))

            s.msg_out(
                self.message_output,
                '  0.3 Finish changing IP address, Rebooting...\n')
            s.chg_light_to_red(
                self.obj_light_telnet,
                self.instance_light_telnet)
            s.sand_glass(20, self.message_output)

    def change_UID(self, mode):
        if mode == 'target':
            str_uid = '0000006022112250'
        elif mode == 'initiator':
            str_uid = '0000006022112251'
        else:
            s.msg_out(self.message_output, 'failed ,check')
            sys.exit()
        uid_cmd = 'uid %s' % str_uid
        output = self._executeCMD(uid_cmd)
        if 'take full effect!' in output:
            self._executeCMD('boot')
        s.msg_out(
            self.message_output,
            '  0.4 Finish changeing UID, Rebooting...\n')
        s.sand_glass(20, self.message_output)

    def install_license(self, string_license):
        if string_license:
            lst_lsc = re.split(' |,|;', string_license)
            if len(lst_lsc) != 3:
                s.msg_out(self.message_output,
                          '    ***0.5 Please check license code\n')
                sys.exit()
            lst_lsc_id = [3, 5, 6]
            lst_lsc_desc = ['Firmware Downgrade', 'IO Generater', 'Fake Drive']
            flag_success = 0
            for i in range(len(lst_lsc)):
                # Command: "license install 3 xxxxxxx"
                cmd_lsc_install = 'license install %s %s' % (
                    str(lst_lsc_id[i]), lst_lsc[i])
                output = self._executeCMD(cmd_lsc_install)
                if 'installed' in output:
                    s.msg_out(
                        self.message_output, '    0.5.%d %s License install successful on %s.\n' % (
                            i + 1, lst_lsc_desc[i], self._host))
                    flag_success = flag_success + 1
                else:
                    s.msg_out(
                        self.message_output, '    ***0.5.%d %s License isntall failed!\n' %
                        (i + 1, lst_lsc_desc[i]))
            if flag_success == 3:
                s.msg_out(
                    self.message_output,
                    '  0.5 Finish installing licenses on %s.\n' %
                    self._host)

        else:
            s.msg_out(
                self.message_output,
                '  ***0.5 License install failed on %s.\n    Please check license code\n' %
                self._host)
            sys.exit()

    def shutdown_behaviour(self):
        if self._TN_Conn.go_to_main_menu():
            self._telnet_write('6')
            # output6 = self._TN_Conn.Connection.read_until(s.encode_utf8('seen'), timeout = 1)
            # print('------------------shutdown',output6)
            for i in range(2):
                output = self._TN_Conn.Connection.read_until(
                    s.encode_utf8('seen'), timeout=1)
                # print('------------------shutdown',output)
                if s.encode_utf8(
                        'stay up if no storage or engines seen') in output:
                    break
                else:
                    self._telnet_write('x')

            s.msg_out(
                self.message_output,
                '  0.6 Finish setting shutdown behaviour.\n')
        else:
            s.msg_out(
                self.message_output,
                '  ***0.6 Setting shutdown behaviour failed!')
            sys.exit()

    # port: 'a','b','c','d','all';mode: 'loop','point'
    def change_FC_mode(self, port, port_mode):

        def _change_mode(port, port_mode):
            time.sleep(0.25)
            tmp = self._TN_Conn.Connection.read_until(
                s.encode_utf8('<Enter> = done'), timeout=1)
            self._telnet_write(port)
            time.sleep(0.25)
            output = self._TN_Conn.Connection.read_until(
                s.encode_utf8('Default: Point-to-point mode'), timeout=1)
            print('--------output after write port\n', output)
            if port_mode == 'loop':
                if not s.encode_utf8(
                        'Current: Arbitrated loop mode') in output:
                    self._telnet_write('l')
                    # o  = self._TN_Conn.Connection.read_until(s.encode_utf8('Default: Point'), timeout = 1)
                    # print('----------\n',o)
            elif port_mode == 'point':
                if not s.encode_utf8('Current: Point-to-point mode') in output:
                    self._telnet_write('l')
                    # o = self._TN_Conn.Connection.read_until(s.encode_utf8('Default: Point'), timeout = 1)
                    # print('----------\n',o)
            self._telnet_write('\r')
            # self._TN_Conn.Connection.read_until(s.encode_utf8('Default: Point'), timeout = 1)

        if self._TN_Conn.go_to_main_menu():
            time.sleep(0.25)
            self._telnet_write('6')
            # output6 = self._TN_Conn.Connection.read_until(s.encode_utf8('Default: Point'), timeout = 1)
            # print('--------output after write 6\n',output6)
            if port == 'all':
                lst_port = ['a', 'b', 'c', 'd']
                for port in lst_port:
                    _change_mode(port, port_mode)

                    s.msg_out(
                        self.message_output,
                        '      Port %s Changed.\n' %
                        port)
            else:
                _change_mode(port, port_mode)
            self._telnet_write('\r')
            self._telnet_write('\r')
            s.msg_out(
                self.message_output,
                '  0.7 Finish changing mode of FC ports.\n')
        else:
            s.msg_out(
                self.message_output,
                '  ***0.7 Changing mode of FC ports failed.\n')
            sys.exit()

    def change_FC_speed(self, port, speed):
        def _change_speed(port, speed):
            self._telnet_write(port)
            self._telnet_write('s')
            self._telnet_write(speed)
            # output = self._TN_Conn.Connection.read_until(s.encode_utf8('Default: Point'), timeout = 1)
            # print('--------output after speed set\n',output)
            self._telnet_write('\r')

        if self._TN_Conn.go_to_main_menu():
            self._telnet_write('6')
            # output6 = self._TN_Conn.Connection.read_until(s.encode_utf8('Default: Point'), timeout = 1)
            # print('--------output after write 6\n',output6)
            if port == 'all':
                lst_port = ['a', 'b', 'c', 'd']
                for port in lst_port:
                    _change_speed(port, speed)
                    time.sleep(0.25)
                    s.msg_out(
                        self.message_output,
                        '      Port %s Changed.\n' %
                        port)
            else:
                _change_speed(port, speed)
            self._telnet_write('\r')
            s.msg_out(
                self.message_output,
                '  0.8 Finish changing speed of FC ports.\n')
        else:
            s.msg_out(
                self.message_output,
                '  ***0.8 Changing speed of FC ports failed!\n')
            sys.exit()

    def sync_time(self):
        if self.AHStatus:
            print("Engine '%s' is at AH status(AH Code %d)"
                  % (self.host, self.AHStatus))
            return

        def _exct_cmd():
            t = s.TimeNow()

            def complete_print(strDesc):
                print(
                    '    Set  %-13s for engine "%s" completed...' %
                    ('"%s"' %
                     strDesc, self._host))
                s.msg_out(
                    self.message_output,
                    '    Set  %-13s for engine "%s" completed.\n' %
                    ('"%s"' %
                     strDesc,
                     self._host))
                time.sleep(0.25)

            try:
                # Set Time
                if self._TN_Conn.exctCMD('rtc set time %d %d %d' % (
                        t.h(), t.mi(), t.s())):
                    complete_print('Time')
                    # Set Date
                    if self._TN_Conn.exctCMD('rtc set date %d %d %d' % (
                            t.y() - 2000, t.mo(), t.d())):
                        complete_print('Date')
                        # Set Day of the Week
                        DoW = t.wd() + 2
                        if DoW == 8:
                            DoW - 7
                        if self._TN_Conn.exctCMD('rtc set day %d' % DoW):
                            complete_print('Day_of_Week')
                return True
            except Exception as E:
                s.ShowErr(self.__class__.__name__,
                          sys._getframe().f_code.co_name,
                          'rtc set faild for engine "{}" with error:'.format(
                              self._host),
                          '"{}"'.format(E))
                sys.exit()

        if self._TN_Conn:
            if _exct_cmd():
                print(
                    '\nSetting time for engine "%s" completed...' %
                    self._host)
                s.msg_out(self.message_output,
                          '  0.9 Finish syncing time of engine with system.\n')
            else:
                print('\nSetting time for engine "%s" failed!!!' % self._host)
                s.msg_out(self.message_output,
                          '  ***0.9 Syncing time of engine failed.\n')

    def create_fake_drive(self):
        self._executeCMD('fake on')
        s.msg_out(self.message_output, '  1.1 Finish creating fake drives.\n')

    def mirror_and_mapping(self):
        self._executeCMD('mirror create 2044')
        self._executeCMD('map auto on')
        self._executeCMD('map 0 33281')
        s.msg_out(
            self.message_output,
            '  1.2 Finish creating mirror and mapping.\n')

    def show_mirror_and_mappting(self):
        string_to_show = ''
        string_to_show = string_to_show + self._executeCMD('mirror') + '\n'
        string_to_show = string_to_show + self._executeCMD('map') + '\n'
        s.msg_out(self.message_output, '''
  Mirror and Mapping:
  -------------------------------------------
  %s
  -------------------------------------------
              \n''' % string_to_show)

    def _register(self, lst_cmd):
        self._executeCMD('conmgr read')
        for cmd in lst_cmd:
            self._executeCMD(cmd)
            time.sleep(0.1)
        self._executeCMD('conmgr write')

    def register_initiator(self):
        # generate command
        lst_cmd = []
        lst_port = ['a1', 'a2', 'b1', 'b2']
        for i in range(len(lst_port)):
            str_cmd = 'conmgr initiator add %d %s 2%d00-006022-112251' % (
                i + 1, lst_port[i], i + 1)
            lst_cmd.append(str_cmd)

        # start registing
        self._register(lst_cmd)
        s.msg_out(
            self.message_output,
            '  1.3 Finish registering initiators.\n')

    def register_drives(self):
        # generate command
        lst_cmd = []
        lst_port = ['a1', 'a2', 'b1', 'b2']
        for i in range(len(lst_port)):
            str_cmd = 'conmgr drive add S %d %s 2%d00-006022-112250 0' % (
                i + 1, lst_port[i], i + 1)
            lst_cmd.append(str_cmd)

        # start registing
        self._register(lst_cmd)
        s.msg_out(
            self.message_output,
            '  2.1 Finish registering initiators.\n')

    def show_conmgr_status(self):
        string_to_show = self._executeCMD('conmgr status')
        s.msg_out(self.message_output, '''
  Conmgr Status:
  -------------------------------------------
  %s
  -------------------------------------------
              \n''' % string_to_show)

    # @s.deco_Exception
    def auto_commands(self, strCMDFile):
        tn = self._TN_Conn
        if self.AHStatus:
            print("Engine '%s' is at AH status(AH Code %d)"
                  % (self.host, self.AHStatus))
            return
        with open(strCMDFile, 'r') as f:
            lstCMD = f.readlines()
            for strCMD in lstCMD:
                strResult = tn.exctCMD(strCMD)
                if strResult:
                    print(strResult)
                else:
                    print('\rExecute command "{}" failed ...'.format(
                        strCMD))
                    break
                time.sleep(0.1)

    @s.deco_OutFromFolder
    def get_trace(self, strBaseFolder, intTraceLevel):
        tn = self._TN_Conn
        connFTP = self._ftp()

        def _get_oddCommand(intTraceLevel):
            oddCMD = odd()
            if intTraceLevel == 1 or intTraceLevel == 2 or intTraceLevel == 3:
                oddCMD['Trace'] = 'ftpprep trace'
                if intTraceLevel == 2 or intTraceLevel == 3:
                    oddCMD['Primary'] = 'ftpprep coredump primary all'
                    if intTraceLevel == 3:
                        oddCMD['Secondary'] = 'ftpprep coredump secondary all'
                return oddCMD
            else:
                print('Trace level must be: 1 or 2 or 3, please refer "Config.ini" ')

        def _get_trace_file(command, strTraceDes):

            # TraceDes = Trace Description
            def _get_trace_name():
                result = tn.exctCMD(command)
                reTraceName = re.compile(r'(ftp_data_\d{8}_\d{6}.txt)')
                strTraceName = reTraceName.search(result)
                if strTraceName:
                    return strTraceName.group()
                else:
                    print('Generate trace "{}" file failed for "{}"'.format(
                        strTraceDes, self._host))

            trace_name = _get_trace_name()
            if trace_name:
                time.sleep(0.1)
                local_name = 'Trace_{}_{}.log'.format(self._host, strTraceDes)
                if connFTP.GetFile('mbtrace', '.', trace_name, local_name):
                    print('Get trace "{:<10}" for "{}" completed ...'.format(
                        strTraceDes, self._host))
                    return True
                else:
                    print('Get trace "{:<10}" for engine "{}" failed!!!\
                        '.format(strTraceDes, self._host))
                #     s.ShowErr(self.__class__.__name__,
                #               sys._getframe().f_code.co_name,
                #               'Get Trace "{:<10}" for Engine "{}" Failed!!!\
                #               '.format(strTraceDes, self._host))

        oddCommand = _get_oddCommand(intTraceLevel)
        lstCommand = list(oddCommand.values())
        lstDescribe = list(oddCommand.keys())

        if s.GotoFolder(strBaseFolder):
            for i in range(len(lstDescribe)):
                try:
                    if _get_trace_file(lstCommand[i], lstDescribe[i]):
                        continue
                    else:
                        break
                except Exception as E:
                    # s.ShowErr(self.__class__.__name__,
                    #           sys._getframe().f_code.co_name,
                    #           'Get Trace "{}" Failed for Engine "{}",\
                    # Error:'.format(lstDescribe[i], self._host),
                    #           E)
                    break
                time.sleep(0.1)

    @s.deco_OutFromFolder
    def periodic_check(self, lstCommand, strResultFolder, strResultFile):
        if self.AHStatus:
            print("Engine '%s' is at AH status(AH Code %d)"
                  % (self.host, self.AHStatus))
            return
        tn = self._TN_Conn
        s.GotoFolder(strResultFolder)
        if tn.exctCMD('\n'):
            with open(strResultFile, 'w') as f:
                for strCMD in lstCommand:
                    time.sleep(0.1)
                    strResult = tn.exctCMD(strCMD)
                    if strResult:
                        print(strResult)
                        f.write(strResult)
                    else:
                        strErr = '\n*** Execute command "{}" failed\n'.format(
                            strCMD)
                        print(strErr)
                        f.write(strErr)

    def set_time(self):
        if self.AHStatus:
            print("Engine '%s' is at AH status(AH Code %d)"
                  % (self.host, self.AHStatus))
            return

        def _exct_cmd():
            t = s.TimeNow()

            def complete_print(strDesc):
                print('    Set  %-13s for engine "%s" completed...\
                        ' % ('"%s"' % strDesc, self._host))
                time.sleep(0.25)

            try:
                # Set Time
                if self._TN_Conn.exctCMD('rtc set time %d %d %d' % (
                        t.h(), t.mi(), t.s())):
                    complete_print('Time')
                    # Set Date
                    if self._TN_Conn.exctCMD('rtc set date %d %d %d' % (
                            t.y() - 2000, t.mo(), t.d())):
                        complete_print('Date')
                        # Set Day of the Week
                        DoW = t.wd() + 2
                        if DoW == 8:
                            DoW - 7
                        if self._TN_Conn.exctCMD('rtc set day %d' % DoW):
                            complete_print('Day_of_Week')
                return True
            except Exception as E:
                s.ShowErr(self.__class__.__name__,
                          sys._getframe().f_code.co_name,
                          'rtc set faild for engine "{}" with error:'.format(
                              self._host),
                          '"{}"'.format(E))

        if self._TN_Conn:
            if _exct_cmd():
                print(
                    '\nSetting time for engine "%s" completed...' %
                    self._host)
            else:
                print('\nSetting time for engine "%s" failed!!!' % self._host)
        else:
            print('\nSetting time for engine "%s" failed!!!' % self._host)


# solid_args = ('a','a','a','a','a')

# w = Action('10.203.1.175', 23, 'password',
#                  21, 'loxoll', solid_args, intTimeout=1.5)
# w.shutdown_behaviour()
# w.install_license('234234234,23424244,24224434')
# w.shutdown_behaviour()

if __name__ == '__main__':

    pass
