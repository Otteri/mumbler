#!/usr/bin/env python

import signal
from threading import Thread
import subprocess
from parlai_internal.mumbler import config as cfg

MODEL = cfg.MODEL

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    # Start processes
    t1 = Thread(target=subprocess.run, args=(["python", "bot.py"], ))
    t2 = Thread(target=subprocess.run, args=(["python", "talk.py", "-t", "internal:blended_skill_talk", "-mf", MODEL],))
    t1.start()
    t2.start()

    # Wait user to kill process with Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    print("Killing threads...")
    t1.join()
    t2.join()
    print("Exiting...")
