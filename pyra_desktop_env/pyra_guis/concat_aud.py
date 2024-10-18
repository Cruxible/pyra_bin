import os
import gi
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GLib
from moviepy.editor import AudioFileClip
from moviepy.editor import concatenate_audioclips

class FileChooser_Stitch_Audio(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Stitch Audio")
        self.set_default_size(450, 300)

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)
        self.connect("delete-event", Gtk.main_quit)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.button1 = Gtk.Button(label="Choose First Audio")
        #sets the css name
        self.button1.set_name("first_button")
        self.button1.connect("clicked", self.on_file_clicked)
        self.box.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.Button(label="Choose Second Audio")
        #sets the css name
        self.button2.set_name("second_button")
        self.button2.connect("clicked", self.on_file_clicked)
        self.box.pack_start(self.button2, True, True, 0)

        self.button3 = Gtk.Button(label="Stitch Audio")
        #sets the css name
        self.button3.set_name("third_button")
        self.button3.connect("clicked", self.on_stitch_clicked)
        self.box.pack_start(self.button3, True, True, 0)
        self.button3.set_sensitive(False)

        # Add a scrolled window for displaying messages
        self.scrolled_window = Gtk.ScrolledWindow()
        self.box.pack_start(self.scrolled_window, True, True, 0)

        # Add a label for displaying messages inside the scrolled window
        self.message_label = Gtk.Label()
        #sets the css name
        self.message_label.set_name("update_label")
        self.scrolled_window.add(self.message_label)

        self.audio_files = []

    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        print("on_delete_event function complete")
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_file_clicked(self, widget):
        self.dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        self.dialog.set_current_folder(os.path.expanduser('~/Music'))
        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        response = self.dialog.run()
        if response == Gtk.ResponseType.CANCEL:
            self.dialog.destroy()
            self.message_label.set_markup("Cancel Clicked")
        if response == Gtk.ResponseType.OK:
            self.audio_files.append(self.dialog.get_filename())
            if len(self.audio_files) == 1:
                self.dialog.hide()
            if len(self.audio_files) == 2:
                self.dialog.hide()
                self.button3.set_sensitive(True)

    def on_stitch_clicked(self, widget):
        try:
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
            dialog.set_current_folder(os.path.expanduser('~/Music'))
            response = dialog.run()
            if response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                self.button3.set_sensitive(False)
                self.message_label.set_markup("Cancel clicked")
            elif response == Gtk.ResponseType.OK:
                output_filename = dialog.get_filename()
                if not output_filename.endswith('.mp3'):
                    self.message_label.set_markup(f"Output filename does not end with .mp4")
                else:
                    dialog.destroy()
                    def stitch_audio_func():
                        clips = [AudioFileClip(f) for f in self.audio_files]
                        final_clip = concatenate_audioclips(clips)
                        final_clip.write_audiofile(output_filename)

                        self.audio_files = []
                        self.button3.set_sensitive(False)
                        self.message_label.set_text(f"Audio stitching completed successfully!\n{output_filename}")
                        #GLib.timeout_add_seconds(0, self.destroy)  # 5 seconds delay
                        # Make the treeview window visible
                        #self.treeview_window.destroy()
                        #self.treeview_window.show_all()
                    # Run the video player in a separate thread
                    stitch_audio_thread = threading.Thread(target=stitch_audio_func)
                    stitch_audio_thread.start()
            else:
                self.message_label.set_markup("No file was selected.")
        except Exception as e:
            self.message_label.set_markup(str(e))