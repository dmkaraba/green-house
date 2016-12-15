#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import subprocess
from config import config


camera_dir = config.camera_dir


class Camera(object):

    @classmethod
    def shoot(cls):
        frame_name = '.'.join((str(int(time.time())), 'jpg'))
        frame_dir = os.path.join(camera_dir, frame_name)
        print frame_dir
        bash_command = 'streamer -f jpeg -s 640x480 -j 100 -o {}'.format(frame_dir)
        # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        # output, error = process.communicate()
        return frame_name
