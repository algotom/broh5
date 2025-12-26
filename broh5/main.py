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


def handle_shutdown(main_app):
    """
    Handle the shutdown process of the application.
    """
    if main_app is not None:
        main_app.shutdown()
    print("\n===============")
    print(" Exit the app!")
    print("===============\n")


def signal_handler(*args):
    """
    Handle the signal for graceful shutdown of the application.

    Parameters
    ----------
    *args
        Variable length argument list.
    """
    sys.exit(0)


def check_port(port):
    """
    Check if a given port is available.

    Parameters
    ----------
    port : int
        The port number to check.

    Returns
    -------
    bool
        True if the port is already in use, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def parse_args():
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments.
    """
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
    """
    Main function to start the application.
    """
    args = parse_args()
    if check_port(args.port):
        print("\n!!! Port {} is already in use. Please specify a "
              "different port using --port !!!\n".format(args.port))
        sys.exit(1)
    signal.signal(signal.SIGINT, signal_handler)  # Back-up shutdown
    try:
        broh5_app = None

        @ui.page('/')
        def main_page():
            global broh5_app
            broh5_app = GuiInteraction()

        app.on_shutdown(lambda: handle_shutdown(broh5_app))
        os.environ["NO_NETIFACES"] = "True"
        app.on_startup(
            lambda: print("Access Broh5 at urls: {}".format(app.urls.union())))
        ui.run(reload=False, title="Browser-based Hdf Viewer", port=args.port,
               show_welcome_message=False)
    except Exception as error:
        print(f"An error occurred: {error}")
        sys.exit(0)


if __name__ in {"__main__", "__mp_main__"}:
    main()
