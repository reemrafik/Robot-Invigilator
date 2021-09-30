from naoqi import ALProxy
import hello


def lookAtP1(ip):
    motion = ALProxy("ALMotion", ip, 9559)
    motion.setStiffnesses("HeadYaw", 1.0)
    motion.post.angleInterpolation(
        ["HeadYaw"],
        [0.4, 0.0],  # right to center
        [1, 3],
        False
    )


def lookAtP2(ip):
    motion = ALProxy("ALMotion", ip, 9559)
    motion.setStiffnesses("HeadYaw", 1.0)
    motion.post.angleInterpolation(
        ["HeadYaw"],
        [-0.2, 0.0],  # left to center
        [1, 3],
        False
    )


# # main
# ip = '169.254.228.115' # real wired
# #ip = '192.168.30.139' # real wifi
# #ip = '127.0.0.1' # virtual
# hello.say(ip,'hi')
# # lookAtP2(ip)
# # lookAtP1(ip)
