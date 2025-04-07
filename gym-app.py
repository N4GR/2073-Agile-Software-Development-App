import os

from src.shared.startup import startup

from src.application.application import Application
from src.windows.main_window import MainWindow

if __name__ == "__main__":
    startup_error = startup()
    
    if startup_error is True:
        print("Startup error occoured, exitting launch.")
        os._exit() # Exit early.
    
    else:
        print("Startup successful, launching...")
    
    # If this is the file being ran, run the application and the main window.
    application = Application() # Load the application object.
    main_window = MainWindow() # Load the main window object.
    main_window.show() # Show the window.
    
    application.exec() # Execute the application event loop.
    