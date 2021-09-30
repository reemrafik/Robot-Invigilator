import cv2 as cv
import mediapipe as mp
import time
from client import Client
import numpy as np

# face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

# draw circles on specific landmarks for each participant
def circle_landmarks(frame, x1, y1, x2, y2):
    cv.circle(frame, (x1, y1), 2, (0, 255, 0), -1)
    cv.circle(frame, (x2, y2), 2, (0, 255, 0), -1)

def annotate_img(frame):
    rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    res = face_mesh.process(rgb_img)
    h, w, _ = frame.shape
    dz_p = 0.0

    if res.multi_face_landmarks:
        for facial_landmarks in res.multi_face_landmarks:
            pt1 = facial_landmarks.landmark[247]
            x1 = int(pt1.x * w)
            y1 = int(pt1.y * h)
            z1 = pt1.z * 1000
            pt2 = facial_landmarks.landmark[467]
            x2 = int(pt2.x * w)
            y2 = int(pt2.y * h)
            z2 = pt2.z * 1000
            circle_landmarks(frame, x1, y1, x2, y2)
            dz_p = z2 - z1
    return frame, dz_p

def calibrate():
    vid = cv.VideoCapture(0, cv.CAP_DSHOW)
    # initialize maximum and minimum difference in z coordinates for each participant
    min_dz_p1 = 100000
    max_dz_p1 = 0
    min_dz_p2 = 100000
    max_dz_p2 = 0

    start = time.time()
    end = time.time()
    while end - start < 5:
        ret, whole = vid.read()
        if not ret:
            break
        h, w, _ = whole.shape

        # split image in half
        img1 = whole[0:h, 0:int(w / 2)]
        img2 = whole[0:h, int(w / 2): w]

        # annotate facial landmarks and obtain
        # difference in z-coordinates for each participant
        img1, p1_dz = annotate_img(img1)
        img2, p2_dz = annotate_img(img2)

        # compare obtained z-coordinates to existing min and max
        # and update for participant 1
        if p1_dz < min_dz_p1:
            min_dz_p1 = p1_dz
        elif p1_dz > max_dz_p1:
            max_dz_p1 = p1_dz

        # compare obtained z-coordinates to existing min and max
        # and update for participant 2
        if p2_dz < min_dz_p2:
            min_dz_p2 = p2_dz
        elif p2_dz > max_dz_p2:
            max_dz_p2 = p2_dz

        # join the 2 half images again
        cal = np.concatenate((img1, img2), axis=1)
        cv.imshow('calibrate', cal)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        end = time.time()
    cv.destroyAllWindows()
    bound_p1 = [min_dz_p1, max_dz_p1]
    bound_p2 = [min_dz_p2, max_dz_p2]
    return bound_p1, bound_p2

def monitor(bound_p1, bound_p2, video_path):
    vid = cv.VideoCapture(0, cv.CAP_DSHOW)
    fourcc = cv.VideoWriter_fourcc('X', 'V', 'I', 'D')
    video_writer = cv.VideoWriter(video_path, fourcc, 30, (640, 480))
    frames1 = 0
    peek1 = 0
    warn1 = 0

    frames2 = 0
    peek2 = 0
    warn2 = 0

    fps = 30
    frame_limit = int(1*fps)
    peek_limit = 3

    # start timer for task
    start = time.time()
    end = time.time()

    while end - start < 300:
        ret, whole = vid.read()
        if not ret:
            break

        h, w, _ = whole.shape
        img1 = whole[0:h, 0:int(w / 2)]
        img2 = whole[0:h, int(w / 2): w]

        img1, p1_dz = annotate_img(img1)
        img2, p2_dz = annotate_img(img2)

        direction1, action_chk1 = get_direction(bound_p1, p1_dz, 1)
        direction2, action_chk2 = get_direction(bound_p2, p2_dz, 2)
        action_chk = [action_chk1, action_chk2]
        warned = [warn1, warn2]

        action = get_action(action_chk, warned)
        show_direction(img1, direction1, 1, peek1, warn1)
        show_direction(img2, direction2, 2, peek2, warn2)

        if action_chk1:
            frames1 += 1
            if frames1 == frame_limit:
                peek1 += 1
                frames1 = 0
                if peek1 % peek_limit == 0:
                    do_action(action)
                    warn1 += 1
                    if action == 'Please look at your own papers3':
                        warn2 += 1
        elif action_chk2:
            frames2 += 1
            if frames2 == frame_limit:
                peek2 += 1
                frames2 = 0
                if peek2 % peek_limit == 0:
                    do_action(action)
                    warn2 += 1
        mon = np.concatenate((img1, img2), axis=1)
        show_action(mon, action)
        cv.imshow('monitor', mon)
        video_writer.write(mon)
        if cv.waitKey(30) & 0xFF == ord('q'):
            break
        end = time.time()
    vid.release()
    video_writer.release()
    cv.destroyAllWindows()

def get_direction(bound_p, p_dz, p_num):
    action_chk = False
    direction = ''

    if p_num == 1:
        if p_dz > bound_p[1]:
            direction = 'left'
            action_chk = True
        elif p_dz < bound_p[0]:
            direction = 'right'
        else:
            direction = 'center'
    elif p_num == 2:
        if p_dz > bound_p[1]:
            direction = 'left'
        elif p_dz < bound_p[0]:
            direction = 'right'
            action_chk = True
        else:
            direction = 'center'

    return direction, action_chk

def get_action(action_chk, warned):
    action = ''
    if action_chk[0]:
        if action_chk[1]:
            action += 'Please look at your own papers2'
        else:
            if warned[0] == 0:
                action += 'P1, please look at your paper3'
            elif warned[0] % 3 == 0:
                action += 'P1, I have warned you several times already5'
            elif warned[0] % 2 == 0:
                action += 'P1, no peeking4'
            else:
                action += 'P1, please look at your paper3'

    elif action_chk[1]:
        if warned[1] == 0:
            action += 'P2, please look at your paper3'
        elif warned[1] % 3 == 0:
            action += 'P2, I have warned you several times already5'
        elif warned[1] % 2 == 0:
            action += 'P2, no peeking4'
        else:
            action += 'P2, please look at your paper3'

    return action

def do_action(action):
    invigilator = Client()
    invigilator.setInstruction(action)
    invigilator.start()
    print('Action: ', action)

def show_direction(img, direction, p_num, peek, warn):
    h, w, _ = img.shape
    if p_num == 1:
        pos_dir = (int(w * 0.1), int(h * 0.1))
        cv.putText(img, 'P1 ' + direction, pos_dir, 0, 1, (255, 0, 0))
        pos_p = (int(w * 0.1), int(h * 0.15))
        cv.putText(img, 'Peeks: ' + str(peek), pos_p, 0, 0.5, (0, 0, 255))
        pos_w = (int(w * 0.1), int(h * 0.2))
        cv.putText(img, 'Warned: ' + str(warn), pos_w, 0, 0.5, (0, 0, 255))
    elif p_num == 2:
        pos = (int(w * 0.4), int(h * 0.1))
        cv.putText(img, 'P2 ' + direction, pos, 0, 1, (255, 0, 0))
        pos_p = (int(w * 0.4), int(h * 0.15))
        cv.putText(img, 'Peeks: ' + str(peek), pos_p, 0, 0.5, (0, 0, 255))
        pos_w = (int(w * 0.4), int(h * 0.2))
        cv.putText(img, 'Warned: ' + str(warn), pos_w, 0, 0.5, (0, 0, 255))

def show_action(img, action):
    h, w, _ = img.shape
    cv.putText(img, action[:-1], (int(w * 0.03), int(h * 0.8)), 0, 0.7, (255, 0, 0))





