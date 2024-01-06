import sys
import subprocess

_success_text = """
 __          __  _                            _        
 \ \        / / | |                          | |       
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___  
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \ 
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |
     \/  \/_\___|_|\___\___/|_|_|_|_|_|\___|  \__\___/ 
          / ____|_   _| /_ |/ _ \ / _ \|  _ \          
         | (___   | |    | | | | | | | | |_) |         
          \___ \  | |    | | | | | | | |  _ <          
          ____) |_| |_   | | |_| | |_| | |_) |         
         |_____/|_____|  |_|\___/ \___/|____/    
        
  Welcome to SI100B Fall 2020. Your system is all set.
     Now you are ready for homework submission.
     
Now copy and paste output of this program into output.txt and submit it to the GitLab following the instruction in README."""

_unsupported_python_version_text = """Python interpreter in this system is of version {}.

Python version 3.7 is used in SI100B for all submission grading. It is higly recommended for you to switch to Python 3.7 or higher.
If you have installed Python 3.7 or higher, try run the script with `python3` instead of `python`.
"""

_no_git_installation_text = """Check https://www.git-scm.com for more information. 

On Ubuntu Linux, install git with:
  
  sudo apt install git

On macOS, install the Xcode command line tools with:
  
  xcode-select --install

On Windows, download setup from https://git-scm.com/downloads or switch to WSL.
"""

_invaild_git_identity_text = """Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity (replace `your@example.com` with your email and `Your Name` with your name in the command).
"""


class DependencyError(BaseException):
    pass


def _check_python_version():
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 7):
        print("Unsupported Python interpreter version.")
        print(_unsupported_python_version_text.format(
            ".".join([str(sys.version_info[i]) for i in range(3)])))
        raise DependencyError
    else:
        print("Python interpreter: OK. (version {})".format(
            ".".join([str(sys.version_info[i]) for i in range(3)])))


def _check_git_installation():
    cmd = ["git", "--version"]
    try:
        r = subprocess.run(cmd, stdout=subprocess.PIPE)
        r.check_returncode()
        print("Git installation: OK. (version: {})".format(
            r.stdout.decode().strip()))
    except:
        print("Could not find your git installation.")
        print(_no_git_installation_text)
        raise DependencyError


def _check_git_signature():
    email_cmd = ["git", "config", "user.email"]
    name_cmd = ["git", "config", "user.name"]
    r_email = subprocess.run(email_cmd, stdout=subprocess.PIPE)
    r_name = subprocess.run(name_cmd, stdout=subprocess.PIPE)
    if r_email.returncode != 0 or r_name.returncode != 0:
        print("Git identity is not configured.")
        print(_invaild_git_identity_text)
        raise DependencyError
    else:
        print("Git identity: OK. (identity: {} <{}>)".format(
            r_name.stdout.decode().strip(), r_email.stdout.decode().strip()))


def _draw_si100b():
    print(_success_text)


if __name__ == "__main__":
    try:
        _check_python_version()
        _check_git_installation()
        _check_git_signature()
    except DependencyError:
        print("Failed: Please fix the problem above before you continue.")
        exit(-1)
    _draw_si100b()
