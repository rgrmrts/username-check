import itertools
import random
import requests
import time


# leave the blank where the username should go as an asterisk (*)
URL_SCHEME = "https://github.com/*"

# this is the N for number of characters
NUM_CHARACTERS = 3

# to avoid getting rate-limited, this is a sleep delay between each call (in seconds)
SLEEP_DURATION = 0

# these are all the characters that you want to be allowed in the combinations
CHARS = "qwertyuiopasdfghjklzxcvbnm"

# store available username in a file, don't retry them on consecutive runs
AVAILABLE_FILENAME = "lists/available-" + str(NUM_CHARACTERS) + ".txt"

# if we've already checked a username we don't want to try it again
UNAVAILABLE_FILENAME = "lists/unavailable-" + str(NUM_CHARACTERS) + ".txt"

# generate all combinations of characters where n is the number of characters
def generate_combinations(n):
    combinations = []
    list_of_characters = list(CHARS)

    for c in itertools.combinations(list_of_characters, NUM_CHARACTERS):
        combinations.append(''.join(c))

    random.shuffle(combinations)
    return combinations

# sleep if SLEEP_DURATION is non-zero
def maybe_sleep():
    if SLEEP_DURATION > 0:
        time.sleep(SLEEP_DURATION)

# make the http request and return it's status (assumption is 404 is available)
def check_availability(username):
    url_to_check = URL_SCHEME.replace("*", username)
    print("[?] checking username '{}'".format(username))
    request = requests.get(url_to_check)
    return request.status_code

def remove_newline(line):
    return line.strip()

# read all usernames in file previously marked available
def get_available():
    with open(AVAILABLE_FILENAME, "r") as f:
        usernames = []
        file_usernames = f.readlines()

        for name in file_usernames:
            usernames.append(name.strip())

        return usernames

# read all usernames in file previously marked unavailable
def get_unavailable():
    with open(UNAVAILABLE_FILENAME, "r") as f:
        usernames = []
        file_usernames = f.readlines()

        for name in file_usernames:
            usernames.append(name.strip())

        return usernames

# write a list of usernames to file
def write_to_file(usernames, filename):
    with open(filename, "w") as f:
        for name in usernames:
            user_with_newline = name + "\n"
            f.write(user_with_newline)

def main():
    possible = generate_combinations(NUM_CHARACTERS)
    available = get_available()
    unavailable = get_unavailable()

    try:
        # remove any usernames that are already tested
        for name in available:
            try:
                possible.remove(name)
            except ValueError:
                pass

        for name in unavailable:
            try:
                possible.remove(name)
            except ValueError:
                pass

        print("-- starting to test usernames")
        print("-- tried: {}".format(len(unavailable)+len(available)))
        print("-- remaining: {}".format(len(possible)))
        # run main loop to check each username
        for name in possible:
            maybe_sleep()
            status = check_availability(name)
            if status == 404:
                print("[!] username '{}' is available".format(name))
                available.append(name)
            elif status == 200:
                unavailable.append(name)
            elif status == 429:
                print("getting rate-limited, will sleep for a bit")
                time.sleep(10)
            else:
                pass
    # mosting just catching a CTRL-C so we still update our lists
    except KeyboardInterrupt:
        print("caught a CTRL-C... exiting")

    # update list of usernames previously saved in file
    finally:
        write_to_file(available, AVAILABLE_FILENAME)
        write_to_file(unavailable, UNAVAILABLE_FILENAME)

if __name__ == "__main__":
    main()
