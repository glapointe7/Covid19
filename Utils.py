import matplotlib.pyplot as plt
import importlib.util
import importlib
import subprocess
import sys

def installPackageIfNotInstalled(library_name):
    spec = importlib.util.find_spec(library_name)
    if spec is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])

class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'