from client import Client
from video_pair_split import calibrate
from video_pair_split import monitor


invigilator = Client()
invigilator.setInstruction('Please look straight then left to right.0')
invigilator.start()

invigilator.join()
bound_p1, bound_p2 = calibrate()
print('left: ', bound_p1[0], ' ', bound_p1[1])
print('right: ', bound_p2[0], ' ', bound_p2[1])

invigilator = Client()
invigilator.setInstruction('Thank you, now you can start your task. You have 5 minutes!1')
invigilator.start()

# appointment number
app_num = '14'

# 1 or 2 indicating first or second task for the same appointment
test_num = '1'

# v or r for virtual or real robot
bot_type = 'r'

video_path = 'Videos/Study'+app_num+test_num+bot_type+'.avi'

invigilator.join()
monitor(bound_p1, bound_p2, video_path)

invigilator = Client()
invigilator.setInstruction('All done, thank you for participating.9')
invigilator.start()