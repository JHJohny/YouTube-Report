import collections
import itertools
import json
import os
import re

from dateutil import parser

dir = os.getcwd() + "/Takeout/YouTube/"
watch_history = dir + "history/watch-history.html"
search_history = dir + "history/search-history.html"
comment_history = dir + "my-comments/my-comments.html"
like_history = dir + "playlists/likes.json"


class HTML:
    html_watch = open(watch_history, "r", encoding="utf-8").read()
    html_search = open(search_history, "r", encoding="utf-8").read()
    try:
        html_comment = open(comment_history, "r", encoding="utf-8").read()
    except Exception:
        print("Could not parse comments.")

    def find_links(self):
        # search all links based on your personal html file
        pattern = re.compile(r"(https://www.youtube.com/watch\?.*?)(?=\")")
        links = pattern.findall(str(HTML.html_watch))

        return links

    def _find_times(self):
        pattern = re.compile(r'(?<=<br>)([^>]*)(?=</div><div )') # Match any kind of date format
        match_list = pattern.findall(str(HTML.html_watch))

        # Format all matched dates
        times = [parser.parse(time).strftime("%d %b %Y, %H:%M:%S UTC %a") for time in match_list] # parser recognize any kind of date format

        return times

    def search_history(self):
        pattern = re.compile(r"(?<=search_query=)(.*?)(?=\">)")
        match_list = pattern.findall(str(HTML.html_search))

        search = [match.split("+") for match in match_list if "%" not in match]

        return search

    def get_commented_videos_links(self):
        pattern = re.compile(r'(?<=on <a href=\")(http://www\.youtube\.com/watch\?v=.*?)(?=\")')
        links = pattern.findall(str(HTML.html_comment))

        print(links)
        print("Links are")
        return links

    def like_history(self):
        with open(like_history, "rb") as f:
            data = json.load(f)
            pattern = re.compile(r"videoId.{15}")
            match_list = pattern.findall(str(data))
            link = r"https://www.youtube.com/watch?v=" + match_list[-1][11:]
            return link, match_list

    def dataframe_heatmap(self, day):
        time_weeks = []
        day_time = []
        times = self._find_times()
        for time in times:
            time_week = time[-3:] + time[13:15]
            time_weeks.append(time_week)
        freq = collections.Counter(time_weeks)
        for k, v in freq.items():
            if k[0:3] == day:
                day_time.append(str(k) + " " + str(v))
        day_time.sort(key=lambda x: int(str(x)[3:5]))
        print(day_time)

        zero_one = 0
        two_three = 0
        four_five = 0
        six_seven = 0
        eight_nine = 0
        ten_eleven = 0
        twelve_thirteen = 0
        fourteen_fifteen = 0
        sixteen_seventeen = 0
        eighteen_nineteen = 0
        twenty_twentyone = 0
        twentytwo_twentythree = 0
        for i in day_time:
            dt = int(i[3:5])
            if dt in range(0, 2):
                zero_one = zero_one + int(i.split(" ")[1])
            elif dt in range(2, 4):
                two_three = two_three + int(i.split(" ")[1])
            elif dt in range(4, 6):
                four_five = four_five + int(i.split(" ")[1])
            elif dt in range(6, 8):
                six_seven = six_seven + int(i.split(" ")[1])
            elif dt in range(8, 10):
                eight_nine = eight_nine + int(i.split(" ")[1])
            elif dt in range(10, 12):
                ten_eleven = ten_eleven + int(i.split(" ")[1])
            elif dt in range(12, 14):
                twelve_thirteen = twelve_thirteen + int(i.split(" ")[1])
            elif dt in range(14, 16):
                fourteen_fifteen = fourteen_fifteen + int(i.split(" ")[1])
            elif dt in range(16, 18):
                sixteen_seventeen = sixteen_seventeen + int(i.split(" ")[1])
            elif dt in range(18, 20):
                eighteen_nineteen = eighteen_nineteen + int(i.split(" ")[1])
            elif dt in range(20, 22):
                twenty_twentyone = twenty_twentyone + int(i.split(" ")[1])
            else:
                twentytwo_twentythree = twentytwo_twentythree + int(i.split(" ")[1])

        return [
            zero_one,
            two_three,
            four_five,
            six_seven,
            eight_nine,
            ten_eleven,
            twelve_thirteen,
            fourteen_fifteen,
            sixteen_seventeen,
            eighteen_nineteen,
            twenty_twentyone,
            twentytwo_twentythree,
        ]
