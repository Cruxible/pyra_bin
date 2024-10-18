import os
import gi
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GLib
from moviepy.editor import VideoFileClip, AudioFileClip

class FileChooser_Merge(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Merge Audio/Video")
        self.set_default_size(450, 300)

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)
        self.connect("delete-event", Gtk.main_quit)

        # Create a vertical box
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.button1 = Gtk.Button(label="Choose Video")
        #sets the css name
        self.button1.set_name("first_button")
        self.button1.connect("clicked", self.on_file_clicked)
        self.box.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.Button(label="Choose Audio")
        #sets the css name
        self.button2.set_name("second_button")
        self.button2.connect("clicked", self.on_file_clicked)
        self.box.pack_start(self.button2, True, True, 0)

        self.button3 = Gtk.Button(label="Merge Files")
        #sets the css name
        self.button3.set_name("third_button")
        self.button3.connect("clicked", self.on_merge_clicked)
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

        self.video_file = None
        self.audio_file = None

        css = """
        #first_button, #second_button, #third_button, #update_Label {
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
        if widget.get_label() == 'Choose Video':
            self.dialog.set_current_folder(os.path.expanduser('~/Videos'))
        elif widget.get_label() == 'Choose Audio':
            self.dialog.set_current_folder(os.path.expanduser('~/Music'))
        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )
        response = self.dialog.run()
        if response == Gtk.ResponseType.CANCEL:
            self.dialog.destroy()
            self.message_label.set_text("Cancel Clicked")
        elif response == Gtk.ResponseType.OK:
            if widget.get_label() == 'Choose Video':
                self.video_file = self.dialog.get_filename()
            elif widget.get_label() == 'Choose Audio':
                self.audio_file = self.dialog.get_filename()
                self.button3.set_sensitive(True)
        self.dialog.destroy()

    def on_merge_clicked(self, widget):
        try:
            dialog = Gtk.FileChooserDialog(
                title="Please choose a file", 
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
            response = dialog.run()
            if response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                self.button3.set_sensitive(False)
                self.message_label.set_text("Cancel clicked")
            elif response == Gtk.ResponseType.OK:
                output_filename = dialog.get_filename()
                if not output_filename.endswith('.mp4'):
                    self.message_label.set_text(f"Output filename does not end with .mp4")
                else:
                    self.message_label.set_text(f"{output_filename}")
                    dialog.destroy()
                    def merge_func():
                        video = VideoFileClip(self.video_file)
                        audio = AudioFileClip(self.audio_file)
                        final_clip = video.set_audio(audio)
                        final_clip.write_videofile(output_filename)
                        self.video_file = None
                        self.audio_file = None
                        self.button3.set_sensitive(False)
                        self.message_label.set_text(f"{output_filename}")
                        #GLib.timeout_add_seconds(0, self.destroy)  # 5 seconds delay
                        # Make the treeview window visible
                        #self.treeview_window.destroy()
                        #self.treeview_window.show_all()
                        
                    # Run the video player in a separate thread
                    merge_func = threading.Thread(target=merge_func)
                    merge_func.start()
            else:
                self.message_label.set_text("No file was selected.")
            
        except ValueError as e:
            self.message_label.set_text(str(e))

if __name__ == "__main__":
    win = FileChooser_Cut_Vid()
    Gtk.main()