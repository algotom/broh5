import os
import sys
import signal
import socket
import argparse
from nicegui import ui, app
from broh5.lib.interactions import GuiInteraction
from broh5 import __version__

display_msg = """
===============================================================================

Web-browser-based GUI (Graphical User Interface) software for viewing HDF files

===============================================================================

Type: broh5 to run the software
Exit the software by pressing: Ctrl + C

===============================================================================
"""


def handle_shutdown():
    print("\n===============")
    print(" Exit the app!")
    print("===============\n")


def signal_handler(*args):
    handle_shutdown()
    sys.exit(0)


def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def parse_args():
    parser = argparse.ArgumentParser(description=display_msg,
                                     formatter_class=
                                     argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    parser.add_argument("--port", type=int, default=8180,
                        help="Specify the port to run broh5 on "
                             "(default: 8180)")
    args = parser.parse_args()
    return args


def main():
    signal.signal(signal.SIGINT, signal_handler)
    args = parse_args()
    if check_port(args.port):
        print("\n!!! Port {} is already in use. Please specify a "
              "different port using --port !!!\n".format(args.port))
        sys.exit(1)
    GuiInteraction()
    os.environ["NO_NETIFACES"] = "True"
    app.on_shutdown(handle_shutdown)
    ui.run(reload=False, title="Browser-based Hdf Viewer", port=args.port)


if __name__ in {"__main__", "__mp_main__"}:
    main()
