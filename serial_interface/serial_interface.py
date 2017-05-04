"""The serial interface bet"""

import sys
import glob
import serial
import subprocess

class SerialConnection(object):
    def __init__(self, port="COM5", rate=9600):
        self.port = port
        self.baud_rate = rate

    def list_available_ports(self):
        data = subprocess.check_output(["python", "-m", "serial.tools.list_ports"])
        print data

    def connect(self):
        try:
            self.connection = serial.Serial()
            self.connection.port = self.port
            self.connection.baudrate = self.baud_rate
            self.connection.open()
        except OSError, serial.SerialException:
            raise Exception("failed to connect to port")

    def read(self, bytes= 8):
        if not self.connection.is_open:
            raise Exception("The serial interface is no longer connected")
        else:
            data = self.connection.read(bytes)
            return data

    def write(self, data):
        if not data:
            raise Exception("No data to write!")
        elif not self.connection.is_open:
            raise Exception("No connection is currently open")

        else:
            self.connection.write(data)

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    s = SerialConnection()
    