#!/bin/bash

while true; do
    # Prompt the user for input
    echo -e " \033[38;5;196m\n compile pyra_toolz\n compile pyra_termux\n compile desktop\n remove all\n exit\033[0m"
    echo -e " ____________________________\n"
    read -p " ░pyra installer░ " input

    # Run different commands based on the input
    case "$input" in
      "compile pyra_termux")
        apt install yt-dlp
        cd && mkdir ~/pyra_temp && cd ~/pyra_temp && python3 -m venv .;
        source ~/pyra_temp/bin/activate;
        pip3 install rich pyinstaller;
        apt update && apt upgrade
        cd ~/pyra_bin/pyra_tool;
        echo -e " Compiling pyra_toolz...\n";
        pyinstaller --onefile --name pyra_termux main.py;
        deactivate;
        cd && rm -rf ~/pyra_temp;
        cp -r ~/pyra_bin/pyra_tool/dist/* ~/pyra_bin/pyra_tool;
        chmod +x ~/pyra_bin/pyra_tool/pyra_termux
        rm -rf ~/pyra_bin/pyra_tool/dist && rm -rf ~/pyra_bin/pyra_tool/build;
        ;;

      "compile pyra_toolz")
        sudo apt install yt-dlp
        cd && mkdir ~/pyra_temp && cd ~/pyra_temp && python3 -m venv .;
        source ~/pyra_temp/bin/activate;
        pip3 install pyinstaller rich
        apt update && apt upgrade
        cd ~/pyra_bin/pyra_tool;
        echo -e " Compiling pyra_toolz...\n";
        pyinstaller --onefile --name pyra_toolz main.py;
        deactivate;
        cd && rm -rf ~/pyra_temp;
        cp ~/pyra_bin/pyra_tool/dist/pyra_toolz ~/pyra_bin/pyra_tool;
        chmod +x ~/pyra_bin/pyra_tool/pyra_toolz
        rm -rf ~/pyra_bin/pyra_tool/dist && rm -rf ~/pyra_bin/pyra_tool/build;
        ;;

      "compile desktop")
        echo -e " Compiling Desktop environment...\n"
        sudo add-apt-repository ppa:tomtomtom/yt-dlp && sudo apt update && sudo apt upgrade && sudo apt install yt-dlp
        sudo apt install libgtk-3-dev;
        sudo apt install libgirepository1.0-dev;
        sudo apt-get install python3-gi;
        sudo apt-get install python3-gi gobject-introspection gir1.2-gtk-3.0;
        cd && mkdir ~/pyra_temp && cd ~/pyra_temp && python3 -m venv .;
        source ~/pyra_temp/bin/activate;
        pip3 install cx-Freeze moviepy pycairo PyGObject;
        cd ~/pyra_bin/pyra_desktop_env;
        python3 pyra_desktop_setup.py build;
        cp -r ~/pyra_bin/pyra_desktop_env/build/exe.linux-x86_64-3.10/* ~/pyra_bin/pyra_desktop_env;
        rm -rf build;
        chmod +x ~/pyra_bin/pyra_desktop_env/pyra_desktop
        cd ~/pyra_bin/pyra_desktop_env/pyra_guis;
        python3 gui_editor_setup.py build;
        cp -r ~/pyra_bin/pyra_desktop_env/pyra_guis/build/exe.linux-x86_64-3.10/* ~/pyra_bin/pyra_desktop_env/pyra_guis;
        rm -rf build;
        chmod +x ~/pyra_bin/pyra_desktop_env/pyra_guis/pyra_gui_editor
        ;;

      "remove all")
        echo " Removing pyra_bin and files...\n"
        # Add your command for restarting the service
        rm -rf ~/pyra_bin
        echo -e " All Pyra directories and files removed...\n"
        ;;

      "exit")
        echo -e " Exiting the Pyra installer.\n"
        exit
        ;;
      *)
        echo -e " Invalid option. Please try again.\n"
        ;;
    esac
done
