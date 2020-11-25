import requests
import time
import itertools

# leave the blank where the username should go as an asterisk (*)
URL_SCHEME = "https://github.com/*"

# this is the N for number of characters
NUM_CHARACTERS = 2

# to avoid getting rate-limited, this is a sleep delay between each call (in seconds)
SLEEP_DURATION = 0

# these are all the characters that you want to be allowed in the combinations
CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"

# store available username in a file, don't retry them on consecutive runs
FILENAME = "available.txt"

# if we've already checked a username we don't want to try it again
UNAVAILABLE_FILENAME = "unavailable.txt"

# generate all combinations of characters where n is the number of characters
# this returns a dictionary of the following format:
# { "aaa": False, "aab": False, ... }
def generate_combinations(n):
    combinations = {}
    list_of_characters = list(CHARS)

    for c in itertools.combinations(list_of_characters, NUM_CHARACTERS):
        combinations[''.join(c)] = False

    return combinations

def maybe_sleep():
    if SLEEP_DURATION > 0:
        time.sleep(SLEEP_DURATION)

def is_available(username):
    url_to_check = URL_SCHEME.replace("*", username)
    request = requests.get(url_to_check)
    print("checking username: {}, got status: {}".format(username, request.status_code))
    if request.status_code == 404:
        print("{} appears to be available!".format(username))
        return True
    else:
        return False

def remove_newline(line):
    return line.strip()

def get_confirmed_usernames():
    with open(FILENAME, "r") as f:
        usernames = []
        content = f.readlines()

        for c in content:
            usernames.append(c.strip())

        return usernames

def get_confirmed_unavailable():
    with open(UNAVAILABLE_FILENAME, "r") as f:
        usernames = []
        content = f.readlines()

        for c in content:
            usernames.append(c.strip())

        return usernames

def write_to_file(usernames):
    with open(FILENAME, "w") as f:
        for u in usernames:
            user_with_newline = u + "\n"
            f.write(user_with_newline)

def main():
    potential_usernames = generate_combinations(NUM_CHARACTERS)
    confirmed_usernames = get_confirmed_usernames()
    confirmed_unavailable = get_confirmed_unavailable()

    # remove any usernames that are already tested from potential_usernames
    for u in confirmed_usernames:
        try:
            potential_usernames.pop(u)
        except KeyError:
            pass

    # run main loop to check each username
    for u in potential_usernames:
        maybe_sleep()
        if is_available(u):
            confirmed_usernames.append(u)

    # write all confirmed usernames back to file
    write_to_file(confirmed_usernames)

if __name__ == "__main__":
    main()
