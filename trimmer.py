import os
import shutil
import cfscrape

scraper = cfscrape.create_scraper()

trim_location = "D:/archive/BeatSaber/new/"
delete_location = "D:/archive/BeatSaber/temp/to_delete/"

min_nps = 3
max_nps = 9.5
min_score_expert_plus = 0.75


def run_trimmer():

    if not os.path.exists(delete_location):
        os.makedirs(delete_location)

    for dirname, dirnames, filenames in os.walk(trim_location, topdown=True):

        for filename in filenames:
            filename_parts = filename.split(" - ", 1)
            key = filename_parts[0]

            r = scraper.get("https://beatsaver.com/api/maps/id/" + str(key))
            if r.status_code == 200:
                print(key)
                data = r.json()

                if should_delete(data):
                    shutil.move(
                        os.path.join(dirname, filename),
                        os.path.join(delete_location, filename),
                    )

            else:
                print("Skipped " + str(key))


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


def should_delete(data):

    if data.get("stats").get("score") < min_score_expert_plus:
        return True

    nps_expert_plus = None
    for diff in data["versions"][0]["diffs"]:
        if diff["difficulty"] and diff["difficulty"] == "ExpertPlus":
            nps_expert_plus = diff["nps"]
            break

    if nps_expert_plus and (nps_expert_plus < min_nps or nps_expert_plus > max_nps):
        return True


run_trimmer()
