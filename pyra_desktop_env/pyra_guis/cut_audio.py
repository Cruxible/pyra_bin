import os
import gi
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GLib
from moviepy.editor import AudioFileClip

class FileChooser_Cut_Audio(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Cut Audio")
        # Create a FileChooserDialog
        self.dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)
        self.connect("delete-event", Gtk.main_quit)
        
        self.set_default_size(450, 300)
        box = Gtk.Box()
        box.set_border_width(10)  # Creates a 10-pixel buffer around the box
        
        # Create a vertical box
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.button1 = Gtk.Button(label="Choose File")
        #sets the css name
        self.button1.set_name("first_button")
        self.button1.connect("clicked", self.on_file_clicked)
        self.box.pack_start(self.button1, True, True, 0)

        #create the label
        self.start_label = Gtk.Label(label="Start Time")
        #sets the css name
        self.start_label.set_name("first_label")
        self.box.pack_start(self.start_label, True, True, 0)

        # Create a scale with a default range
        self.start_time_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 10, 1)
        #sets the css name
        self.start_time_scale.set_name("first_scale")
        self.start_time_scale.set_size_request(200, -1)  # Set the width to 200 and the height to -1 (default)
        self.box.pack_start(self.start_time_scale, True, True, 0)

        #create the label
        self.end_label = Gtk.Label(label="End Time")
        #sets the css name
        self.end_label.set_name("second_label")
        self.box.pack_start(self.end_label, True, True, 0)

        # Create a scale with a default range
        self.end_time_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 10, 1)
        #sets the css name
        self.end_time_scale.set_name("second_scale")
        self.box.pack_start(self.end_time_scale, True, True, 0)

        # Add another button
        self.button2 = Gtk.Button(label='Cut Audio')
        #sets the css name
        self.button2.set_name("second_button")
        self.button2.connect("clicked", self.on_button2_clicked)
        self.box.pack_start(self.button2, True, True, 0)
        self.button2.set_sensitive(False)

        # Add a scrolled window for displaying messages
        self.scrolled_window = Gtk.ScrolledWindow()
        self.box.pack_start(self.scrolled_window, True, True, 0)

        # Add a label for displaying messages inside the scrolled window
        self.message_label = Gtk.Label()
        #sets the css name
        self.message_label.set_name("update_label")
        self.scrolled_window.add(self.message_label)

        css = """
        #first_button, #first_label, #first_scale, #second_label, #second_scale, #second_button, #update_Label {
          font-size: 20px;
        }
        """
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )

        filter_mp4 = Gtk.FileFilter()
        filter_mp4.set_name("MP3 files")
        filter_mp4.add_mime_type("audio/mpeg")
        self.dialog.add_filter(filter_mp4)

        response = self.dialog.run()
        if response == Gtk.ResponseType.CANCEL:
            self.dialog.destroy()
            self.message_label.set_text("Cancel Clicked")
        if response == Gtk.ResponseType.OK:
            #print("You selected %s" % self.dialog.get_filename())
            # Here you can add your video cutting function
            # Get the duration of the video
            clip = AudioFileClip(self.dialog.get_filename())
            duration = clip.duration

            # Update the range of the scale
            self.start_time_scale.set_range(0, duration)
            # Update the range of the scale
            self.end_time_scale.set_range(0, duration)
            self.dialog.hide()
            self.button2.set_sensitive(True)

    def on_button2_clicked(self, widget):
        try:
            start_time_str = self.start_time_scale.get_value()  # Get the text from the start time textbox
            end_time_str = self.end_time_scale.get_value()  # Get the text from the end time textbox
            start_time = int(start_time_str)  # Try to convert the start time to an integer
            end_time = int(end_time_str)  # Try to convert the end time to an integer
            # Here you can add your video cutting function
            filename = self.dialog.get_filename()
            if self.dialog is None:
                self.message_label.set_text("Please select a file first.")
                return
            if filename is not None:
                self.dialog = Gtk.FileChooserDialog(
                    title="Please choose a file", 
                    parent=self,
                    action=Gtk.FileChooserAction.SAVE
                )
                self.dialog.add_buttons(
                    Gtk.STOCK_CANCEL,
                    Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_SAVE,
                    Gtk.ResponseType.OK,
                )
                # Set the current folder to 'Videos'
                self.dialog.set_current_folder(os.path.expanduser('~/Music'))
                response = self.dialog.run()
                if response == Gtk.ResponseType.CANCEL:
                    self.dialog.destroy()
                    self.button2.set_sensitive(False)
                    self.message_label.set_text("Cancel Clicked")
                elif response == Gtk.ResponseType.OK:
                    output_filename = self.dialog.get_filename()
                    if not output_filename.endswith('.mp3'):
                        self.message_label.set_text(f"Output filename does not end with .mp3.")
                    else:
                        self.message_label.set_text(f"Output file selected: {output_filename}")
                        self.dialog.destroy()
                        def cut_audio_func():
                            clip = AudioFileClip(filename).subclip(start_time, end_time)
                            clip.write_audiofile(output_filename)
                            self.button2.set_sensitive(False)
                            self.message_label.set_text(f"{output_filename}")
                            #GLib.timeout_add_seconds(0, self.destroy)
                            # Make the treeview window visible
                            #self.treeview_window.destroy()
                            #self.treeview_window.show_all()
                        audio_cut_thread = threading.Thread(target=cut_audio_func)
                        audio_cut_thread.start()
            else:
                self.message_label.set_text("No file was selected.")
        except ValueError as e:
            self.message_label.set_text(str(e))
if __name__ == "__main__":
    win = FileChooser_Cut_Audio()
    Gtk.main()