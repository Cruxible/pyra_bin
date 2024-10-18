#!/usr/bin/env python3
#Created by: Ioannes Cruxibulum
#Date Created: 11-23-23

import subprocess
import pathlib
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from gi.repository import GLib

class MySexyVariables:
    desktop = pathlib.Path.home() / "Desktop"
    desktop = pathlib.Path.home() / "pyra_bin"

class MenuBarWindow1(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Secondary Window")
        self.set_default_size(400, 300)  # Customize the window size

        label = Gtk.Label(label="Hello from the first menu bar window!")
        self.add(label)

class TextBoxWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pyra Desktop")
        self.set_default_size(600, 850)
        self.set_border_width(10)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        # Create a menubar
        menubar = Gtk.MenuBar()

        # Create a "File" menu
        file_item = Gtk.MenuItem(label="File")
        file_menu = Gtk.Menu()
        file_item.set_submenu(file_menu)

        # Add menu items
        open_item = Gtk.MenuItem(label="Open")
        open_item.connect("activate", self.open_file)
        file_menu.append(open_item)

        save_item = Gtk.MenuItem(label="Save")
        save_item.connect("activate", self.save_to_file)
        file_menu.append(save_item)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit_app)
        file_menu.append(quit_item)

        # Add the "File" menu to the menubar
        menubar.append(file_item)

        # Add additional menu items
        pyra_applications_item = Gtk.MenuItem(label="Pyra Terminal Apps")
        pyra_applications_menu = Gtk.Menu()
        pyra_applications_item.set_submenu(pyra_applications_menu)
        menubar.append(pyra_applications_item)

        quit_item1 = Gtk.MenuItem(label="Quit")
        quit_item1.connect("activate", Gtk.main_quit)
        pyra_applications_menu.append(quit_item1)

        hello_item1 = Gtk.MenuItem(label="Print Hello")
        hello_item1.connect("activate", self.open_new_window)
        pyra_applications_menu.append(hello_item1)

        cli_editor = Gtk.MenuItem(label="pyra toolz")
        cli_editor.connect("activate", self.cli_downloader)
        pyra_applications_menu.append(cli_editor)

        gui_editor = Gtk.MenuItem(label="Pyra Editor")
        gui_editor.connect("activate", self.gui_editor)
        pyra_applications_menu.append(gui_editor)

        repeater = Gtk.MenuItem(label="Repeater")
        repeater.connect("activate", self.Repeater)
        pyra_applications_menu.append(repeater)

        # Add the menubar to the window
        self.box.pack_start(menubar, False, False, 0)


        self.entry = Gtk.Entry()
        self.entry.set_name('first_entry')
        self.entry.set_text("")
        self.box.pack_start(self.entry, False, True, 0)

        self.button = Gtk.Button(label="Run File/Enter")
        self.button.set_name('first_button')
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, False, True, 0)

        self.button2 = Gtk.Button(label="Compile Program")
        self.button2.set_name('second_button')
        self.button2.connect("clicked", self.on_second_button_clicked)
        self.box.pack_start(self.button2, False, True, 0)

        #create the label
        self.note_label = Gtk.Label(label="Notes")
        #sets the css name
        self.note_label.set_name("note_label")
        self.box.pack_start(self.note_label, False, True, 0)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.box.pack_start(self.scrollable_treelist, False, True, 0)
        self.textview = Gtk.TextView()
        self.textview.set_name('text_box')
        self.textbuffer = self.textview.get_buffer()
        self.scrollable_treelist.add(self.textview)

        # Add a scrolled window for displaying messages
        self.scrolled_window = Gtk.ScrolledWindow()
        self.box.pack_start(self.scrolled_window, False, True, 0)
        # Add a label for displaying messages inside the scrolled window
        self.message_label = Gtk.Label()
        self.message_label.set_name('message_label')
        self.scrolled_window.add(self.message_label)
        self.message_label.set_text(f"Welcome Sentient!")

        # Apply CSS
        css_provider = Gtk.CssProvider()
        css = """
        #first_entry {
            font-family: Sans;
            font-size: 20px;
        }
        #first_button {
            font-family: Sans;
            font-size: 20px;
        }
        #second_button {
            font-family: Sans;
            font-size: 20px;
        }
        #note_label {
            font-family: Sans;
            font-size: 20px;
        }
        #text_box {
            font-family: Sans;
            font-size: 20px;
        }
        #message_label {
            font-family: Sans;
            font-size: 14px;
        }
        """
        css_provider.load_from_data(css.encode())
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def quit_app(self, widget):
        self.destroy()

    def on_button_clicked(self, widget):
        filename = self.entry.get_text()

        # Search for the file on the desktop
        desktop_path = pathlib.Path.home() / "Desktop"
        for file_path in desktop_path.rglob(filename):
            file_parent_dir = file_path.parent
            found = True
            break
        else:
            # Search for the file in the home directory
            home_dir = pathlib.Path.home() / "pyra_bin"
            for file_path in home_dir.rglob(filename):
                file_parent_dir = file_path.parent
                found = True
                break
            else:
                raise FileNotFoundError(f"{filename} not found in Desktop or pyra env")
        if file_path.suffix == ".py":
            # Check if the file exists
            if (file_parent_dir / filename).exists():
                self.compile_py(filename, str(file_parent_dir))
            else:
                print(f"File '{filename}' does not exist in '{file_parent_dir}'.")
        elif file_path.suffix == "":
            # Check if the file exists
            if (file_parent_dir / filename).exists():
                self.compile_executable(filename, str(file_parent_dir))
            else:
                print(f"File '{filename}' does not exist in '{file_parent_dir}'.")

    def on_second_button_clicked(self, widget):
        filename = self.entry.get_text()
        # Search for the file on the desktop
        desktop_path = pathlib.Path.home() / "Desktop"
        for file_path in desktop_path.rglob(filename):
            file_parent_dir = file_path.parent
            found = True
            break
        else:
            # Search for the file in the home directory
            home_dir = pathlib.Path.home() / "pyra_bin"
            for file_path in home_dir.rglob(filename):
                file_parent_dir = file_path.parent
                found = True
                break
            else:
                raise FileNotFoundError(f"{filename} not found in Desktop or pyra env")
        if file_path.suffix == ".c":
            # Check if the file exists
            if (file_parent_dir / filename).exists():
                self.compile_c_lang(filename, str(file_parent_dir))
            else:
                print(f"File '{filename}' does not exist in '{file_parent_dir}'.")
        elif file_path.suffix == ".cpp":
            # Check if the file exists
            if (file_parent_dir / filename).exists():
                self.compile_c_plusplus(filename, str(file_parent_dir))
            else:
                print(f"File '{filename}' does not exist in '{file_parent_dir}'.")
        elif file_path.suffix == ".py":
            # Check if the file exists
            if (file_parent_dir / filename).exists():
                self.compile_cx(filename, str(file_parent_dir))
            else:
                print(f"File '{filename}' does not exist in '{file_parent_dir}'.")

    def compile_c_lang(self, filename, filepath):
        # Convert the input path to a pathlib.Path object
        filepath = pathlib.Path(filepath)
        # Construct the absolute path of the file using pathlib
        file_path = filepath / filename
        # Get the output filename without the extension
        output_file = file_path.stem
        # Use the full file path for the gcc compilation
        subprocess.run(['gcc', str(file_path), '-o', str(output_file)], check=True)
        # Update the message label with the full file path
        self.message_label.set_text(f'{filename} compilation complete.\n{filepath}')

    def compile_c_plusplus(self, filename, filepath):
        # Convert the input path to a pathlib.Path object
        filepath = pathlib.Path(filepath)
        # Construct the absolute path of the file using pathlib
        file_path = filepath / filename
        # Get the output filename without the extension
        output_file = file_path.stem
        # Use the full file path for the g++ compilation
        subprocess.run(['g++', str(file_path), '-o', str(output_file)], check=True)
        # Update the message label with the full file path
        self.message_label.set_text(f'{filename} compilation complete.\n{filepath}')

    def compile_py(self, filename, file_parent_dir):
        file_path = pathlib.Path(file_parent_dir) / filename
        if file_path.exists():
            try:
                # Use the full file path to run the Python script
                subprocess.run(['python3', str(file_path)], check=True)
                self.message_label.set_text(f'{filename} execution complete.\n{file_parent_dir}')
            except subprocess.CalledProcessError as e:
                print(f"Error executing {filename}: {e}")
        else:
            self.message_label.set_text(f"File '{filename}' does not exist in '{file_parent_dir}'.")

    def compile_cx(self, filename, filepath):
        # Check if the desired character setup is in the file
        if "setup" in filename:
            # Use the full file path to run the Python script
            subprocess.run(['python3', str(filename), 'build'], check=True)
            # Update the message label with the full file path
            self.message_label.set_text(f'{filename} compilation complete.\n{filepath}')
        else:
            # If the desired character setup is not in the file, display an error message
            self.message_label.set_text(f"{filename} cannot be compiled. Setup not in filename.")

    def compile_executable(self, filename, filepath):
        # Convert the input path to a pathlib.Path object
        filepath = pathlib.Path(filepath)
        # Construct the absolute path of the file using pathlib
        file_path = filepath / filename
        # Use the full file path in the chmod command
        subprocess.run(['chmod', '+x', file_path], check=True)
        # Use the full file path to execute it
        subprocess.run([file_path], check=True)
        # Update the message label with the full file path
        self.message_label.set_text(f'{filename} compilation complete.\n{filepath}')

    def open_file(self, widget):
        self.dialog = Gtk.FileChooserDialog(
            title="Please choose a file to open",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
        # Set the current folder to 'Documents'
        documents_folder = pathlib.Path.home() / "Documents"
        self.dialog.set_current_folder(str(documents_folder))
        self.dialog.show_all()  # Ensure the dialog is shown first
        self.dialog.resize(450, 300)
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            file_selected = True
            filename = self.dialog.get_filename()
            with open(filename, "r") as file:
                content = file.read()
                # Update the text buffer with the file content
                self.textbuffer.set_text(content)
                self.message_label.set_text(f"Opened file: {filename}")
        
        elif response == Gtk.ResponseType.CANCEL:
            file_selected = False

        self.dialog.destroy()

    def save_to_file(self, button):
        self.dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            parent=self,
            action=Gtk.FileChooserAction.SAVE
        )
        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK
        )
        # Set the current folder to 'Videos'
        documents_folder = pathlib.Path.home() / "Documents"
        self.dialog.set_current_folder(str(documents_folder))
        self.dialog.show_all()  # Ensure the dialog is shown first
        self.dialog.resize(450, 300)
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            file_selected = True
            filename = self.dialog.get_filename()
            textbuffer = self.textview.get_buffer()
            start_iter = textbuffer.get_start_iter()
            end_iter = textbuffer.get_end_iter()
            text = textbuffer.get_text(start_iter, end_iter, False)
            with open(filename, 'w') as f:
                f.write(text)
                self.message_label.set_text(f"Saved File: {filename}")
        
        elif response == Gtk.ResponseType.CANCEL:
            file_selected = False
        
        self.dialog.destroy()

    def Repeater(self, widget):
        home_dir = pathlib.Path.home()
        exe_path1 = home_dir / "pyra_bin" / "repeater" / "pyra_repeater"
        # Replace with the actual path to your executable
        subprocess.Popen(["mate-terminal", "-e", exe_path1])

    def cli_downloader(self, widget):
        home_dir = pathlib.Path.home()
        exe_path1 = home_dir / "pyra_bin" / "pyra_tool" / "pyra_toolz"
        # Replace with the actual path to your executable
        subprocess.Popen(["mate-terminal", "-e", exe_path1])

    def gui_editor(self, widget):
        home_dir = pathlib.Path.home()
        exe_path1 = home_dir / "pyra_bin" / "pyra_desktop_env" / "pyra_guis" / "pyra_gui_editor"
        subprocess.Popen([exe_path1])
        #self.message_label.set_text(f'{filename} compilation complete.\n{filepath}')

    def open_new_window(self, widget):
        print("first menu bar window opened")
        new_win = MenuBarWindow1()  # Create an instance of the secondary window
        new_win.show_all()


if __name__ == "__main__":
    win = TextBoxWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()