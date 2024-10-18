#!/usr/bin/env python3
#Created by: Ioannes Cruxibulum
#Date Created: 1-18-24
#version 2.0

import os
import gi
import subprocess
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GLib

class DownloaderWindow(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="YouTube Downloader")
        self.set_default_size(450, 300)
        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        self.connect("delete-event", self.on_delete_event)
        self.connect("delete-event", Gtk.main_quit)
        self.set_border_width(10)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_name('url_entry')
        self.url_entry.set_text("Enter YouTube URL here")
        self.box.pack_start(self.url_entry, True, True, 0)

        self.aud_download_button = Gtk.Button(label="Audio Download")
        self.aud_download_button.set_name('audio_download')
        self.aud_download_button.connect("clicked", self.on_aud_download_button_clicked)
        self.box.pack_start(self.aud_download_button, True, True, 0)

        self.button = Gtk.Button(label="Fetch Video Formats")
        self.button.set_name('first_button')
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.format_entry = Gtk.Entry()
        self.format_entry.set_name('format_entry')
        self.format_entry.set_text("Enter format code here")
        self.box.pack_start(self.format_entry, True, True, 0)

        self.download_button = Gtk.Button(label="Download")
        self.download_button.set_name('download_button')
        self.download_button.connect("clicked", self.on_download_button_clicked)
        self.box.pack_start(self.download_button, True, True, 0)

        # Add a scrolled window for displaying messages
        self.scrolled_window = Gtk.ScrolledWindow()
        self.box.pack_start(self.scrolled_window, True, True, 0)

        # Add a label for displaying messages inside the scrolled window
        self.message_label = Gtk.Label()
        self.message_label.set_name('message_label')
        self.scrolled_window.add(self.message_label)
        self.message_label.set_markup(f"Enter a Link.")

        # Apply CSS
        css_provider = Gtk.CssProvider()
        css = """
        #url_entry, #format_entry {
            font-family: Sans;
            font-size: 17px;
        }
        #first_button, #download_button, #audio_download, #message_label {
            font-family: Sans;
            font-size: 17px;
        }
        """
        css_provider.load_from_data(css.encode())
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        print("on_delete_event function complete")
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_button_clicked(self, widget):
        url = self.url_entry.get_text()
        self.update_formats(url)

    def on_download_button_clicked(self, widget):
        try:
            url = self.url_entry.get_text()
            format_code = self.format_entry.get_text()
            self.hide()
            dialog = Gtk.FileChooserDialog(
                title="Save File", 
                parent=self,
                action=Gtk.FileChooserAction.SAVE
            )

            dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE,
                Gtk.ResponseType.OK,
            )
            # Set the current folder to 'Videos'
            dialog.set_current_folder(os.path.expanduser('~/Videos'))
            dialog.show_all()  # Ensure the dialog is shown first
            dialog.resize(450, 300)  # Then attempt to resize it
            response = dialog.run()
            if response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                self.message_label.set_text("Cancel Clicked")
                self.show_all()
            elif response == Gtk.ResponseType.OK:
                output_filename = dialog.get_filename()
                dialog.destroy()
                if not output_filename.endswith('.mp4'):
                    self.show_all()
                    self.message_label.set_text(f"Output filename does not end with .mp4")
                elif output_filename.endswith(".mp4"):
                    self.show_all()
                    # Run the download command in a separate thread
                    def download_video():
                        #Audio Format Command
                        self.show_all()
                        process = subprocess.Popen(["yt-dlp", "-f", format_code, "-o", output_filename, url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                        while True:
                            output = process.stdout.readline()
                            if output == '' and process.poll() is not None:
                                break
                            if output:
                                self.message_label.set_text(output.strip())
                                self.resize(500, 300)
                        rc = process.poll()
                        self.message_label.set_text(f"File saved at: {output_filename}")

                    # Run the video player in a separate thread
                    download_func = threading.Thread(target=download_video)
                    download_func.start()

            else:
                self.message_label.set_text("No file was selected.")
        except Exception as e:
            self.message_label.set_text(str(e))

    def on_aud_download_button_clicked(self, widget):
        try:
            url = self.url_entry.get_text()
            self.hide()
            self.dialog = Gtk.FileChooserDialog(
                title="Save File", 
                parent=self,
                action=Gtk.FileChooserAction.SAVE
            )
            # Set the current folder to 'Music'
            self.dialog.set_current_folder(os.path.expanduser('~/Music'))
            self.dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE,
                Gtk.ResponseType.OK,
            )
            response = self.dialog.run()
            if response == Gtk.ResponseType.CANCEL:
                self.dialog.destroy()
                self.show_all()
                self.message_label.set_text("Cancel Clicked")
            elif response == Gtk.ResponseType.OK:
                output_filename = self.dialog.get_filename()
                if not output_filename.endswith('.mp3'):
                    self.dialog.destroy()
                    self.message_label.set_text("Output filename does not end with .mp3")
                elif output_filename.endswith('.mp3'):
                    self.dialog.destroy()
                    # Run the download command in a separate thread
                    def download_audio():
                        #Audio Format Command
                        self.show_all()
                        process = subprocess.Popen(["yt-dlp", "-x", "--audio-format=mp3", "-o", output_filename, url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                        while True:
                            output = process.stdout.readline()
                            if output == '' and process.poll() is not None:
                                break
                            if output:
                                self.message_label.set_text(output.strip())
                                self.resize(450, 300)
                        rc = process.poll()
                        self.message_label.set_text(f"File saved at: {output_filename}")

                    # Run the video player in a separate thread
                    download_func = threading.Thread(target=download_audio)
                    download_func.start()
            else:
                self.message_label.set_text("No file was selected.")
        except Exception as e:
            self.message_label.set_text(str(e))

    def update_formats(self, url):
        result = subprocess.run(["yt-dlp", "-F", url], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        formats = [line for line in lines if ("mp4" in line and "video only" not in line and "audio only" not in line)]
        self.message_label.set_text('\n'.join(formats))

if __name__ == "__main__":
    win = DownloaderWindow()
    Gtk.main()