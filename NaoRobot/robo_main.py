from hello import *
from server import Server
from sound import play


ip = '169.254.228.115' # real
#ip = '127.0.0.1' # virtual


robot = Server()
robot.set_ip(ip)
#robot.set_virtual() # virtual

hello_all(ip) # real
#play('VoiceWAV/Intro-nao.wav') # virtual

while True:
    robot.start()