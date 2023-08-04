#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Author  : Nov30th, HOHO``
import json

import pytube

# finds all the "cinema-video.json" in D:\SteamLibrary\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels and it's sub folders
file_name = "cinema-video.json"
folder = "D:\\SteamLibrary\\steamapps\\common\\Beat Saber\\Beat Saber_Data\\CustomLevels\\"
import os


def find_all(name, path):
    # including sub folders
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))

    # only current folder
    # for file in os.listdir(path):
    #     if os.path.isfile(os.path.join(path, file)) and name == file:
    #         result.append(os.path.join(path, file))
    return result


for folder in find_all(file_name, folder):
    # read the json file
    with open(folder, "r", encoding="utf-8") as f:
        try:
            # convert the json content
            json_content: dict = json.loads(f.read())
            video_id = json_content["videoID"]
            if "videoFile" not in json_content:
                video_file = json_content["title"]
            else:
                video_file = json_content["videoFile"]
            print(folder, video_id, video_file)
            full_path_of_folder = os.path.dirname(folder)

            # if file exist full_path_of_folder + video_file
            if os.path.isfile(full_path_of_folder + "\\" + video_file):
                print(rf"{video_file} File Exists")
                # check if file larger than 1MB
                if os.path.getsize(full_path_of_folder + "\\" + video_file) > 1024 * 1024:
                    print(rf"{video_file} File Exists and Larger than 1MB")
                    continue

            # download the video using pytube
            url = "https://www.youtube.com/watch?v=" + video_id
            print(rf"Downloading: {url}, to {full_path_of_folder}")
            yt = pytube.YouTube(url, use_oauth=True,
                                allow_oauth_cache=True)
            stream = yt.streams.get_highest_resolution()
            stream.download(full_path_of_folder, video_file)
            break_here = True
        except Exception as e:
            print(folder)
            print("Error:", e)
            pass
