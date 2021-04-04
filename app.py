from diff_frames import different_frames
from mss import mss
from PIL import Image
import numpy as np
import cv2
import time
import os


height = 1080
width = 1920
screen_dimensions = {'top': 0, 'left': 0, 'width': width, 'height': height}
sct = mss()
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (width, height))
last_frame = None
frames_without_moving = 0

os.system('cls')
print(" ")
print(" CARL v0.0.1")
print(" ===========")
print(" ")

try:
    while True:
        start_time = time.time()
        sct.get_pixels(screen_dimensions)
        img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        status = "Awake"

        if not different_frames(last_frame, frame):
            if frames_without_moving < 5:
                frames_without_moving += 1
            else:
                status = "Asleep"
        else:
            status = "Awake!"
            frames_without_moving = 0

        last_frame = frame

        fps = round(1 / (time.time() - start_time), 2)
        print(" RECORDING! \tFPS:", fps, "\tCurrent status:", status, end='\r')

        if frames_without_moving >= 5:
            continue

        out.write(frame)
        time.sleep(0.01)  # adds smoothness


except Exception as e:
    print("Finishing video!", e)
    out.release()
except:
    out.release()
