import naoqi
from naoqi import ALProxy


def hello_all(ip):
    tts = ALProxy("ALTextToSpeech", ip, 9559)
    tts.say("Hello participants!")
    tts.say("I will be monitoring you today, while you complete a short quiz.")
    tts.say("You will notice, there are four lines of tape on the table.")
    tts.say("Two for each participant.")
    tts.say("In a moment I will ask you to look from left to right")
    tts.say("The tape lines indicate the maximum left and right positions")
    tts.say("which you should swivel your head between")
    tts.say("You will then start a 5 minute quiz")
    tts.say("I will let you know when time is up")
    tts.say("Finally, good luck!")

def say(ip, talk):
    tts = ALProxy("ALTextToSpeech", ip, 9559)
    tts.say(talk)