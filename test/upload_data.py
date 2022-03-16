"""
Auto commit data in Python
"""

import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

git_path = "F:\Filippo Gambarota\git\git-cmd.exe"

# activating git
#subprocess.call([git_path])

# pulling remote
subprocess.call(["git", "pull"])
 
# subject number
subj_number = input("Inserisci il numero del soggetto: ")

# adding all relevant files
subprocess.call(["git", "add", "data/"])

# commit message
msg = "adding subject {}".format(subj_number)

# commit
subprocess.call(["git", "commit", "-m", msg])

# pushing to remote
subprocess.call(["git", "push"])

print(bcolors.OKGREEN + "I dati sono stati salvati! :)" + bcolors.OKGREEN)