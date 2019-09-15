from datetime import datetime, timedelta
import string
import unicodedata
import requests
import os
import shutil
import dateutil.parser
import pytz


min_rating_expert_plus = 0.67
min_downloads_expert_plus = 800

min_rating_expert = 0.70
min_downloads_expert = 1000

days_to_stable = 14
download_location = 'D:/Beat Saber/beatsaver-downloader/files/'


def run_downloader():
    if not os.path.exists(download_location):
        os.makedirs(download_location)

    next_page = 45  # Posible arrancar desde una pagina mas alta debido a los 30 dias que no se tienen en cuenta
    now = datetime.now(pytz.utc)
    from_date = now - timedelta(days=days_to_stable)
    until_date = None

    f = open("runs.txt", "r")
    if f.mode == 'r':
        line_list = f.readlines()
        until_date = dateutil.parser.parse(line_list[-1])
    f.close()
    print('From Date: ' + str(from_date))
    print('Until Date: ' + str(until_date))

    while next_page is not None:
        next_page = download_from_page(next_page, from_date, until_date)

    f = open("runs.txt", "a+")
    f.write("\n")
    f.write(str(from_date))
    f.close()


def download_from_page(page_number, from_date, until_date):
    print('Page: '+str(page_number))
    r = requests.get('https://beatsaver.com/api/maps/latest/'+str(page_number))
    data = r.json()
    for doc in data.get('docs'):

        uploaded = dateutil.parser.parse(doc.get('uploaded'))
        if until_date is not None and uploaded < until_date:
            print('Until Date Reached')
            return None
        elif uploaded < from_date:
            metadata = doc.get('metadata')
            difficulties = metadata.get('difficulties')
            stats = doc.get('stats')
            if (difficulties.get('expertPlus') and stats.get('rating') > min_rating_expert_plus and stats.get('downloads') > min_downloads_expert_plus) \
                    or (difficulties.get('expert') and stats.get('rating') > min_rating_expert and stats.get('downloads') > min_downloads_expert):
                filename = doc.get('key')+' - '+metadata.get('songName')
                filename = remove_disallowed_filename_chars(filename)
                try:
                    print(filename)
                    r_file = requests.get('https://beatsaver.com'+doc.get('downloadURL'))
                    with open(download_location+filename+'.zip', 'wb') as f:
                        f.write(r_file.content)
                except:
                    pass

    return data.get('nextPage')


validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)


def remove_disallowed_filename_chars(filename):
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(chr(c) for c in cleaned_filename if chr(c) in validFilenameChars)


def fix_names():
    for dirname, dirnames, filenames in os.walk('files'):
        for filename in filenames:
            filename_parts = filename.split(' - ', 1)
            key = filename_parts[0]
            while len(key) < 4:
                key = '0'+key

            nombre = key+' - '+filename_parts[1]
            print(nombre)
            shutil.move(os.path.join(dirname, filename), os.path.join(dirname, nombre))


run_downloader()

# fix_names()
