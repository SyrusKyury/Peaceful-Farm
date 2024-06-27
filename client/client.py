from concurrent.futures import ThreadPoolExecutor
import requests
import os
import time
import re


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
    # Have fun!
    # -------------------------------------------------------------------------

    # Don't touch this, it will return only valid flags
    return set([i for i in flags if re.match(FLAG_REGEX, i)])


#------------------------------------------------------------------------------
# Peaceful Farm settings
#------------------------------------------------------------------------------
SERVER_IP = "127.0.0.1"
SERVER_PORT = "5000"
NICKNAME = os.getenv('USER') or os.getenv('USERNAME')
API_KEY = "1234567890"

#------------------------------------------------------------------------------
# Exploit settings
#------------------------------------------------------------------------------
N_TEAMS = 41
TEAM_ID = 39
NOP_TEAM_ID = 0
FLAG_REGEX = r"[A-Z0-9]{31}="
SUBMIT_TIME = 30

#------------------------------------------------------------------------------
# Exploit function
#------------------------------------------------------------------------------

SERVICE = "Example"    # Service you're exploiting
EXPLOIT = "Peaceful Farm"    # Name of your exploit

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
    target_ip_list = [f"10.60.0.{i}" for i in range(N_TEAMS, 0, -1) if i != NOP_TEAM_ID and i != TEAM_ID]

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