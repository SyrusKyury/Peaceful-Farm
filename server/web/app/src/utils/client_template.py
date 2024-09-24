from concurrent.futures import ThreadPoolExecutor
import requests
import os
import time
import re
import random
import string

#------------------------------------------------------------------------------
# Exploit settings
#------------------------------------------------------------------------------
# ATTENTION
# EDIT THEESE PARAMETERS TO MATCH THE SERVICE YOU'RE EXPLOITING
# THIS INFORMATION WILL BE USED TO RECORD STATISTICS ON THE SERVER
#------------------------------------------------------------------------------
# Service you're exploiting
SERVICE = "Example"
# Name of your exploit
EXPLOIT = "%s"

# -------------------------------------------------------------------------
# Set this to True to test your exploit on the NOP team.
# This will not submit flags to the server and will only print
# the extracted flags.
# -------------------------------------------------------------------------
DEBUG = False                   
VERBOSE_EXCEPTIONS = False

def exploit(target_ip : str, exploit_data : any = None) -> list:
    flags = set()

    # -------------------------------------------------------------------------
    # Your exploit here
    # -------------------------------------------------------------------------
    # Example:
    # response = requests.get(f"http://{target_ip}/flag")
    # flag = response.text
    # flags.add(flag)
    # -------------------------------------------------------------------------
    # Parameters:
    # - target_ip: str, the IP of the target service
    # - exploit_data: any data you want to reuse to attack the target ip.
    #         For example, if you need to keep a session, you can store it here.
    #         If you want to reuse the same account, you can store the credentials here.
    #
    # Useful functions:
    # 
    # - generate_random_string 
    #   Generates a random string of a given length
    #   Arguments:
    #       length: int, the length of the string to generate
    #       include_symbols: bool, whether to include symbols in the string
    #       valid_set: str, the set of characters to choose from
    #
    # - random_napolify         
    #   Generates a random string with a Napoli theme
    #   Arguments:
    #       length: int, the length of the string to generate
    #       blacklist: str, a string containing characters to avoid in the output
    #       stronger_leet: bool, whether to apply stronger leet transformations
    #
    # -------------------------------------------------------------------------
    # Have fun!
    # -------------------------------------------------------------------------

    # Don't touch this, it will return only valid flags
    return target_ip, set([i for i in flags if re.match(r"%s", i)]), exploit_data

#------------------------------------------------------------------------------
# Peaceful Farm settings
#------------------------------------------------------------------------------
# Peaceful Farm server IP
SERVER_IP = "%s"
# Peaceful Farm server port
SERVER_PORT = "%s"
# Peaceful Farm API key
API_KEY = "%s"
# How often the client should submit flags to Peaceful Farm server
SUBMIT_TIME = int("%s")
# How oftein the client should attack the targets
ATTACK_TIME = int("%s")
# Your nickname (your OS username will be used as default)
NICKNAME = os.getenv('USER') or os.getenv('USERNAME') or "Peaceful Farmer"

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

def submit_flags(flags : dict[str, set]):
    if len(flags) == 0:
        print("No flags to submit")
        return
    
    for key, value in flags.items():
        flags[key] = list(value)
    
    json = {
        "api_key": API_KEY,
        "flags": flags,
        "exploit": EXPLOIT,
        "service": SERVICE,
        "nickname": NICKNAME
    }

    max_attempts = 5
    
    for i in range(max_attempts):
        try:
            response = requests.post(f"http://{SERVER_IP}:{SERVER_PORT}/flags", json=json)
            print(f"Server: {response.text}")
            return
        except Exception as e:
            if VERBOSE_EXCEPTIONS:
                print(f"Error submitting flags: {e}")
            else:
                print(f"Error submitting flags to the Peaceful Farm server")
            print(f"DO NOT CLOSE THE CLIENT! The flags will be stored in a backup file after {str(max_attempts - i)} more attempts")
            print(f"Retrying in 5 seconds...")
            time.sleep(5)
    
    print(f"Could not submit flags after {max_attempts} attempts")
    now = time.time()
    print(f"The obtained flags will be stored in a file named flags_{EXPLOIT}_{SERVICE}_{now}.txt")
    with open(f"flags_{EXPLOIT}_{SERVICE}_{now}.txt", "w") as f:
        for key, value in flags.items():
            for flag in value:
                f.write(f"{key},{flag}\n")
    exit(1)


#------------------------------------------------------------------------------
# Load backup if exists
#------------------------------------------------------------------------------

def load_backup():
    print("Checking for backup files...")
    files = [i for i in os.listdir() if os.path.isfile(i) and i.startswith(f"flags_{EXPLOIT}_{SERVICE}")]
    if len(files) == 0:
        print("No backup files found")
        return
    
    print(f"Found {len(files)} backup files")
    
    choice = input("Do you want to load the backup files? [y/n] ").lower()
    if choice != "y":
        return

    flags = dict()
    for f in files:
        print(f"Loading backup file {f}...")
        line = open(f).read().split("\n")
        n = 0
        for l in line:
            if not l:
                continue
            ip, flag = l.split(",")
            if ip not in flags:
                flags[ip] = set()
            flags[ip].add(flag)
            n += 1
        print(f"Loaded {n} flags")
    
    submit_flags(flags)

#------------------------------------------------------------------------------
# Get targets
#------------------------------------------------------------------------------

def get_targets():
    print("Getting the list of target machines...")
    try:
        response = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/targets")
        print(f"Found {len(response.json())} target machines")
        return response.json()
    except Exception as e:
        if VERBOSE_EXCEPTIONS:
            print(f"Error getting targets: \n{e}")
        else:
            print(f"Error getting the list of target machines. Check your connection to the Peaceful Farm server.")
        print("Exiting...")
        exit(1)

#------------------------------------------------------------------------------
# Get NOP team ID
#------------------------------------------------------------------------------
def get_nop():
    try:
        response = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/nop")
        return response.json()[0]
    except Exception as e:
        if VERBOSE_EXCEPTIONS:
            print(f"Error getting NOP team: \n{e}")
        else:
            print("Error getting NOP team. Check your connection to the Peaceful Farm server.")
        print("Exiting...")
        exit(1)

#------------------------------------------------------------------------------
# Banner
#------------------------------------------------------------------------------
banner = """
 __   ___       __   ___  ___               ___       __        
|__) |__   /\\  /  ` |__  |__  |  | |       |__   /\\  |__)  |\\/| 
|    |___ /~~\\ \\__, |___ |    \\__/ |___    |    /~~\\ |  \\  |  | 
                                                                
                   __          ___      ___                     
                  /  ` |    | |__  |\\ |  |                      
                  \\__, |___ | |___ | \\|  |                      
                                                                
"""


#------------------------------------------------------------------------------
# Main function
#------------------------------------------------------------------------------

if __name__ == '__main__':

    if DEBUG:
        print("Exploited flags from NOP team:\n{extracted_flags}".format(extracted_flags=exploit(get_nop())))
        exit(0)
    
    print(banner)
    load_backup()
    target_list = get_targets()

    flags = dict()
    now = time.time()
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [(pool.submit(exploit, ip, None), ip) for ip in target_list]
        try:
            while True:
                completed_futures = list(filter(lambda x: x[0].done(), futures))
                futures = list(filter(lambda x: not x[0].done(), futures))
                
                for future, ip in completed_futures:
                    target_ip, extracted_flags, exploit_data = future.result()
                    if extracted_flags:
                        flags[target_ip] = extracted_flags if target_ip not in flags else flags[target_ip].union(extracted_flags)
                    futures.append((pool.submit(exploit, target_ip, exploit_data), target_ip))

                time.sleep(ATTACK_TIME)

                if time.time() - now > SUBMIT_TIME:
                    submit_flags(flags)
                    flags = dict()
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