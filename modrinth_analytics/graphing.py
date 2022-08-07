import datetime
import json
import os.path
import matplotlib.pyplot as mpl
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import DateFormatter
import labrinth.user
import labrinth.projects
from xander_utils import pretty
import numpy as np


def downloads(type: str, time: str, username: str, db: str, token: str):
    if not os.path.exists(db):
        raise FileNotFoundError('Analytics file does not exist!')

    with open(db, 'r') as f:
        analytics = json.loads(f.read())

    user = labrinth.user.user(username, token)
    user_analytics = analytics[user.id]

    unfiltered_times = list(map(lambda entry: datetime.datetime.fromtimestamp(entry['time']), user_analytics))

    def get_time(t: datetime):
        diff = t - datetime.datetime(1970, 1, 1)
        match time:
            case 'hourly':
                return diff.hours
            case 'daily':
                return diff.days
            case 'weekly':
                return diff.weeks
            case 'monthly':
                return diff.months
            case 'annually':
                return diff.years

    prev_time = get_time(unfiltered_times[0])
    indexes = [0]
    for idx, date in enumerate(unfiltered_times):
        current_time = get_time(date)
        if current_time > prev_time:
            indexes.append(idx)
        prev_time = current_time
    times = [unfiltered_times[i] for i in indexes][1:]

    match type:
        case 'total':
            unfiltered_downloads = list(map(lambda entry: sum(list(entry.values())[1:]), user_analytics))
            downloads = np.diff([unfiltered_downloads[i] for i in indexes])

            mpl.plot(times, downloads)
        case 'individual':
            total_downloads = {}
            for idx, entry in enumerate(user_analytics):
                if idx not in indexes:
                    continue

                for project_id, amt in entry.items():
                    if project_id == 'time':
                        continue

                    if project_id not in total_downloads:
                        total_downloads[project_id] = [amt]
                    else:
                        total_downloads[project_id].append(amt)

            diff_downloads = {k: np.diff(v) for k, v in total_downloads.items()}

            for project_id, download_count in diff_downloads.items():
                project = labrinth.projects.project(project_id, token)
                mpl.plot(times, download_count, label=project.title)

            mpl.legend()

    mpl.gca().xaxis.set_major_formatter(DateFormatter('%d/%m/%y'))
    mpl.gcf().autofmt_xdate()
    mpl.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: pretty.human_format(x)))
    mpl.title(f'{type} downloads ({time})'.capitalize())
    mpl.xlabel('Time')
    mpl.ylabel('Downloads')
    mpl.show()
