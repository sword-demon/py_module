import socket
import optparse


class FtpClient(object):
    """ftp client"""

    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option("-s", "--server", dest="server", help="ftp server ip_addr")
        parser.add_option("-p", "--port", type="int", dest="port", help="ftp server port")
        parser.add_option("-u", "--username", dest="username", help="username info")
        parser.add_option("-p", "--password", dest="password", help="password info")
        self.options, self.args = parser.parse_args()

        print(self.options, self.args)


if __name__ == '__main__':
    client = FtpClient()
