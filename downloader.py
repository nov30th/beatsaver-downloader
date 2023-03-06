from datetime import datetime, timedelta
import string
import unicodedata
import os
import dateutil.parser
import pytz
import cfscrape
import zipfile

scraper = cfscrape.create_scraper()

min_nps = 3
max_nps = 9.5
min_score_expert_plus = 0.75

days_to_stable = 14
download_location = "D:/Temp_Saber_Songs/"


def run_downloader():
    if not os.path.exists(download_location):
        os.makedirs(download_location)

    next_page = 10
    now = datetime.now(pytz.utc)
    from_date = now - timedelta(days=days_to_stable)
    until_date = None

    f = open("runs.txt", "r")
    if f.mode == "r":
        line_list = f.readlines()
        until_date = dateutil.parser.parse(line_list[-1])
    f.close()
    print("From Date: " + str(from_date))
    print("Until Date: " + str(until_date))

    while next_page is not None:
        next_page = download_from_page(next_page, from_date, until_date)

    f = open("runs.txt", "a+")
    f.write("\n")
    f.write(str(from_date))
    f.close()


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


def download_from_page(page_number, from_date, until_date):
    print("Page: " + str(page_number))
    r = scraper.get(
        "https://beatsaver.com/api/search/text/"
        + str(page_number)
        + "?sortOrder=Latest"
    )
    # r = requests.get('https://beatsaver.com/api/maps/latest/'+str(page_number))
    data = r.json()
    for doc in data.get("docs"):

        uploaded = dateutil.parser.parse(doc.get("uploaded"))
        if until_date is not None and uploaded < until_date:
            print("Until Date Reached")
            return None
        elif uploaded < from_date:
            metadata = doc.get("metadata")
            stats = doc.get("stats")

            for version in doc.get("versions"):
                difficulties = version.get("diffs")
                hasExpertPlus = contains(
                    difficulties, lambda x: x.get("difficulty") == "Expert"
                )
                if hasExpertPlus:
                    nps_expert_plus = None
                    for diff in difficulties:
                        if (
                            diff.get("difficulty")
                            and diff.get("difficulty") == "Expert"
                        ):
                            nps_expert_plus = diff.get("nps")
                            break

                    if (
                        stats.get("score") >= min_score_expert_plus
                        and nps_expert_plus >= min_nps
                        and nps_expert_plus <= max_nps
                    ):
                        filename = doc.get("id") + " - " + metadata.get("songName")
                        filename = remove_disallowed_filename_chars(filename)
                        try:
                            print(filename)
                            # file if exist
                            if os.path.isdir("D:\\SteamLibrary\\steamapps\\common\\Beat Saber\\Beat Saber_Data\\CustomLevels\\" + filename):
                                print(rf"{filename} File Exists")
                                continue
                            r_file = scraper.get(version.get("downloadURL"))
                            with open(download_location + filename + ".zip", "wb") as f:
                                f.write(r_file.content)
                            zip_file = zipfile.ZipFile(download_location + filename + ".zip")
                            zip_file.extractall("D:\\SteamLibrary\\steamapps\\common\\Beat Saber\\Beat Saber_Data\\CustomLevels\\" + filename)
                            zip_file.close()
                            os.remove(download_location + filename + ".zip")

                        except:
                            pass

    return page_number + 1


validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)


def remove_disallowed_filename_chars(filename):
    cleaned_filename = unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore")
    return "".join(chr(c) for c in cleaned_filename if chr(c) in validFilenameChars)


run_downloader()
