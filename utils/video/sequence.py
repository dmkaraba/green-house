#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, glob, json
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, ImageSequenceClip
from configer import ConfigCreator, ConfigDefaults


class SequenceProcessing(object):

    def __init__(self):
        config = ConfigCreator()
        config_default = ConfigDefaults()
        for i in ['PATH', 'STAMP_LOGO']:
            if config.get_value(i):
                setattr(self, i, config.get_value(i))
            else:
                setattr(self, i, getattr(config_default, i))

    def make_stamp(self, task_id):
        '''
        stamps all frames in specified sequence
        :param sequenceFolder: frames folder
        :param shotNumber: number to be stamped on each frame
        :return:
        '''
        task = self._find_task(task_id)
        sequence_folder = task['sequence_path']
        stamp_shot_number = os.path.split(task['scene_path'])[-1].split('.')[0]
        stamp_shot_version = os.path.split(task['scene_path'])[-1].split('.')[1]
        # stamp_focal_length = json.load(open(os.path.join(self.PATH, stamp_shot_number, 'shotInfo.json')))['focalLength']
        # frames = os.listdir(sequence_folder)
        # stamp_logo = ImageClip(str(self.STAMP_LOGO), transparent=True)
        # for frame in frames:
        #     if os.path.splitext(frame)[-1] in ['.jpeg']:
        #         image = ImageClip(str(os.path.join(sequence_folder, frame)))
        #         stamp_frame_number = frame.split('.')[1]
        #         txt_clip1 = TextClip(stamp_shot_number, color='white', fontsize=20)
        #         txt_clip2 = TextClip('version: {}'.format(stamp_shot_version[1:]), color='white', fontsize=15)
        #         txt_clip3 = TextClip('frame: {}'.format(stamp_frame_number), color='white', fontsize=15)
        #         txt_clip4 = TextClip('focalLength: {}'.format(stamp_focal_length), color='white', fontsize=15)
        #         result = CompositeVideoClip([image, txt_clip1.set_position((5, 5)),
        #                                      txt_clip2.set_position((5, 25)),
        #                                      txt_clip3.set_position((5, 40)),
        #                                      txt_clip4.set_position((5, 55)),
        #                                      stamp_logo.set_position(("left", "bottom"))])
        #         result.save_frame(os.path.join(sequence_folder, frame))
        print 'STAMP#################'
        print stamp_shot_number, stamp_shot_version, self.STAMP_LOGO, self.PATH
        print '######################'

    def make_video(self, task_id):
        '''
        makes video file from specified frame folder
        :param sequenceFolder: frames folder
        :param shotNumber: number for naming the resulting video file
        :return:
        '''
        task = self._find_task(task_id)
        sequence_folder = task['sequence_path']
        sequence_frames = glob.glob(os.path.join(sequence_folder, '*.jpeg'))
        stamp_shot_number = os.path.split(task['scene_path'])[-1].split('.')[0]
        # clip = ImageSequenceClip(sequence_frames, fps=25)
        # if not os.path.exists(os.path.join(self.PATH, 'videos')):
        #     os.mkdir(os.path.join(self.PATH, 'videos'))
        # clip.write_videofile(os.path.join(self.PATH, 'mov', stamp_shot_number+'.mp4'), fps=25)
        print 'VIDEO#################'
        print sequence_folder, sequence_frames[0], stamp_shot_number, self.PATH
        print '######################'

    def _find_task(self, task_id):
        tasks_data = os.path.join(os.path.dirname(sys.argv[0]), 'config/renderData.json')
        tasks = json.load(open(tasks_data))
        for task in tasks:
            if task['id'] == task_id:
                return task
