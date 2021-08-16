import os
# import requests
import csv
import cfscrape

scraper = cfscrape.create_scraper()

# check_location = 'D:/Beat Saber/songs/3_g/'
check_location = 'D:/Beat Saber/songs/5_g/'
destination_file = check_location+'check_results.csv'


def run_checker():
    array = check_values()

    csv_columns = ['key', 'name', 'uploaded', 'diff_hard', 'diff_expert', 'diff_expert_plus', 'downloads', 'up_votes', 'down_votes', 'heat', 'rating']
    try:
        with open(destination_file, 'w', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, lineterminator='\n')
            writer.writeheader()
            for data in array:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def check_values():

    array = []

    for dirname, dirnames, filenames in os.walk(check_location):
        for filename in filenames:
            filename_parts = filename.split(' - ', 1)
            key = filename_parts[0]

            r = scraper.get('https://beatsaver.com/api/maps/detail/' + str(key))
            if r.status_code == 200:
                print(key)
                data = r.json()

                item = {
                    'key': str(key),
                    'name': data['name'],
                    'uploaded': data['uploaded'],
                    'diff_hard': data['metadata']['difficulties']['hard'],
                    'diff_expert': data['metadata']['difficulties']['expert'],
                    'diff_expert_plus': data['metadata']['difficulties']['expertPlus'],
                    'downloads': data['stats']['downloads'],
                    'up_votes': data['stats']['upVotes'],
                    'down_votes': data['stats']['downVotes'],
                    'heat': data['stats']['heat'],
                    'rating': data['stats']['rating'],
                }

                array.append(item)
            else:
                print('Skipped '+str(key))

    return array


run_checker()
