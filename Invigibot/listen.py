# source: http://people.csail.mit.edu/hubert/pyaudio/
import speech_recognition as sr
from threading import *
from client import Client
import time
import random


def action(instruction):
    invigilator = Client()
    invigilator.setInstruction(instruction)
    invigilator.start()


class Listen(Thread):
    warnings = ['I can hear you, please be quiet6',
                'Talking is not allowed7',
                'No chit chat8']

    def run(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            print('Listening...')
            audio_data = r.record(source, duration=10)
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_google(audio_data, language='en-IN', show_all=True)
            if len(text) > 0:
                heard = text['alternative'][0]['transcript']
                if 'please be quiet' in heard \
                        or 'paper' in heard \
                        or 'one please' in heard \
                        or 'two please' in heard \
                        or 'thank you' in heard \
                        or 'chit chat' in heard:
                    print("It's just the robot")
                else:
                    pick = random.randint(0,2)
                    action(self.warnings[pick])
                print('heard: ', heard)
            else:
                print('--silence--')


# main
start = time.time()
end = time.time()
while end - start < 300:
    ear = Listen()
    ear.run()
    end = time.time()
