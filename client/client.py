from concurrent.futures import ThreadPoolExecutor
import requests
import os
import time
import re
import random
import string

#------------------------------------------------------------------------------
# Exploit function
#------------------------------------------------------------------------------
# ATTENTION
# EDIT THEESE PARAMETERS TO MATCH THE SERVICE YOU'RE EXPLOITING
# THIS INFORMATION WILL BE USED TO RECORD STATISTICS ON THE SERVER

SERVICE = "Example"             # Service you're exploiting
EXPLOIT = "Peaceful Farm"       # Name of your exploit

def exploit(target_ip : str) -> list[str]:
    flags = set()

    # -------------------------------------------------------------------------
    # Your exploit here
    # -------------------------------------------------------------------------
    # Example:
    # response = requests.get(f"http://{target_ip}/flag")
    # flag = response.text
    # flags.add(flag)
    # -------------------------------------------------------------------------
    # Useful functions:
    # - generate_random_string  Generates a random string of a given length
    # - random_napolify         Generates a random string with a Napoli theme
    # -------------------------------------------------------------------------
    # Have fun!
    # -------------------------------------------------------------------------

    # Don't touch this, it will return only valid flags
    return set([i for i in flags if re.match(FLAG_REGEX, i)])

#------------------------------------------------------------------------------
# Peaceful Farm settings
#------------------------------------------------------------------------------
SERVER_IP = "127.0.0.1"         # Peaceful Farm server IP
SERVER_PORT = "5000"            # Peaceful Farm server port
API_KEY = "1234567890"          # Peaceful Farm API key
NICKNAME = os.getenv('USER') or os.getenv('USERNAME') or "Peaceful Farmer"

#------------------------------------------------------------------------------
# Competition settings
#------------------------------------------------------------------------------
N_TEAMS = 41                    # Number of teams in the competition
TEAM_ID = 39                    # Your team ID
NOP_TEAM_ID = 0                 # Team ID of the NOP team
FLAG_REGEX = r"[A-Z0-9]{31}="   # Regex to validate flags
SUBMIT_TIME = 30                # How often to submit flags to the server

#------------------------------------------------------------------------------
# Don't touch anything below this line
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Utility functions
#------------------------------------------------------------------------------

def generate_random_string(length : int, include_symbols=False, valid_set=string.ascii_letters + string.digits):
    r"""
    Generate a random string of a given length.
    length: int, the length of the string to generate.
    include_symbols: bool, whether to include symbols in the string.
    valid_set: str, the set of characters to choose from.
    """
    ascii_chars = valid_set
    if include_symbols:
        ascii_chars += string.punctuation

    random_string = "".join(random.choice(ascii_chars) for _ in range(length))
    return random_string


def random_leet(text: str, prob : float = 0.5, stronger : bool = False) -> str:
    r"""
    Randomly apply leet transformations to a string.
    text: str, the text to transform.
    prob: float, the probability of transforming a character.
    stronger: bool, whether to apply stronger leet transformations (uses non-alphanumeric characters instead of numbers).
    """

    leet_map = {
        "a" : ["4", "@"],
        "b" : ["8"],
        "c" : ["c", "(", "{"],
        "d" : ["d"],
        "e" : ["3"],
        "f" : ["f"],
        "g" : ["6"],
        "h" : ["h"],
        "i" : ["1", "!", "|"],
        "j" : ["j"],
        "k" : ["k"],
        "l" : ["l", "1", "|", "I"],
        "m" : ["m"],
        "n" : ["n"],
        "o" : ["0"],
        "p" : ["p"],
        "q" : ["q"],
        "r" : ["r"],
        "s" : ["5", "$"],
        "t" : ["7"],
        "u" : ["u"],
        "v" : ["v"],
        "w" : ["w"],
        "x" : ["x"],
        "y" : ["y"],
        "z" : ["z", "2"]
    }

    res = ""
    for char in text:
        entry = char
        if random.random() < prob:
            entry = entry.lower()
        else:
            entry = entry.upper()

        if random.random() < prob:
            entry = leet_map.get(entry.lower(), entry)
            if isinstance(entry, list):
                if stronger:
                    entry = random.choice(entry)
                else:
                    entry = entry[0]

        res += entry

    return res


def random_napolify(length : int, blacklist : str = "", stronger_leet = False) -> str:
    r"""
    Generate a random string with a Napoli theme.
    length: int, the length of the string to generate.
    blacklist: str, a string containing characters to avoid in the output.
    stronger_leet: bool, whether to apply stronger leet transformations.
    """
    sentences = [
        "forza napoli sempre",
        "il ciuccio vola",
        "staro con te",
        "un giorno all improvviso",
        "victor osimhen",
        "dries mertens",
        "lorenzo insigne",
        "jose maria callejon",
        "marek hamsik",
        "edinson cavani",
        "maradona",
        "diego",
        "san paolo",
        "kvicha kvaratskhelia",
        "tifa napoli",
        "ciccio bello tifa napoli",
        "forza napoli",
        "napoli",
        "capitan di lorenzo",
        "giovanni di lorenzo",
        "diego armando maradona",
        "ezequiel lavezzi",
        "christian maggio",
        "paolo cannavaro",
        "rispetta il ciuccio",
        "napoli rules torino",
        "napoli capitale",
        "luciano spalletti",
        "mario rui",
        "il maestro mario rui",
        "Alessio Zerbin",
        "coca cola",
        "bevi cocacola napoletana",
        "il ciuccio",
        "pulcinella",
        "goku con la maglia del napoli",
        "napoli e il napoli",
        "napoli napoli napoli",
        "chi non salta juventino e",
        "Pizza",
        "Mandolino",
        "Vesuvio",
        "San Gennaro",
        "O sole mio",
        "Napoli e",
        "Pino Daniele",
        "Toto",
        "Tarantella",
        "margherita",
        "ragu",
        "kalidou",
        "koulibaly",
        "azzurri",
        "partenopei",
        "scudetto"
    ]

    sentences = [i for i in sentences if len(i) + 1 <= length]

    if len(sentences) == 0:
        return generate_random_string(length)

    spacing = random.choice(["-", "_", "~", ".", ","])
    sentences = [i.replace(" ", spacing) + spacing for i in sentences]

    random_sentence = random_leet(random.choice(sentences), prob=0.5, stronger=stronger_leet)
    if len(random_sentence) > length:
        random_sentence = random_sentence[:length]
    elif len(random_sentence) < length:
        random_sentence += generate_random_string(length - len(random_sentence))

    for char in blacklist:
        random_sentence = random_sentence.replace(char, random.choice(string.ascii_letters))

    return random_sentence

#------------------------------------------------------------------------------
# Submit flags
#------------------------------------------------------------------------------

def submit_flags(flags : list[str]):
    if not flags:
        return
    
    json = {
        "api_key": API_KEY,
        "flags": list(flags),
        "exploit": EXPLOIT,
        "service": SERVICE,
        "nickname": NICKNAME
    }
    response = requests.post(f"http://{SERVER_IP}:{SERVER_PORT}/flags", json=json)
    print(f"Server: {response.text}")

#------------------------------------------------------------------------------
# Main function
#------------------------------------------------------------------------------

if __name__ == '__main__':
    # Generate target ip list
    target_ip_list = [f"10.60.{i}.1" for i in range(N_TEAMS, 0, -1) if i != NOP_TEAM_ID and i != TEAM_ID]

    futures = []
    flags = set()
    now = time.time()
    with ThreadPoolExecutor() as pool:
        try:
            while True:
                for _ in target_ip_list[:]:
                    target_ip = target_ip_list.pop()
                    target_ip_list.insert(0, target_ip)
                    #if a thread with target_ip is already running, skip
                    for future, ip in futures:
                        if ip == target_ip:
                            if future.done():
                                flags = flags.union(future.result())
                                futures.remove((future, ip))
                            else:
                                break
                    else:
                        futures.append((pool.submit(exploit, target_ip), target_ip))

                if time.time() - now > SUBMIT_TIME:
                    submit_flags(flags)
                    flags = set()
                    now = time.time()

        except KeyboardInterrupt:  # CTRL+C
            try:
                print(f"\n\nCompleting running threads...")
                pool.shutdown(wait=True, cancel_futures=True)
            except KeyboardInterrupt:
                print(f"\nSubmitting flags before you kill me...")
            finally:
                print(f"\nSubmitting flags")
                submit_flags(flags)
                exit(0)