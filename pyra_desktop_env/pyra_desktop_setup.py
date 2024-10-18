from cx_Freeze import setup, Executable


build_exe_options = {"packages": []}

setup(
    name = "Pyra Desktop",
    version = "1.0",
    description = "cli yt-dlp",
    options = {"build_exe": build_exe_options},
    executables = [Executable("pyra_desktop.py")]
)