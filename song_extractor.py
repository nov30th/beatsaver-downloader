import os
import shutil


location = 'D:/Beat Saber/songs/to_delete/_unzipped/'
song_location = 'D:/Beat Saber/songs/to_delete/_songs/'


def run_extractor():

    if not os.path.exists(song_location):
        os.makedirs(song_location)

    for dirname, dirnames, filenames in os.walk(location, topdown=True):

        for filename in filenames:
            if filename.endswith(('.ogg', '.egg')):
                new_name = dirname.rsplit('/', 1)[1]
                if filename.endswith(('.egg',)):
                    new_name += '.egg'
                else:
                    new_name += '.ogg'
                shutil.move(os.path.join(dirname, filename), os.path.join(song_location, new_name))


run_extractor()
