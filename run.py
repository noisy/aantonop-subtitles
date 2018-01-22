import re
from collections import defaultdict
from glob import glob


languages = set()
videos = {}

for filepath in glob("./subtitles/original/*"):
    filename = filepath.replace("./subtitles/original/", "")
    title, youtube_id, lang = re.match(r"(.*)-(.{11,13})\.(.*)\.vtt", filename).groups()

    languages.add(lang)

    if title not in videos:
        videos[youtube_id] = {
            "title": title,
            "subtitles": [{"lang": lang, "filepath": filepath}]
        }

    else:
        videos[youtube_id]["subtitles"].append({{"lang": lang, "filepath": filepath}})


    print(filename)


headers = ["No.", "Title"] + list(languages)
langs = list(languages)

print("|", end="")
for header in ["No.", "Title"] + langs:
    print(" <sup><sub>{}</sub></sup> |".format(header), end="")
print("")

print("|", end="")
for i in range(len(headers)):
    print("----|", end="")
print("")


def multiline_split(str, char_per_line):
    words = str.split(" ")

    result = ""
    line = ""
    for word in words:
        if len(line + word) < char_per_line:
            line += " " + word
        else:
            result += line + "<br>"
            line = word

    result += line

    return result

lang_stat = defaultdict(int)

for i, (youtube_id, video) in enumerate(videos.items()):
    print("| <sup><sub>{}</sub></sup> |".format(i+1), end="", flush=True)
    print(" <sup><sub>[{title}]({youtube_link})</sub></sup> |".format(
        title=multiline_split(video["title"], 25),
        youtube_link="https://www.youtube.com/watch?v={}".format(youtube_id)
    ), end="", flush=True)

    for lang in langs:

        if lang in [sub["lang"] for sub in video["subtitles"]]:
            print(" <sup><sub>✓</sub></sup> |", end="", flush=True)
            lang_stat[lang] += 1
        else:
            print(" |", end="", flush=True)

    print("")

print("")
