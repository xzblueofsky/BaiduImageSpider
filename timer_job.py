#!/usr/bin/env python

from datetime import datetime
import time
import test
import os

def timer(n):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        os.system('./haha.py')
        time.sleep(n)


timer(7200)
