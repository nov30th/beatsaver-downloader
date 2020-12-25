import os
import requests
import shutil
import cfscrape

scraper = cfscrape.create_scraper()

trim_location = 'D:/Beat Saber/songs/new/'
delete_location = 'D:/Beat Saber/songs/to_delete/_n/'
# trim_location = 'D:/Beat Saber/songs/to_delete/_a/'
# delete_location = 'D:/Beat Saber/songs/to_delete/_g/'


min_rating_expert_plus = 0.75
# min_downloads_expert_plus = 800

# min_rating_expert = 0.85
# min_downloads_expert = 2500


def run_trimmer():

    if not os.path.exists(delete_location):
        os.makedirs(delete_location)

    for dirname, dirnames, filenames in os.walk(trim_location, topdown=True):

        # for filename in filenames:
        #     if filename.endswith(('.ogg', '.egg')):
        #         new_name = dirname.rsplit('/', 1)[1]
        #         if filename.endswith(('.egg',)):
        #             new_name += '.egg'
        #         else:
        #             new_name += '.ogg'
        #         shutil.move(os.path.join(dirname, filename), os.path.join(delete_location, new_name))

        for filename in filenames:
            filename_parts = filename.split(' - ', 1)
            key = filename_parts[0]

            r = scraper.get('https://beatsaver.com/api/maps/detail/' + str(key))
            if r.status_code == 200:
                # print(key)
                data = r.json()

                metadata = data.get('metadata')
                difficulties = metadata.get('difficulties')
                stats = data.get('stats')

                if not difficulties.get('expertPlus') or stats.get('rating') < min_rating_expert_plus:
                    shutil.move(os.path.join(dirname, filename), os.path.join(delete_location, filename))

            else:
                print('Skipped '+str(key))


run_trimmer()
