from utils import different_frames
from mss import mss
from PIL import Image
import numpy as np
import cv2
import time
import threading
from datetime import datetime


class RecordingThread:
    def __init__(self):
        self.stopped = True
        self.screen_height = 1080
        self.screen_width = 1920

        thread = threading.Thread(target=self.start_recording, args=())
        thread.daemon = True
        thread.start()

    def start_recording(self):
        self.stopped = False
        screen_dimensions = {'top': 0, 'left': 0,
                             'width': self.screen_width, 'height': self.screen_height}
        sct = mss()
        filename = datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + '.avi'
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), 10, (self.screen_width, self.screen_height))
        last_frame = None
        frames_without_moving = 0

        while not self.stopped:
            start_time = time.time()
            sct.get_pixels(screen_dimensions)
            img = Image.frombytes(
                'RGB', (sct.width, sct.height), sct.image)
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
            # print(" RECORDING! \tFPS:", fps,
            #         "\tCurrent status:", status, end='\r')

            if frames_without_moving >= 5:
                continue

            out.write(frame)
            time.sleep(0.01)  # adds smoothness

        out.release()

    def stop_recording(self):
        self.stopped = True
