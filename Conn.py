# coding:utf-8

from ftplib import FTP
import telnetlib
import sys
import re
import Sundry as s


class FTPConn(object):
    def __init__(self, strIP, intPort, strUser, strPWD, intTO):
        self._host = strIP
        self._port = intPort
        self._username = strUser
        self._password = strPWD
        self._timeout = intTO
        self._connected = None
        self._logined = None
        self._Connection = None
        # self._FTPconnect()

    def _FTPconnect(self):
        ftp = FTP()

        def _conn():
            try:
                ftp.connect(self._host, self._port, self._timeout)
                self._connected = ftp
                print("FTP Connect Success")
                return True
            except Exception as E:
                s.ShowErr(self.__class__.__name__,
                          sys._getframe().f_code.co_name,
                          'FTP connect to "{}" failed with error:'.format(
                              self._host),
                          '"{}"'.format(E))

        def _login():
            try:
                ftp.login(self._username, self._password)
                self._logined = ftp
                print("FTP Login Success")
                return True
            except Exception as E:
                # print(E)
                s.ShowErr(self.__class__.__name__,
                          sys._getframe().f_code.co_name,
                          'FTP login to "{}" failed with error:'.format(
                              self._host),
                          '"{}"'.format(E))

        if _conn():
            if _login():
                self._Connection = ftp
                return True

    def GetFile(self, strRemoteFolder, strLocalFolder, strRemoteFileName,
                strLocalFileName, FTPtype='bin', intBufSize=1024):
        def _getfile(strRemoteFolder, strLocalFolder, strRemoteFileName,
                     strLocalFileName):
            # try:
            ftp = self._Connection
            # print(ftp.getwelcome())
            ftp.cwd(strRemoteFolder)
            file_path_name = '%s/%s' % (strLocalFolder, strLocalFileName)
            if FTPtype == 'asc':
                ftp.retrlines(
                    'RETR %s' %
                    strRemoteFileName,
                    open(
                        file_path_name,
                        'w').write)
            elif FTPtype == 'bin':
                ftp.retrbinary(
                    'RETR %s' %
                    strRemoteFileName,
                    open(
                        file_path_name,
                        'wb').write)
            # with open(file_path_name, "wb") as f:
            #     if FTPtype == 'bin':
            #         ftp.retrbinary('RETR {}'.format(strRemoteFileName),f.write)
            #     elif FTPtype == 'asc':
            #         ftp.retrlines(b'RETR %s' % strRemoteFileName, f.write)
            ftp.cwd('/')
            return True
            # except Exception as E:
            #     s.ShowErr(self.__class__.__name__,
            #               sys._getframe().f_code.co_name,
            #               'FTP download "{}" failed with error:'.format(
            #                   self._host),
            #               '"{}"'.format(E))

        if self._Connection:
            if _getfile(strRemoteFolder, strLocalFolder, strRemoteFileName,
                        strLocalFileName):
                return True
        else:
            if self._FTPconnect():
                if _getfile(strRemoteFolder, strLocalFolder, strRemoteFileName,
                            strLocalFileName):
                    return True

    def PutFile(self, strRemoteFolder, strLocalFolder, strRemoteFileName,
                strLocalFileName, FTPtype='bin', intBufSize=1024):
        def _putfile():
            # try:
            ftp = self._Connection
            # ftp.set_pasv(0)
            # print(ftp.getwelcome())
            ftp.cwd(strRemoteFolder)

            file_path_name = '%s/%s' % (strLocalFolder, strLocalFileName)
            print('--------', file_path_name)
            print('---------r', strRemoteFileName)
            if FTPtype == 'asc':
                with open(file_path_name, 'rb') as f:
                    ftp.storlines('STOR %s' % strRemoteFileName, f)
            elif FTPtype == 'bin':
                ftp.storbinary(
                    'STOR %s' %
                    strRemoteFileName, open(
                        file_path_name, 'rb'))

            # except Exception as E:
            #     s.ShowErr(self.__class__.__name__,
            #               sys._getframe().f_code.co_name,
            #               'FTP upload "{}" failed with error:'.format(
            #                   self._host),
            #               '"{}"'.format(E))

        if self._Connection:
            if _putfile():
                return True
        else:
            if self._FTPconnect():
                if _putfile():
                    return True

    def close(self):
        print("FTP Close")
        if self._Connection:
            self._Connection.quit()
            self._Connection = None


class HAAPConn(object):
    def __init__(self, strIP, intPort, strPWD, intTO):
        self._host = strIP
        self._port = intPort
        self._password = strPWD.encode(encoding="utf-8")
        self._timeout = intTO
        self._strLoginPrompt = 'Enter password'.encode(encoding="utf-8")
        self._strMainPrompt = 'HA-AP'.encode(encoding="utf-8")
        self._strCLIPrompt = 'CLI>'.encode(encoding="utf-8")
        self._strAHPrompt = 'AH_CLI>'.encode(encoding="utf-8")
        self._strCLIConflict = 'Another session owns the CLI'.encode(
            encoding="utf-8")
        self.Connection = None
        self.telnet_connect()

    def _connect(self):
        # try:
        objTelnetConnect = telnetlib.Telnet(
            self._host, self._port, self._timeout)
        objTelnetConnect.read_until(self._strLoginPrompt, timeout=2)
        objTelnetConnect.write(self._password)
        objTelnetConnect.write(b'\r')

        objTelnetConnect.read_until(
            self._strMainPrompt, timeout=1)
        self.Connection = objTelnetConnect
        return True
        # except Exception as E:
        #     s.ShowErr(self.__class__.__name__,
        #               sys._getframe().f_code.co_name,
        #               'Telnet connect to "{}" failed with error:'.format(
        #                   self._host),
        #               '"{}"'.format(E))

    def _connect_retry(self):
        if self.Connection:
            return True
        else:
            print('Connect retry for engine "%s" ...' % self._host)
            self._connect()

    def telnet_connect(self):

        if not self._connect():
            self._connect_retry()

    def get_connection_status(self):
        if self.Connection:
            return True
        else:
            return False

    def is_AH(self):
        strPrompt = self.exctCMD('')
        if strPrompt:
            if self._strAHPrompt in s.encode_utf8(strPrompt):
                strVPD = self.exctCMD('vpd')
                reAHNum = re.compile(r'Alert:\s*(\d*)')
                objReAHNum = reAHNum.search(strVPD)
                return int(objReAHNum.group(1))
            else:
                return 0

    def go_to_main_menu(self):
        self.Connection.write(b'\r')
        output = self.Connection.read_until(self._strMainPrompt, timeout=2)
        if self._strCLIPrompt in output:
            self.Connection.write(b'exit')
            self.Connection.write(b'\r')
            self.Connection.write(b'\r')
            self.Connection.write(b'\r')
            output_exit = self.Connection.read_until(
                self._strMainPrompt, timeout=1)
            # if s.encode_utf8('Configuration Conflicts\r\nOwner is session') in output_exit
            # print('--------------------exit\n',output_exit)
            if self._strMainPrompt in output_exit:
                return True
        elif self._strMainPrompt in output:
            return True

    def go_to_CLI(self):
        self.Connection.write(b'\r')
        output = self.Connection.read_until(self._strCLIPrompt, timeout=1)
        if self._strCLIPrompt in output:
            return True
        elif self._strMainPrompt in output:
            self.Connection.write(s.encode_utf8('7'))
            str7Output = self.Connection.read_until(
                self._strCLIPrompt, timeout=1)
            if self._strCLIPrompt in str7Output:
                return True
            elif self._strCLIConflict in str7Output:
                self.Connection.write(s.encode_utf8('y'))
                strConfirmCLI = self.Connection.read_until(
                    self._strCLIPrompt, timeout=1)
                if self._strCLIPrompt in strConfirmCLI:
                    return True

            # except Exception as E:
            #     print('No need to reboot')
            # self.Connection.close()

    def exctCMD(self, strCommand):
        if self.Connection:
            if self.go_to_CLI():
                self.Connection.write(
                    strCommand.encode(encoding="utf-8") + b'\r')
                strResult = str(self.Connection.read_until(
                    self._strCLIPrompt, timeout=2).decode())
                if self._strCLIPrompt.decode() in strResult:
                    return strResult

    def Close(self):
        if self.Connection:
            self.Connection.close()

    connection = property(
        get_connection_status, doc="Get HAAPConn instance's connection")

# w = HAAPConn('10.203.1.175', 23, 'password', 2)
# w.install_license()


if __name__ == '__main__':

    pass
