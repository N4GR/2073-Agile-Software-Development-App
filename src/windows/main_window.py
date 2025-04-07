from src.shared.imports import *

### Local imports.
# Window imports.
from src.windows.login_window import LoginWindow
from src.windows.gym_window import GymWindow
from src.windows.profile_window import ProfileWindow
from src.windows.classes_window import ClassesWindow

# Widget imports.
from src.windows.widgets.header_widget import HeaderWidget

class MainWindow(QWidget):
    def __init__(self):
        """A QWidget subclass containing the main window of the QApplication."""
        super().__init__()
        # Add a property to QApplication, making this widget the main window.
        QApplication.instance().setProperty("MainWindow", self)
        
        self.current_window : QWidget = None # Storage for the current window showing.
        
        self._set_design()
        self._set_widgets()
    
    def _set_design(self):
        """A function to set the design of a QWidget."""
        self.setFixedSize(360, 640) # Low resolution mobile to fit in window.
        
        # Set the window title.
        self.setWindowTitle("Gymify")
    
        self.move_to_screen("Acer P226HQ")
    
    def _set_widgets(self):
        """A function to load widgets into the widget."""
        self.login_window = LoginWindow(self)
        self.header = HeaderWidget(self)
        
        self.current_window = self.login_window # Set the current window to the login window.
    
    def login_member(
            self,
            member: Member
    ) -> None:
        """Function to log a user into the application.

        Args:
            member (Member): Member logging in.
        """
        print(f"Logging in user: {member}")
        
        # Set a property to QApplication, adding the currently logged in member to be accessed globally.
        QApplication.instance().setProperty("LoggedMember", member)
        
        # Create a random profile image for the user and set it to a property in QApplication.
        random_profile = get_random_profile_pixmap()
        QApplication.instance().setProperty("ProfilePicture", random_profile)
        
        # Crop the profile into an eclipse and set set it as a property too.
        eclipse_profile = circular_pixmap(random_profile)
        QApplication.instance().setProperty("EclipseProfilePicture", eclipse_profile)
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Delete the header.
        self.header.deleteLater()
        
        # Create the gym window.
        self.gym_window = GymWindow(self)
        self.current_window = self.gym_window # Set the current window to the gym window.
    
    def show_profile_window(self):
        """A function to show the profile window."""
        print("Showing profile window.")
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the profile window.
        self.profile_window = ProfileWindow(self)
        
        # Set the current window.
        self.current_window = self.profile_window
    
    def show_classes_window(self):
        """A function to show the classes window."""
        print("Showing the classes window.")
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the profile window.
        self.classes_window = ClassesWindow(self)
        
        # Set the current window.
        self.current_window = self.classes_window

    def move_to_screen(
            self,
            name: str
    ):
        """A function to move the widget to a different screen with a given name.

        Args:
            name (str): Name of the screen to move to.
        """
        for screen in QApplication.screens(): # Iterate through application screens.
            if screen.name() == name:
                screen_centre = screen.geometry().center() # Centre point of screen.
                centre = QPoint(
                    screen_centre.x() - (self.width() / 2),
                    screen_centre.y() - (self.height() / 2)
                ) # Centre point of the screen with the widget in the centre.
                
                self.move(centre) # Move to adjusted centre point.