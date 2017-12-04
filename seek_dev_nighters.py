#!/usr/bin/env python3

from datetime import datetime, time
import requests
import pytz


def load_attempts():
    url = 'https://devman.org/api/challenges/solution_attempts/'
    pages = requests.get(url, ).json()['number_of_pages']
    for page in range(1, pages+1):
        params = {
            'page': page
            }
        users_attempts = requests.get(url, params).json()['records']
        for attempt in users_attempts:
            yield attempt


def is_midnighter(user_attempt):
    user_time_zone = user_attempt['timezone']
    user_utc_datetime = datetime.fromtimestamp(user_attempt['timestamp'])
    user_local_time = pytz.timezone(
        user_time_zone).fromutc(user_utc_datetime).time()
    return True if time(5, 0, 0) > user_local_time > time(0, 0, 0) else False


def get_midnighters():
    owl_users = set()
    for attempt in load_attempts():
        if is_midnighter(attempt):
            owl_users.add(attempt['username'])
    return owl_users


if __name__ == '__main__':
    for counter, user in enumerate(get_midnighters()):
        print('{} : {}'.format(counter, user))
