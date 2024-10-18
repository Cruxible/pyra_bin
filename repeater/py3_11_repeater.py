#!/usr/bin/env python3

#Author: Ioannes Cruxibulum
#Nov.16th 2023

import getpass
import os
import time
import platform
import sys
import webbrowser
import pyautogui
from rich.tree import Tree
from rich import print
from rich.console import Console

class string_var:
	num_links = ' Number of links'
	enter_links = ' Enter links'
	tab_closed = ' tab closed'
	not_valid = ' Not a valid attack option.'

	enter_link = '\n Enter a link or press enter to skip'
	enter_time = '\n Enter a time interval'
	iter_finished = ' File iteration finished'
	not_linux = ' This is not Linux'

class MySexyVariables:
	docs_dir = os.path.join(os.path.expanduser("~"), "Documents")
	x = os.listdir(docs_dir)
	list_dirs = os.listdir(docs_dir)


class main_logo:
	def logo():
		print(" [red1]___  _   _ ____ ____\n |__]  \\_/  |__/ |__|\n |      |   |  \\ |  |[/red1]\n")

class Input:
	@staticmethod
	def get_string_input():
		user = getpass.getuser()
		curdir = os.getcwd()
		console = Console()
		return console.input(" [white]_____________________________________[/white]" + "[red]\n  _ [/red]" + "[white]" + curdir + " [/white]" + "[red]\n (__[/red]" + "[white]" + user + "[/white]" + "[red] __: [/red]")

	@staticmethod
	def get_integer_input():
		user = getpass.getuser()
		curdir = os.getcwd()
		console = Console()
		return int(console.input(" [white]_____________________________________[/white]" + "[red]\n  _ [/red]" + "[white]" + curdir + " [/white]" + "[red]\n (__[/red]" + "[white]" + user + "[/white]" + "[red] __: [/red]"))

class main_functions:
	@staticmethod
	def txt_list():
		tree = Tree("[white]" + MySexyVariables.docs_dir, guide_style="red")
		for i in MySexyVariables.list_dirs:
		    tree.add("[white]" + str(i))
		print(" ", tree, " ___________________________________")

	@staticmethod
	def single_repeater():
		while True:
			main_functions.txt_list()
			string_input = Input.get_string_input()
			if string_input in MySexyVariables.list_dirs:
				print(string_var.enter_link)
				user_input_link = Input.get_string_input()
				print(string_var.enter_time)
				time_interval = Input.get_integer_input()
				if user_input_link:
					webbrowser.open(user_input_link)
					time.sleep(10)
					with open(string_input, 'r') as word:
						lines = word.readlines()
						for line in lines:
							print(line)
							time.sleep(time_interval)
							pyautogui.typewrite(line)
							pyautogui.press('enter')
					return string_var.iter_finished
				else:
					time.sleep(10)
					with open(string_input, 'r') as word:
						lines = word.readlines()
						for line in lines:
							print(line)
							time.sleep(time_interval)
							pyautogui.typewrite(line)
							pyautogui.press('enter')
					return string_var.iter_finished
			elif string_input == "exit":
				os.system('clear')
				sys.exit()
			else:
				return string_var.not_valid

class Main:
	def main():
	    main_logo.logo()
	    os.chdir(MySexyVariables.docs_dir)
	    main_functions.single_repeater()

if __name__ == "__main__":
	if platform.system() == 'Linux':
		print(f" System: {platform.system()}\n Node Name: {platform.node()}\n Release: {platform.release()}")
		print(f" Version: {platform.version()}\n Machine: {platform.machine()}\n Python version: {platform.python_version()}")
		Main.main()
