#!/usr/bin/env python3
#Created by: Ioannes Cruxibulum
#Date Created: 11-23-23

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
from pyra_downloader import DownloaderWindow
from cut_video import FileChooser_Cut_Vid
from cut_audio import FileChooser_Cut_Audio
from merge_aud_vid import FileChooser_Merge
from extract_audio import FileChooser_Extract_Audio
from adjust_volume import FileChooser_Adjust_Vol
from concat_vid import FileChooser_Stitch_Vid
from concat_aud import FileChooser_Stitch_Audio

class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pyra Video/Audio Editor")

        # Set the window size here
        self.set_default_size(450, 300)

        # Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Creating the ListStore model
        self.func_liststore = Gtk.ListStore(str)
        for main_functions in [
                            "YT Downloader",
                            "Cut Video", "Cut Audio",
                            "Merge Audio Video",
                            "Extract Audio",
                            "Adjust Volume",
                            "Stitch Video",
                            "Stitch Audio"
                            ]:
            self.func_liststore.append([main_functions])

        # Creating the treeview and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.func_liststore)
        for i, column_title in enumerate(["Editing Functions"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("font", "Sans 14")  # Change the font size here
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # Connect the row-activated signal to the on_row_activated function
        self.treeview.connect("row-activated", self.on_row_activated)

        # Setting up the layout, putting the treeview in a scrollwindow
        self.scrollable_treelist = Gtk.ScrolledWindow()
        # Makes the treeview expand the height of the window
        self.scrollable_treelist.set_vexpand(True)
        # Makes the treeview expand the width of the window
        self.scrollable_treelist.set_hexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()

    def on_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        iter = model.get_iter(path)
        main_functions = model.get_value(iter, 0)

        # Perform an action based on the selected list
        if main_functions == "YT Downloader":
            self.yt_downloader_func()
        elif main_functions == "Cut Video":
            self.cut_vid_func()
        elif main_functions == "Cut Audio":
            self.cut_audio_func()
        elif main_functions == "Merge Audio Video":
            self.merge_av_func()
        elif main_functions == "Extract Audio":
            self.extract_audio_func()
        elif main_functions == "Adjust Volume":
            self.adjust_vol_func()
        elif main_functions == "Stitch Video":
            self.stitch_video()
        elif main_functions == "Stitch Audio":
            self.stitch_audio()

    def yt_downloader_func(self):
        tree_win.hide()
        ytd_win = DownloaderWindow(self)  # Pass the current instance (self) to DownloaderWindow
        ytd_win.show_all()
        print("yt_downloader_func complete.")
    def cut_vid_func(self):
        tree_win.hide()
        cut_vid = FileChooser_Cut_Vid(self)
        cut_vid.show_all()
        print("cut_vid_func complete.")
    def cut_audio_func(self):
        tree_win.hide()
        cut_audio = FileChooser_Cut_Audio(self)
        cut_audio.show_all()
        print("cut_audio_func complete.")
    def merge_av_func(self):
        tree_win.hide()
        merge = FileChooser_Merge(self)
        merge.show_all()
        print("merge_func complete.")
    def extract_audio_func(self):
        tree_win.hide()
        merge = FileChooser_Extract_Audio(self)
        merge.show_all()
        print("extract_audio_func complete.")
    def adjust_vol_func(self):
        tree_win.hide()
        adjust_vol = FileChooser_Adjust_Vol(self)
        adjust_vol.show_all()
        print("adjust_vol_func complete.")
    def stitch_video(self):
        tree_win.hide()
        stitch_vid = FileChooser_Stitch_Vid(self)
        stitch_vid.show_all()
        print("stitch_vid_func complete.")
    def stitch_audio(self):
        tree_win.hide()
        stitch_aud = FileChooser_Stitch_Audio(self)
        stitch_aud.show_all()
        print("stitch_aud_func complete.")

if __name__ == "__main__":
    tree_win = TreeViewFilterWindow()
    tree_win.connect("destroy", Gtk.main_quit)
    Gtk.main()  # Starts the GTK main loop