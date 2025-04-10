import os

from src.shared.startup import startup
from src.shared.testing_data import TestingData

from src.application.application import Application
from src.windows.main_window import MainWindow

if __name__ == "__main__":
    # Startup function - used to check if everything is running on to continue with the application.
    startup_error = startup()
    
    if startup_error is True:
        print("Startup error occoured, exitting launch.")
        os._exit(1) # Exit early.
    
    else:
        print("Startup successful, launching...")
    
    # Load the testing data.
    testing_data = TestingData()
    
    # If this is the file being ran, run the application and the main window.
    application = Application() # Load the application object.
    main_window = MainWindow() # Load the main window object.
    main_window.show() # Show the window.
    
    application.exec() # Execute the application event loop.
    