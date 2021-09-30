import socket
from threading import *
from time import sleep


class Client(Thread):
    instruction = ''

    def setInstruction(self, i):
        self.instruction = i

    def getInstruction(self):
        return self.instruction

    def run(self):
        c = socket.socket()
        print('client socket created')
        c.connect(('localhost', 1234))
        msg = self.getInstruction()
        c.sendall(bytes(msg, 'utf-8'))
        message = c.recv(1024).decode()
        if len(message) > 0:
            print(message)
        c.close()
        sleep(0.3)
