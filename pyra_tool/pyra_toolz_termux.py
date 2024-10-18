#!/usr/bin/env python3

#Author: Ioannes Cruxibulum
#Sep.10th 2023

#sudo apt install yt-dlp

#pkg install gnupg
#create a password protected tarfile.
#tar -czvf archive.tar.gz file1 file2 file3

#decrypt tar file.
#gpg --decrypt archive.tar.gz.gpg | tar -xzvf -


##unpacks the tarball
#tar -xvf your_tarball.tar.gz

import platform
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

class main_functions:
	@staticmethod
	def download_video():
		def download_call():
			list_choice = ['mp3', 'best video']
			tree = Tree("[white]" + " How would you like to download?",guide_style="red")
			for i in list_choice:
				tree.add("[white]" + str(i))
			print(" ", tree)
			video_format = Input.get_string_input()
			if video_format == 'mp3':
				print("filename?")
				output_filename = Input.get_string_input()
				print(' [white]Please enter a link[/white]')
				url = Input.get_string_input()
				mp3_command = f"yt-dlp -x --audio-format mp3 -o {output_filename} {url}"
				subprocess.call(mp3_command, shell=True)
			elif video_format == 'best video':
				print("filename?")
				output_filename = Input.get_string_input()
				print(' [white]Please enter a link[/white]')
				url = Input.get_string_input()
				#best_video_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -o {output_filename} "{url}"'
				best_video_command = f'yt-dlp -f "bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" --merge-output-format mp4 -o "{output_filename}" "{url}"'
				subprocess.call(best_video_command, shell=True)
			elif video_format == 'exit':
				sys.exit()

		print(HonerableMentions.save_where)
		directory = Input.get_string_input()
		# Call download_call with the correct directory based on user input
		if directory == 'Desktop':
			os.chdir(MySexyVariables.desktop_dir)
			download_call()
		elif directory == 'Videos':
			os.chdir(MySexyVariables.video_dir)
			download_call()
		elif directory == 'droid movies':
			os.chdir(MySexyVariables.sd_video_dir)
			download_call()
		elif directory == 'droid music':
			os.chdir(MySexyVariables.sd_music_dir)
			download_call()
		elif directory == MySexyVariables.calls_list[1]:
			sys.exit()

	@staticmethod
	def search_for_file(directory, filename):
		"""Search for a specific file by name in the given directory and subdirectories."""
		for file in directory.rglob(filename):
			if file.is_file():
				return file
		return None

	@staticmethod
	def run_or_compile(file_path):
		"""Run or compile the file based on its extension."""
		if file_path.suffix == ".py":
			print(f"Running Python file: {file_path}")
			subprocess.run(["python3", str(file_path)])
		elif file_path.suffix == ".c":
			print(f"Compiling and running C file: {file_path}")
			executable = file_path.with_suffix("")
			subprocess.run(["gcc", str(file_path), "-o", str(executable)])
			subprocess.run([str(executable)])
		elif file_path.suffix == ".cpp":
			print(f"Compiling and running C++ file: {file_path}")
			executable = file_path.with_suffix("")
			subprocess.run(["g++", str(file_path), "-o", str(executable)])
			subprocess.run([str(executable)])
		elif file_path.suffix == "":
			print(f"Compiling and running executable file: {file_path}")
			executable = file_path.with_suffix("")
			subprocess.run([str(executable)])
		else:
			print(f"Unknown file extension: {file_path}")

	@staticmethod
	def pyra_run_func():
		while True:
			if MySexyVariables.SEARCH_DIRECTORY.is_dir():
				print("\n Enter a filename:")
				filename = Input.get_string_input().strip()
				# Exit the loop if the user inputs 'exit' (case-insensitive)
				if filename.lower() == 'exit':
					print("Exiting the loop...")
					break
				print(f"Searching for '{filename}' in '{MySexyVariables.SEARCH_DIRECTORY}'...")
				file_path = main_functions.search_for_file(MySexyVariables.SEARCH_DIRECTORY, filename)
				if file_path:
					print(f"File found: {file_path}")
					main_functions.run_or_compile(file_path)
				else:
					print(f"File '{filename}' not found in the directory.")
			else:
				print(f"Error: {MySexyVariables.SEARCH_DIRECTORY} is not a valid directory.")

	@staticmethod
	def encrypt_tarball(tar_filename, password):
		"""Encrypts the tarball using GPG with a password."""
		encrypted_filename = tar_filename + ".gpg"
		try:
			subprocess.run(
				["gpg", "--symmetric", "--cipher-algo", "AES256", "--batch", "--yes",
				"--passphrase", password, tar_filename],
				check=True
				)
			print(f"Encrypted tarball: {encrypted_filename}")
			# Move encrypted file to /sdcard/Download/
			destination = f"/sdcard/Download/{os.path.basename(encrypted_filename)}"
			shutil.move(encrypted_filename, destination)
			print(f"Moved encrypted tarball to {destination}")
			# Clean up the original tar file
			os.remove(tar_filename)
		except Exception as e:
			print(f"Failed to encrypt or move the tarball: {e}")

	@staticmethod
	def decrypt_tarball(encrypted_filename, password):
		"""Decrypts the GPG-encrypted tarball."""
		try:
			# Define the decrypted filename
			decrypted_filename = encrypted_filename.replace(".gpg", "")
			# Decrypt and save the tarball
			with open(decrypted_filename, "wb") as decrypted_file:
				subprocess.run(
					["gpg", "--decrypt", "--batch", "--yes", "--passphrase", password, encrypted_filename],
					stdout=decrypted_file,
					check=True
					)
			print(f"Decrypted tarball: {decrypted_filename}")
			# Move the decrypted tarball to /sdcard/Download/
			destination = f"/sdcard/Download/{os.path.basename(decrypted_filename)}"
			shutil.move(decrypted_filename, destination)
			print(f"Moved decrypted tarball to: {destination}")
			# Extract the tarball in /sdcard/Download/
			with tarfile.open(destination, "r:gz") as tar:
				tar.extractall("/sdcard/Download/")
			print("Decryption and extraction completed.")
		except Exception as e:
			print(f"Failed to decrypt or extract the tarball: {e}")

	@staticmethod
	def enc_make_tarfile(output_filename, source_dir):
		"""Creates a tar.gz file from the given directory."""
		with tarfile.open(output_filename, "w:gz") as tar:
			tar.add(source_dir, arcname=os.path.basename(source_dir))
		print(f"Created tarball: {output_filename}")

	@staticmethod
	def linux_tarmaker():
		def make_tarfile(output_filename, source_dir):
			with tarfile.open(output_filename, "w:gz") as tar:
				tar.add(source_dir, arcname=os.path.basename(source_dir))
			# Define destination path
			destination = "/sdcard/Download/" + output_filename
			try:
				# Move the tar file to /sdcard/Download
				shutil.move(output_filename, destination)
				print(f"Tarball moved to {destination}")
			except Exception as e:
				print(f"Failed to move the tarball: {e}")

		print(" commands:\n create tarfile\n encrypt tarfile\n decrypt tarfile\n exit")
		tar_funcs = Input.get_string_input()
		if tar_funcs == "create tarfile":
			print("\n Directory to be packed? (Example: /home/ioannes/pyra_bin)")
			source_dir = Input.get_string_input()
			if source_dir == "exit":
				sys.exit()
			print("\n New Tarball name?")
			new_dir = Input.get_string_input()
			if new_dir == "exit":
				sys.exit()
			make_tarfile(f"{new_dir}.tar.gz", source_dir)
		elif tar_funcs == "encrypt tarfile":
			print("\n Directory to be packed? (Example: /home/ioannes/pyra_bin)")
			source_dir = Input.get_string_input()
			if source_dir == "exit":
				sys.exit()
			print("\n New Tarball name?")
			new_dir = Input.get_string_input()
			if new_dir == "exit":
				sys.exit()
			tar_filename = f"{new_dir}.tar.gz"
			main_functions.enc_make_tarfile(tar_filename, source_dir)
			print("\n Enter a password for encryption:")
			password = Input.get_string_input()
			main_functions.encrypt_tarball(tar_filename, password)
		elif tar_funcs =="decrypt tarfile":
			print("\n Encrypted tarball path? (Example: /sdcard/Download/archive.tar.gz.gpg)")
			encrypted_filename = Input.get_string_input()
			if encrypted_filename == "exit":
				sys.exit()
			print("\n Enter the decryption password:")
			password = Input.get_string_input()
			main_functions.decrypt_tarball(encrypted_filename, password)
		elif tar_funcs == "exit":
			sys.exit()
		else:
			print("Invalid command")

class calls:
	@staticmethod
	def call_list():
		tree = Tree("[white]" + " Editing Tools", guide_style= "red")
		for i in MySexyVariables.calls_list:
			tree.add("[white]" + str(i))
		print(" ", tree)

class list_dirs:
	@staticmethod
	def vid_list():
		tree = Tree("[white]" + str(MySexyVariables.video_dir), guide_style="red")
		for i in MySexyVariables.vid_list:
			tree.add("[white]" + str(i))
		print(" ", tree)

	@staticmethod
	def music_list():
		tree = Tree("[white]" + str(MySexyVariables.audio_dir), guide_style="red")
		for i in MySexyVariables.audio_list:
			tree.add("[white]" + str(i))
		print(" ", tree)

	@staticmethod
	def desktop_list():
		tree = Tree("[white]" + str(MySexyVariables.desktop_dir), guide_style="red")
		for i in MySexyVariables.desktop_list:
			tree.add("[white]" + str(i))
		print(" ", tree)

	@staticmethod
	def picture_list():
		tree = Tree("[white]" + str(MySexyVariables.pics_dir), guide_style="red")
		for i in MySexyVariables.pics_list:
			tree.add("[white]" + str(i))
		print(" ", tree)

	@staticmethod
	def sd_vid_list():
		tree = Tree("[white]" + str(MySexyVariables.sd_video_dir), guide_style="red")
		for i in MySexyVariables.sd_video_list:
			tree.add("[white]" + str(i))
		print(" ", tree)

	@staticmethod
	def sd_music_list():
		tree = Tree("[white]" + str(MySexyVariables.sd_music_dir), guide_style="red")
		for i in MySexyVariables.sd_music_list:
			tree.add("[white]" + str(i))
		print(" ", tree)

class Input:
    @staticmethod
    def get_string_input():
        user = getpass.getuser()
        curdir = os.getcwd()
        console = Console()
        return console.input(" [white]_______________________________________________[/white]" + "[red]\n ┌░[/red]" + "[white]" + curdir + "░[/white]" + "[red]\n └░[/red]" + "[white]" + user + "[/white]" + "[red]░ [/red]")

    @staticmethod
    def get_integer_input():
        user = getpass.getuser()
        curdir = os.getcwd()
        console = Console()
        return int(console.input(" [white]_______________________________________________[/white]" + "[red]\n ┌░[/red]" + "[white]" + curdir + "░[/white]" + "[red]\n └░[/red]" + "[white]" + user + "[/white]" + "[red]░ [/red]"))

    @staticmethod
    def get_float_input():
        user = getpass.getuser()
        curdir = os.getcwd()
        console = Console()
        return float(console.input(" [white]_______________________________________________[/white]" + "[red]\n ┌░[/red]" + "[white]" + curdir + "░[/white]" + "[red]\n └░[/red]" + "[white]" + user + "[/white]" + "[red]░ [/red]"))

class main_logo:
	def logo():
		program_creator = " Creator: Ioannes Cruxibulum"
		program_name = " Termux Pyra Toolz"
		program_version = " 3.0"
		logos = [f"[red1] \n  ██▓███ ▓██   ██▓ ██▀███   ▄▄▄      \n ▓██░  ██▒▒██  ██▒▓██ ▒ ██▒▒████▄    \n ▓██░ ██▓▒ ▒██ ██░▓██ ░▄█ ▒▒██  ▀█▄  \n ▒██▄█▓▒ ▒ ░ ▐██▓░▒██▀▀█▄  ░██▄▄▄▄██ \n ▒██▒ ░  ░ ░ ██▒▓░░██▓ ▒██▒ ▓█   ▓██▒\n ▒▓▒░ ░  ░  ██▒▒▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░\n ░▒ ░     ▓██ ░▒░   ░▒ ░ ▒░  ▒   ▒▒ ░\n ░░       ▒ ▒ ░░    ░░   ░   ░   ▒   \n          ░ ░        ░           ░  ░\n          ░ ░                        \n{program_name} {program_version}\n{program_creator}[/red1]", f" [red1] ___  _   _ ____ ____\n  |__]  \\_/  |__/ |__|\n  |      |   |  \\ |  |\n {program_name} {program_version}\n {program_creator}[/red1]"]
		print(random.choice(logos))

class HonerableMentions:
	mp4 = " [white]Please choose a mp4[/white]"
	mp3 = " [white]Please choose a mp3[/white]"
	starting_time = " [white]start time?[/white]"
	ending_time = " [white]End Time?[/white]"
	save_where = " [white]Save on Desktop Videos droid movies droid music?[/white]"
	save_audio_where = " [white]Save on Desktop Music or droid?[/white]"
	old_filename = " [white]Filename?[/bright_black]"
	new_filename = " [white]New filename?[/white]"
	exit_program = " [white]Exiting the program...[/white]"

class MySexyVariables:
	SEARCH_DIRECTORY = Path.home() / "pyra_bin"
	video_dir = Path.home() / "Videos"
	audio_dir = Path.home() / "Music"
	desktop_dir = Path.home() / "Desktop"
	pics_dir = Path.home() / "Pictures"
	sd_video_dir = Path("/sdcard/Movies")
	sd_music_dir = Path("/sdcard/Music")
	vid_list = os.listdir(video_dir)
	audio_list = os.listdir(audio_dir)
	desktop_list = os.listdir(desktop_dir)
	pics_list = os.listdir(pics_dir)
	sd_video_list = os.listdir(sd_video_dir)
	sd_music_list = os.listdir(sd_music_dir)
	calls_list = [
                                "download",
                                "pyra run",
                                "tarfile",
                                "exit",
                                "list"
                                ]

class Main_Termux:
	def main():
		if platform.system() == 'Linux':
			calls.call_list()
			while True:
				command = Input.get_string_input()
				if command == MySexyVariables.calls_list[0]:
					main_functions.download_video()
					Main_Termux.main()
				elif command == MySexyVariables.calls_list[1]:
					main_functions.pyra_run_func()
					Main_Termux.main()
				elif command == MySexyVariables.calls_list[2]:
					main_functions.linux_tarmaker()
					Main_Termux.main()
				elif command == MySexyVariables.calls_list[3]:
					sys.exit()
				elif command == MySexyVariables.calls_list[4]:
					while True:
						list_dir_commands = ["videos", "music", "desktop", "pictures", "sd videos", "sd music", "exit"]
						tree = Tree("[white]" + " which directory?", guide_style= "red")
						for i in list_dir_commands:
							tree.add("[white]" + str(i))
						print(" ", tree)
						command = Input.get_string_input()
						if command == "videos":
							list_dirs.vid_list()
						elif command == "music":
							list_dirs.music_list()
						elif command == "desktop":
							list_dirs.desktop_list()
						elif command == "pictures":
							list_dirs.picture_list()
						elif command == "sd videos":
							list_dirs.sd_vid_list()
						elif command == "sd music":
							list_dirs.sd_music_list()
						elif command == "exit":
							Main_Termux.main()
				else:
					continue
		else:
			print(' Wrong, just wrong. Do it again.')
