import os
import string
import zipfile

import cfscrape
import requests
import unicodedata

scraper = cfscrape.create_scraper()
from multiprocessing import Pool

validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)


def remove_disallowed_filename_chars(filename):
    cleaned_filename = unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore")
    return "".join(chr(c) for c in cleaned_filename if chr(c) in validFilenameChars)


download_location = "D:/Temp_Saber_Songs/"


def download_file(download_link: str, dest_file_or_folder_name: str, song_name: str):
    r_file = requests.get(download_link)
    with open(download_location + dest_file_or_folder_name + ".zip", "wb") as f:
        f.write(r_file.content)
    zip_file = zipfile.ZipFile(download_location + dest_file_or_folder_name + ".zip")
    dest_path = "D:\\SteamLibrary\\steamapps\\common\\Beat Saber\\Beat Saber_Data\\CustomLevels\\" + dest_file_or_folder_name
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    zip_file.extractall("D:\\SteamLibrary\\steamapps\\common\\Beat Saber\\Beat Saber_Data\\CustomLevels\\" + dest_file_or_folder_name)
    zip_file.close()
    # os.remove(download_location + dest_file_or_folder_name + ".zip")
    print("Downloaded:", song_name)


def main():
    download_url = "https://bsaber.com/songs/new/page/{page}/?difficulty=expert"
    # get each page from number 15 to 200
    for page in range(15, 200):
        p = Pool(16)
        # get the page
        r = requests.get(download_url.format(page=page))
        # get the text
        text = r.text
        # find each "article" tag section in the text
        articles = text.split("<article")
        # for each article
        for article in articles:
            # find the span tag and class "post-stat" in the article html text
            if "post-stat" in article:
                # find the song name
                song_name = article.split("<h4 class=\"entry-title\" itemprop=\"name headline\">")[1].split("</a>")[0].split(">")[1]
                song_name = remove_disallowed_filename_chars(song_name)
                # find the value of "<i class='fa fa-thumbs-up fa-fw' aria-hidden='true'></i>{value}</span>"
                # and convert it to an integer
                likes = int(article.split("fa-thumbs-up fa-fw' aria-hidden='true'></i>")[1].split("</span>")[0])
                # find the unlikes value
                unlikes = int(article.split("fa-thumbs-down fa-fw' aria-hidden='true'></i>")[1].split("</span>")[0])
                if likes + unlikes > 0:
                    # calculate the ratio
                    ratio = likes / (likes + unlikes)
                    if ratio > 0.8 and likes > 10:
                        # get the download link from "<a class="action post-icon bsaber-tooltip -download-zip" href="{value}">"
                        download_link = article.split("action post-icon bsaber-tooltip -download-zip\" href=\"")[1].split("\"")[0]
                        print("Song Name:", song_name)
                        print("Download Link:", download_link)
                        key = download_link.split("/")[-1]
                        try:
                            # remove begin and end spaces from the song name
                            song_name = song_name.strip()
                            dest_file_or_folder_name = key + " " + song_name
                            # file if exist
                            if os.path.isdir("D:\\SteamLibrary\\steamapps\\common\\Beat Saber\\Beat Saber_Data\\CustomLevels\\" + dest_file_or_folder_name):
                                print(rf"{dest_file_or_folder_name} File Exists")
                                continue
                            # download the file of download_link into the download_location
                            # r_file = scraper.get(download_link)
                            p.apply_async(download_file, args=(download_link, dest_file_or_folder_name, song_name))
                            # download_file(download_link, dest_file_or_folder_name, song_name)
                        except Exception as e:
                            print("Error:", e)
                            pass
                else:
                    print("No likes or unlikes of song:", song_name)
        p.close()
        p.join()
        print("Page:", page)
    print("Done")


if __name__ == '__main__':
    main()
