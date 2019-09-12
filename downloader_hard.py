import string
import unicodedata
import requests
import os
import shutil


min_rating = 0.80
min_downloads = 1000
download_location = 'D:/Beat Saber/beatsaver-downloader/files/'


def run_downloader():
    if not os.path.exists(download_location):
        os.makedirs(download_location)

    next_page = 0

    while next_page is not None:
        next_page = download_from_page(next_page)


def download_from_page(page_number):
    print('Page: '+str(page_number))
    r = requests.get('https://beatsaver.com/api/maps/latest/'+str(page_number))
    data = r.json()
    for doc in data.get('docs'):
        metadata = doc.get('metadata')
        difficulties = metadata.get('difficulties')
        stats = doc.get('stats')
        if (not difficulties.get('expert') and not difficulties.get('expertPlus')) \
                and stats.get('rating') > min_rating \
                and stats.get('downloads') > min_downloads:
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


# run_downloader()
fix_names()
