import os
import requests
import shutil

# trim_location = 'D:/Beat Saber/songs/new/'
trim_location = 'D:/Beat Saber/songs/2_g/'
# trim_location = 'D:/Beat Saber/songs/2_ng/'
delete_location = 'D:/Beat Saber/songs/to_delete/'


min_rating_expert_plus = 0.67
min_downloads_expert_plus = 600

min_rating_expert = 0.70
min_downloads_expert = 1000


def run_trimmer():

    if not os.path.exists(delete_location):
        os.makedirs(delete_location)

    for dirname, dirnames, filenames in os.walk(trim_location):
        for filename in filenames:
            filename_parts = filename.split(' - ', 1)
            key = filename_parts[0]

            r = requests.get('https://beatsaver.com/api/maps/detail/' + str(key))
            if r.status_code == 200:
                # print(key)
                data = r.json()

                metadata = data.get('metadata')
                difficulties = metadata.get('difficulties')
                stats = data.get('stats')
                if not ((difficulties.get('expertPlus') and stats.get('rating') > min_rating_expert_plus and stats.get(
                        'downloads') > min_downloads_expert_plus) \
                        or (difficulties.get('expert') and stats.get('rating') > min_rating_expert and stats.get(
                    'downloads') > min_downloads_expert)):
                    shutil.move(os.path.join(dirname, filename), os.path.join(delete_location, filename))

            else:
                print('Skipped '+str(key))


run_trimmer()
