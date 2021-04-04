import os
from recording_thread import RecordingThread
import threading


def main():
    recording_thread = RecordingThread()

    while True:
        command = input(" Command: \t")
        if command == "help":
            print("Type in 'stop' to stop recording")
        
        if command == "stop":
            recording_thread.stop_recording()
            break

if __name__ == '__main__':
    os.system('cls')
    print(" ")
    print(" CARL v0.0.1")
    print(" ===========")
    print(" ")
    
    main()
