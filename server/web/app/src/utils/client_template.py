import threading, queue, requests, os, time, re, random, string

#------------------------------------------------------------------------------
# QUICK START
#------------------------------------------------------------------------------
# Welcome to the Peaceful Farm client! Write your exploit in the exploit
# function below. Also DON'T FORGET to set the SERVICE constant to the name of
# the service you are exploiting. This helps the server to identify the service
# you are attacking and to store the flags correctly. 
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS
#------------------------------------------------------------------------------

# Enable verbose debug messages for detailed output during execution.
# Set to True to enable detailed logs, or False to disable them.
VERBOSE_DEBUG: bool = False

# Configure exploit settings for team attacks.
# Choose the target of the attack:
# 0: Attack the nop team (to test your exploit before spoiling to the other teams)
# 1: Attack your own team (to test if you fixed the vulnerability you're exploiting)
# 2: Attack your opponents (to get and submit the flags)
EXPLOIT_DEBUG: int = 2

# The name of the service being exploited.
SERVICE: str = "Example"

# The name of the exploit being used.
EXPLOIT = "%s"


def exploit(target_ip : str, exploit_data : any = None) -> set[str]:
    try:
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
        #         If you want to reuse the same account, you can store the credentials 
        #         here etc.
        #
        # -------------------------------------------------------------------------
        #
        # Useful functions:
        # 
        # - Utils.random_string 
        #   Generates a random string of a given length
        #   Arguments:
        #       length: int, the length of the string to generate
        #       valid_set: str, the set of characters to choose from
        #   Returns:
        #       str: the generated string
        #
        # - Utils.flagids         
        #   Returns the challenge's flag ids. Flag ids provide useful
        #   information to exploit services. For example, they can be
        #   usernames, ids, or any other information.
        #   Arguments:
        #       None
        #   Returns:
        #       dict: the challenge's flag ids
        #
        # -------------------------------------------------------------------------
        # Have fun!
        # -------------------------------------------------------------------------

    except:
        # You can handle exceptions here. Please don't let your exploit crash,
        # this would stop the attack for that target. If you want to ignore the
        # exception, just use the pass statement.
        pass

    finally:
        # Don't touch this, it will return only valid flags
        return set(filter(lambda f: re.match(FLAG_REGEX, f), flags))


#------------------------------------------------------------------------------
# CONSTANTS
#------------------------------------------------------------------------------
# The following constants are set by the server. You can modify them if needed
# but it is not recommended.

# Peaceful Farm server IP
SERVER_IP = "%s"

# Peaceful Farm server port
SERVER_PORT = "%s"

# Peaceful Farm API key
API_KEY = "%s"

# How often the client should submit flags to Peaceful Farm server
SUBMIT_TIME = int("%s")

# Flag regex
FLAG_REGEX = r"%s"

# Your nickname (your OS username will be used as default)
NICKNAME = os.getenv('USER') or os.getenv('USERNAME') or "Peaceful Farmer"

# Maximum number of retries when submitting flags
MAX_RETRIES_FOR_SUBMISSION = 3

# Time to wait before submitting flags again after a failure
RETRY_TIME = 3

# Iteration time for exploit threads. When the thread doesn't find any flags
# it kills itself
SUICIDE_COUNTDOWN : int = 10

# How often the attacks are performed
ATTACK_TIME : int = int("%s")

# How often the threads' health is checked
HEALT_CHECK_TIME : int = 5

#------------------------------------------------------------------------------
# Colors
#------------------------------------------------------------------------------

YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
SKY = "\033[96m"
RESET = "\033[0m"

#------------------------------------------------------------------------------
# Exploit Thread Class
#------------------------------------------------------------------------------

class ExploitThread(threading.Thread):

    def __init__(self, target_ip : str, queue : queue.Queue, stop_event : threading.Event):
        super().__init__()
        self.target_ip = target_ip
        self.exploit_data = None
        self.queue = queue
        self.stop_event = stop_event

    def run(self):
        suicide_countdown : int = SUICIDE_COUNTDOWN

        while suicide_countdown > 0 and not self.stop_event.is_set():
            flags = exploit(self.target_ip, self.exploit_data)
            if len(flags) > 0:
                self.queue.put((self.target_ip, flags))
                suicide_countdown = SUICIDE_COUNTDOWN
            else:
                suicide_countdown -= 1
            time.sleep(ATTACK_TIME)

        
        if suicide_countdown == 0:
            print(f"{RED}[FAIL] [Thread {self.target_ip}] Exiting due to the lack of new flags{RESET}")
        else:
            print(f"{GREEN}[SUCCESS] [Thread {self.target_ip}] Exiting due to EXIT signal{RESET}")

#------------------------------------------------------------------------------
# Submission Manager Class
#------------------------------------------------------------------------------

class SubmissionManager(threading.Thread):


    def __init__(self, queue : queue.Queue, stop_flag_submission : threading.Event, backup_manager : 'BackupManager'):
        super().__init__()
        self.stop_flag_submission = stop_flag_submission
        self.backup_manager = backup_manager
        self.exploit_data = None
        self.flags = dict()
        self.queue = queue


    def run(self):
        while not self.stop_flag_submission.is_set():
            time.sleep(SUBMIT_TIME)
            self.get_data_from_queue()
            self.try_to_submit_flags()

        if EXPLOIT_DEBUG == 1 or EXPLOIT_DEBUG == 0:
            return
        
        print(f"{GREEN}[SUCCESS] [Submission service] Sending the last flags before exiting due to EXIT signal{RESET}")
        self.get_data_from_queue()
        if len(self.flags) > 0:
            self.try_to_submit_flags()


    def try_to_submit_flags(self):
        if EXPLOIT_DEBUG == 1 or EXPLOIT_DEBUG == 0:
            print(f"{YELLOW}[WARNING] [Submission service] Debug mode enabled, flags will not be submitted{RESET}")
            return
        # Load data from backup if it exists
        if self.backup_manager.backup_enabled:
            data = self.backup_manager.load_data()
            for key, value in data.items():
                self.flags[key] = self.flags[key].union(value) if key in self.flags.keys() else value

        for i in range(MAX_RETRIES_FOR_SUBMISSION):
            try:
                self.submit_flags()
                return
            except Exception as e:
                if VERBOSE_DEBUG:
                    print(f"{RED}[FAIL] [Submission service], try {str(i+1)}: {e}{RESET}")
                else:
                    print(f"{RED}[FAIL] [Submission service] Failed to submit flags, try {str(i+1)}{RESET}")
                
                print(f"{RED}[FAIL] [Submission service] Could not submit flags to the Peaceful Farm server{RESET}")
                print(f"{YELLOW}[WARNING] [Submission service] Retrying in 5 seconds{RESET}")
                time.sleep(RETRY_TIME)
        
        if self.backup_manager.backup_enabled:
            self.backup_manager.save_data(self.flags)
            self.flags.clear()
            print(f"{YELLOW}[WARNING] [Submission service] Flags saved to backup{RESET}")
        


    def get_data_from_queue(self):
        current_queue_size = self.queue.qsize()
        for _ in range(current_queue_size):
            data = self.queue.get()
            self.flags[data[0]] = self.flags[data[0]].union(data[1]) if data[0] in self.flags.keys() else data[1]

    
    def submit_flags(self):
        if len(self.flags) == 0:
            print(f"{YELLOW}[WARNING] [Submission service] No flags to submit{RESET}")
            return
        
        for key, value in self.flags.items():
            self.flags[key] = list(value)
        
        json = {
            "api_key": API_KEY,
            "flags": self.flags,
            "exploit": EXPLOIT,
            "service": SERVICE,
            "nickname": NICKNAME
        }

        response = requests.post(f"http://{SERVER_IP}:{SERVER_PORT}/flags", json=json)
        print(f"{SKY}[SERVER] {response.text}{RESET}")
        self.flags.clear()
        return
        
#------------------------------------------------------------------------------
# Client Class
#------------------------------------------------------------------------------     

class Client:


    def __init__(self, targets : list[str], backup_manager : 'BackupManager') -> None:
        self.targets = targets
        self.backup_manager = backup_manager
        self.threads = []
        self.flags_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.stop_flag_submission = threading.Event()


    def start(self):
        for t in self.targets:
            thread = ExploitThread(t, self.flags_queue, self.stop_event)
            thread.start()
            self.threads.append(thread)

        self.threads.append(SubmissionManager(self.flags_queue, self.stop_flag_submission, self.backup_manager))
        self.threads[-1].start()

    
    def stop(self):
        self.stop_event.set()
        for t in self.threads[:-1]:
            t.join()
        
        self.stop_flag_submission.set()
        self.threads[-1].join()


    def healt_check(self):
        if [t.is_alive() for t in self.threads[:-1]].count(True) == 0:
            return False, "All exploit threads are dead"
        
        if not self.threads[-1].is_alive():
            return False, "Submission service is dead"
        
        return True, "System is healthy"


#------------------------------------------------------------------------------
# Custom Exception
#------------------------------------------------------------------------------


class HealtException(Exception):
    pass


#------------------------------------------------------------------------------
# Backup Manager Class
#------------------------------------------------------------------------------


class BackupManager:


    def __init__(self) -> None:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        self.backup_directory = os.path.join(current_directory, "backup_" + EXPLOIT + "_" + SERVICE)
        self.backup_file_base = "backup_"
        self.backup_enabled = False


    def create_backup_directory(self) -> bool:
        try:
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
            self.backup_enabled = True
            return True
        except Exception as e:
            if VERBOSE_DEBUG:
                print(f"{RED}[FAIL] [Backup Manager] Failed to create backup directory: {e}{RESET}")
            else:
                print(f"{RED}[FAIL] [Backup Manager] Failed to create backup directory{RESET}")
            return False
        
    
    def save_data(self, data : dict) -> bool:
        if not self.backup_enabled:
            return False
        
        try:
            files = [f for f in os.listdir(self.backup_directory) if self.backup_file_base in f]
            backup_file = self.backup_file_base + str(len(files))
            with open(os.path.join(self.backup_directory, backup_file), "w") as f:
                for target, list in data.items():
                    for flag in list:
                        f.write(f"{target}:::{flag}\n")
            return True
        
        except Exception as e:
            if VERBOSE_DEBUG:
                print(f"{RED}[FAIL] [Backup Manager] Failed to save data: {e}{RESET}")
            else:
                print(f"{RED}[FAIL] [Backup Manager] Failed to save data{RESET}")
            return False
        

    def load_data(self) -> dict[str, list[str]]:
        if not self.backup_enabled:
            return dict()
        
        try:
            files = [f for f in os.listdir(self.backup_directory) if self.backup_file_base in f]
            if len(files) == 0:
                return dict()
            
            data = dict()
            for f in files:
                with open(os.path.join(self.backup_directory, f), "r") as file:
                    for line in file:
                        if len(line) > 0:
                            target, flag = line.replace("\n", "").split(":::")
                            if target in data.keys():
                                data[target].append(flag)
                            else:
                                data[target] = [flag]
            
            # Remove backup files
            for f in files:
                os.remove(os.path.join(self.backup_directory, f))
            return data
        
        except Exception as e:
            if VERBOSE_DEBUG:
                print(f"{RED}[FAIL] [Backup Manager] Failed to load data: {e}{RESET}")
            else:
                print(f"{RED}[FAIL] [Backup Manager] Failed to load data{RESET}")
            return dict()
        

    def save_file(self, filename : str, data : str) -> bool:
        if not self.backup_enabled:
            return False
        
        try:
            with open(os.path.join(self.backup_directory, filename), "w") as f:
                f.write(data)
            return True
        except Exception as e:
            if VERBOSE_DEBUG:
                print(f"{RED}[FAIL] [Backup Manager] Failed to save file: {e}{RESET}")
            else:
                print(f"{RED}[FAIL] [Backup Manager] Failed to save file{RESET}")
            return False
        

    def load_file(self, filename : str) -> str:
        if not self.backup_enabled:
            return ""
        
        try:
            with open(os.path.join(self.backup_directory, filename), "r") as f:
                return f.read()
        except Exception as e:
            if VERBOSE_DEBUG:
                print(f"{RED}[FAIL] [Backup Manager] Failed to load file: {e}{RESET}")
            else:
                print(f"{RED}[FAIL] [Backup Manager] Failed to load file{RESET}")
            return ""
                
        
#-------------------------------------------------------------------------------
# Target Manager Class
#-------------------------------------------------------------------------------

class TargetManager:

    def __init__(self, backup_manager : 'BackupManager') -> None:
        self.backup_manager = backup_manager
    
    def get_targets(self):
        for i in range(MAX_RETRIES_FOR_SUBMISSION):
            try:
                response = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/targets", json={"api_key": API_KEY})
                if self.backup_manager.backup_enabled:
                    self.backup_manager.save_file("targets", "\n".join(response.json()))
                return response.json()
            except Exception as e:
                if VERBOSE_DEBUG:
                    print(f"{RED}[FAIL] [Targets] try {str(i+1)}: {e}{RESET}")
                else:
                    print(f"{RED}[FAIL] [Targets] Failed to get targets, try {str(i+1)}{RESET}")
                time.sleep(RETRY_TIME)
        
        if self.backup_manager.backup_enabled:
            print(f"{YELLOW}[WARNING] [Targets] Loading targets from backup{RESET}")
            data = self.backup_manager.load_file("targets")
            if data != "":
                return list(filter(lambda t : len(t) > 0, data.split("\n")))
        return []


    def get_nop(self):
        for i in range(MAX_RETRIES_FOR_SUBMISSION):
            try:
                response = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/nop", json={"api_key": API_KEY})
                if self.backup_manager.backup_enabled:
                    self.backup_manager.save_file("nop", "\n".join(response.json()))
                return response.json()
            except Exception as e:
                if VERBOSE_DEBUG:
                    print(f"{RED}[FAIL] [NOP] try {str(i+1)}: {e}{RESET}")
                else:
                    print(f"{RED}[FAIL] [NOP] Failed to get NOP, try {str(i+1)}{RESET}")
                time.sleep(RETRY_TIME)
        
        if self.backup_manager.backup_enabled:
            print(f"{YELLOW}[WARNING] [Targets] Loading nop from backup{RESET}")
            data = self.backup_manager.load_file("nop")
            if data != "":
                return list(filter(lambda t : len(t) > 0, data.split("\n")))

        return []
    

    def get_own_team(self):
        for i in range(MAX_RETRIES_FOR_SUBMISSION):
            try:
                response = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/own", json={"api_key": API_KEY})
                if self.backup_manager.backup_enabled:
                    self.backup_manager.save_file("own", "\n".join(response.json()))
                return response.json()
            except Exception as e:
                if VERBOSE_DEBUG:
                    print(f"{RED}[FAIL] [Own] try {str(i+1)}: {e}{RESET}")
                else:
                    print(f"{RED}[FAIL] [Own] Failed to get own team, try {str(i+1)}{RESET}")
                time.sleep(RETRY_TIME)
        
        if self.backup_manager.backup_enabled:
            print(f"{YELLOW}[WARNING] [Targets] Loading own team from backup{RESET}")
            data = self.backup_manager.load_file("own")
            if data != "":
                return list(filter(lambda t : len(t) > 0, data.split("\n")))
            
        return []

        
#------------------------------------------------------------------------------
# Utils
#------------------------------------------------------------------------------

class Utils:

    @staticmethod
    def random_string(length : int, valid_set=string.ascii_letters + string.digits):
        r"""
        Generate a random string of a given length.
        length: int, the length of the string to generate.
        include_symbols: bool, whether to include symbols in the string.
        valid_set: str, the set of characters to choose from.
        """
        return "".join(random.choice(valid_set) for _ in range(length))


    @staticmethod
    def flagids() -> dict:
        r"""
        Return the challenge's flag ids. Flag ids provide useful
        information to exploit services. For example, they can be
        usernames, ids, or any other information.
        """
        for i in range(MAX_RETRIES_FOR_SUBMISSION):
            try:
                response = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/flagids", json={"api_key": API_KEY})
                return response.json()
            except Exception as e:
                if VERBOSE_DEBUG:
                    print(f"{RED}[FAIL] [FlagIds] try {str(i+1)}: {e}{RESET}")
                else:
                    print(f"{RED}[FAIL] [FlagIds] Failed to get flag ids, try {str(i+1)}{RESET}")
        
        return None



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


if __name__ == "__main__":
    # Print banner
    print(YELLOW + banner + RESET)
    print(f"{SKY}[Service]{RESET} {SERVICE}")
    print(f"{SKY}[Exploit]{RESET} {EXPLOIT}")
    print(f"{SKY}[Peaceful Farm server IP]{RESET} {SERVER_IP}")
    print(f"{SKY}[Peaceful Farm server port]{RESET} {SERVER_PORT}")
    print(f"{SKY}[Mode]{RESET} {'NOP' if EXPLOIT_DEBUG == 0 else 'OWN' if EXPLOIT_DEBUG == 1 else 'OPPONENTS'}\n")

    try:
        # Backup manager setup
        backup_manager = BackupManager()
        if backup_manager.create_backup_directory():
            print(f"{GREEN}[SUCCESS] [MAIN] Backup manager set up successfully ✔{RESET}")
        else:
            print(f"{RED}[FAIL] [MAIN] Backup manager failed to set up ✘{RESET}")
            print(f"{YELLOW}[WARNING] [MAIN] Backup will not be created{RESET}")

        # Getting targets
        target_manager = TargetManager(backup_manager)

        if EXPLOIT_DEBUG == 0:
            targets = target_manager.get_nop()
        elif EXPLOIT_DEBUG == 1:
            targets = target_manager.get_own_team()
        else:
            targets = target_manager.get_targets()


        if len(targets) == 0:
            print(f"{RED}[FAIL] [MAIN] No targets found ✘{RESET}")
            print(f"{YELLOW}[WARNING] [MAIN] Exiting...{RESET}")
            exit(1)
        else:
            print(f"{GREEN}[SUCCESS] [MAIN] {len(targets)} Targets found ✔{RESET}")

    except KeyboardInterrupt:
        print(f"{YELLOW}[WARNING] [MAIN] CTRL+C detected before starting threads{RESET}")
        exit(0)
    except Exception as e:
        if VERBOSE_DEBUG:
            print(f"{RED}[EXCEPTION] [MAIN] {e}{RESET}")
        else:
            print(f"{RED}[EXCEPTION] [MAIN] An error occurred before starting threafd{RESET}")
        exit(1)

    client = Client(targets, backup_manager)
    try:
        client.start()
        print(f"{GREEN}[SUCCESS] [MAIN] Threads started ✔{RESET}\n")
        healt_check = client.healt_check()
        while healt_check[0]:
            time.sleep(HEALT_CHECK_TIME)
            healt_check = client.healt_check()
        
        raise HealtException(healt_check[1])
        
    except KeyboardInterrupt:
        print(f"{YELLOW}[WARNING] [MAIN] CTRL+C detected, collecting flags and exiting{RESET}\n")

    except HealtException as e:
        print(f"{RED}[EXCEPTION] [MAIN] Healt check failed -> {e}{RESET}")
        
    finally:
        client.stop()
        print(f"{GREEN}[SUCCESS] [MAIN] Exiting...{RESET}")
        exit(0)