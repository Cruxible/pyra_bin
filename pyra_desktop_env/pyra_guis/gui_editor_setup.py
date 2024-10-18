from cx_Freeze import setup, Executable
import os

def make_executable():
    build_exe_options = {"packages": ["gi", "moviepy"]}
    setup(
        name = "Pyra Gui Editor",
        version = "2.0",
        description = "Downloader/Video Editor Gui",
        options = {"build_exe": build_exe_options},
        executables = [
                      Executable("pyra_gui_editor.py"),
                      Executable("pyra_downloader.py"),
                      Executable("cut_video.py"),
                      Executable("cut_audio.py"),
                      Executable("merge_aud_vid.py"),
                      Executable("extract_audio.py"),
                      Executable("adjust_volume.py"),
                      Executable("concat_vid.py"),
                      Executable("concat_aud.py"),
                      ]
    )

make_executable()