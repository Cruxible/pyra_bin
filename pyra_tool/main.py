import platform
from pathlib import Path
from pathlib import Path
import os
import time
import getpass
from rich.tree import Tree
from rich import print
from rich.console import Console
import sys
import subprocess
import random
import tarfile
import shutil

if __name__ == '__main__':
	print(f" [white]System: {platform.system()}\n Node Name: {platform.node()}\n Release: {platform.release()}[/white]")
	print(f" [white]Version: {platform.version()}\n Machine: {platform.machine()}\n Python version: {platform.python_version()}[/white]")
	print(" [red1]All that we see or seem is but a dream within a dream\n ~ Edgar Allen Poe[/red1]")
	if platform.system() == 'Linux':
		if Path("/sdcard/Download").exists():
			from pyra_toolz_termux import Main_Termux
			print(" Android directories exist.")
			Main_Termux.main()
		else:
			if not Path("/sdcard/Download").exists():
				from pyra_toolz import Main
				print(" Android directories do not exist")
				Main.main()
