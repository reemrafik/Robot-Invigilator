import socket
from threading import *
from time import sleep
from hello import *
from move import *
from sound import play


class Server(Thread):
    s = socket.socket()
    instruction = ''
    print('server socket created')
    s.bind(('localhost', 1234))
    s.listen(3)
    print('server waiting for connections')
    ip = ''
    virtual = False
    sounds = ['Calibrate', 'Start', 'Papers',
              'Your paper', 'Peeking', 'Warned',
              'Quiet', 'Talking', 'Chitchat', 'Thank you']
    talk = False

    # sets ip to be used
    def set_ip(self, ip_address):
        self.ip = ip_address

    # change robot type to virtual
    def set_virtual(self):
        self.virtual = True

    def set_flag(self):
        self.talk = True

    def get_flag(self):
        return self.talk

    def run(self):
        while True:
            c, addr = self.s.accept()
            print('Connected with', addr)
            instruction = c.recv(1024).decode()
            if len(instruction) > 0:
                instruction = str(instruction)
                i = int(instruction[-1])
                print('instruction from client: ', instruction)
                if instruction[0:2] == 'P1':
                    lookAtP1(self.ip)
                    if self.virtual:
                        play('VoiceWAV/Participant1.wav')
                    instruction = 'Participant 1'+instruction[2:]
                elif instruction[0:2] == 'P2':
                    lookAtP2(self.ip)
                    if self.virtual:
                        play('VoiceWAV/Participant 2.wav')
                    instruction = 'Participant 2'+instruction[2:]
                instruction = instruction[:-1]
                say(self.ip, str(instruction))
                if self.virtual:
                    filename = 'VoiceWAV/'+self.sounds[i]+'.wav'
                    play(filename)
                    print('play sound: ', filename)
            c.close()
            sleep(0.3)