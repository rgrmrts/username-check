import itertools
import random
import requests
import time

from queue import Queue
from threading import Thread


# leave the blank where the username should go as an asterisk (*)
URL_SCHEME = "https://github.com/*"

# this is the N for number of characters
NUM_CHARACTERS = 3

# to avoid getting rate-limited, this is a sleep delay between each call (in seconds)
SLEEP_DURATION = 0.15

# these are all the characters that you want to be allowed in the combinations
CHARS = "qwertyuiopasdfghjklzxcvbnm"

# store available username in a file, don't retry them on consecutive runs
AVAILABLE_FILENAME = "available.txt"

# if we've already checked a username we don't want to try it again
UNAVAILABLE_FILENAME = "unavailable.txt"

# generate all combinations of characters where n is the number of characters
def generate_combinations(n):
    combinations = []
    list_of_characters = list(CHARS)

    for c in itertools.combinations(list_of_characters, NUM_CHARACTERS):
        combinations.append(''.join(c))

    random.shuffle(combinations)
    return combinations

def maybe_sleep():
    if SLEEP_DURATION > 0:
        time.sleep(SLEEP_DURATION)

def check_availability(username):
    url_to_check = URL_SCHEME.replace("*", username)
    request = requests.get(url_to_check)
    return request.status_code

def remove_newline(line):
    return line.strip()

def get_available():
    with open(AVAILABLE_FILENAME, "r") as f:
        usernames = []
        content = f.readlines()

        for c in content:
            usernames.append(c.strip())

        return usernames

def get_unavailable():
    with open(UNAVAILABLE_FILENAME, "r") as f:
        usernames = []
        content = f.readlines()

        for c in content:
            usernames.append(c.strip())

        return usernames

def write_to_file(usernames, filename):
    with open(filename, "w") as f:
        for u in usernames:
            user_with_newline = u + "\n"
            f.write(user_with_newline)

def main():
    possible = generate_combinations(NUM_CHARACTERS)
    available = get_available()
    unavailable = get_unavailable()

    try:
        # remove any usernames that are already tested
        for u in available:
            try:
                possible.remove(u)
            except ValueError:
                pass

        for u in unavailable:
            try:
                possible.remove(u)
            except ValueError:
                pass

        # run main loop to check each username
        for u in possible:
            maybe_sleep()
            status = check_availability(u)
            if status == 404:
                print("> the username '{}' is available!".format(u))
                available.append(u)
            elif status == 200:
                unavailable.append(u)
            elif status == 429:
                print("getting rate-limited, will sleep for a bit")
                time.sleep(7)
                possible.append(u)  # adding this to the end of the list to retry later
            else:
                pass
    except KeyboardInterrupt:
        print("caught a CTRL-C... exiting")
    finally:
        # write all confirmed usernames back to files
        write_to_file(available, AVAILABLE_FILENAME)
        write_to_file(unavailable, UNAVAILABLE_FILENAME)

if __name__ == "__main__":
    main()
