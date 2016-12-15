#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import subprocess
from config import config


camera_dir = config.camera_dir


class Camera(object):

    @classmethod
    def shoot(cls):
        frame_name = '.'.join((str(int(time.time())), 'jpg'))
        bash_command = 'streamer -f jpeg -s 640x480 -j 100 -o {}'.format(frame_name)
        # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        # output, error = process.communicate()
        return frame_name
