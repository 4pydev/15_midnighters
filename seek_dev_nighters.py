#!/usr/bin/env python3

from datetime import datetime, time
import requests
import pytz


def load_attempts():
    url = 'https://devman.org/api/challenges/solution_attempts/'
    params = {
        'page': 1
    }

    while True:
        response = requests.get(url, params).json()
        page = response['page']
        number_of_pages = response['number_of_pages']
        users_attempts = response['records']
        for attempt in users_attempts:
            yield attempt
        params = {
            'page': page + 1
        }
        if page + 1 > number_of_pages: break


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
