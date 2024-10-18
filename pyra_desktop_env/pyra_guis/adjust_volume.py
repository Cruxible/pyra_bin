
import os
import gi
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GLib
from moviepy.audio.fx.all import volumex
from moviepy.editor import AudioFileClip

class FileChooser_Adjust_Vol(Gtk.Window):
	def __init__(self, treeview_window):
		Gtk.Window.__init__(self, title="Adjust Volume")
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

		self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 20, 1)
		#sets the css name
		self.scale.set_name("scale")
		self.scale.set_value(10)
		self.box.pack_start(self.scale, True, True, 0)

		self.button2 = Gtk.Button(label="Adjust Volume")
		#sets the css name
		self.button2.set_name("second_button")
		self.button2.connect("clicked", self.on_adjust_clicked)
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

		self.audio_file = None

		css = """
		#first_button, #scale, #second_button, #update_Label {
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
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK
		)
		response = self.dialog.run()
		if response == Gtk.ResponseType.CANCEL:
			self.dialog.destroy()
			self.message_label.set_text("Cancel Clicked")
		elif response == Gtk.ResponseType.OK:
			self.audio_file = self.dialog.get_filename()
			self.button2.set_sensitive(True)
			self.dialog.hide()

	def on_adjust_clicked(self, widget):
		try:
			volume_level = float(self.scale.get_value())
		except ValueError:
			self.label.set_text("Volume level must be a number")
			return
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
			dialog.set_current_folder(os.path.expanduser('~/Music'))
			response = dialog.run()
			if response == Gtk.ResponseType.CANCEL:
				dialog.destroy()
				self.button2.set_sensitive(False)
				self.message_label.set_text("Cancel Clicked")
			elif response == Gtk.ResponseType.OK:
				output_filename = dialog.get_filename()
				if not output_filename.endswith('.mp3'):
					self.message_label.set_text(f"Output filename does not end with .mp3")
				else:
					self.message_label.set_text(f"{output_filename}")
					dialog.destroy()
					def adjust_vol_func():
						audio = AudioFileClip(self.audio_file)
						audio = audio.fx(volumex, volume_level)
						audio.write_audiofile(output_filename)
						self.audio_file = None
						self.button2.set_sensitive(False)
						self.message_label.set_text(f"Volume adjustment completed successfully!\n{output_filename}")
						#GLib.timeout_add_seconds(0, self.destroy)  # 5 seconds delay
						# Make the treeview window visible
						#self.treeview_window.destroy()
						#self.treeview_window.show_all()
					# Run the volume adjust in a separate thread
					adjust = threading.Thread(target=adjust_vol_func)
					adjust.start()
			else:
				self.message_label.set_text("No file was selected.")
		except Exception as e:
			self.message_label.set_text(str(e))

if __name__ == "__main__":
	win = FileChooser_Extract_Audio()
	Gtk.main()