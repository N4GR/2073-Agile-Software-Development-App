from src.shared.imports import *

### Local imports.
# Window imports.
from src.windows.login_window import LoginWindow
from src.windows.gym_window import GymWindow
from src.windows.profile_window import ProfileWindow
from src.windows.classes_window import ClassesWindow
from src.windows.chat_window import ChatWindow
from src.windows.billing_window import BillingWindow
from src.windows.current_classes_window import CurrentClassesWindow

class MainWindow(QWidget):
    def __init__(self):
        """A QWidget subclass containing the main window of the QApplication."""
        super().__init__()
        # Add a property to QApplication, making this widget the main window.
        QApplication.instance().setProperty("MainWindow", self)
        
        self.application_name = "Gymify"
        
        self.current_window : QWidget = None # Storage for the current window showing.
        
        self._set_design()
        self._set_widgets()
    
    def _set_design(self):
        """A function to set the design of a QWidget."""
        self.setFixedSize(360, 640) # Low resolution mobile to fit in window.
        
        # Set the window title.
        self.setWindowTitle(self.application_name)
        
        # Set the window icon.
        self.setWindowIcon(QPixmap(path("/assets/logo.png")))
    
        #self.move_to_screen("Acer P226HQ")
    
    def _set_widgets(self):
        """A function to load widgets into the widget."""
        self.login_window = LoginWindow(self)
        
        self.current_window = self.login_window # Set the current window to the login window.
        
        # Change the window title to reflect new window.
        self.setWindowTitle(f"{self.application_name} - Login")
    
    def login_member(self, member: Member) -> None:
        """Function to log a user into the application.

        Args:
            member (Member): Member logging in.
        """
        print(f"Logging in user: {member}")
        
        # Set a property to QApplication, adding the currently logged in member to be accessed globally.
        QApplication.instance().setProperty("LoggedMember", member)
        
        # Create a random profile image for the user and set it to a property in QApplication.
        user_profile = QPixmap(path(f"/assets/profiles/{member.profile}"))
        QApplication.instance().setProperty("ProfilePicture", user_profile)
        
        # Crop the profile into an eclipse and set set it as a property too.
        eclipse_profile = circular_pixmap(user_profile)
        QApplication.instance().setProperty("EclipseProfilePicture", eclipse_profile)
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the gym window.
        self.gym_window = GymWindow(self)
        self.current_window = self.gym_window # Set the current window to the gym window.
    
    def logout_member(self) -> None:
        """A function to log out a user from the application, returning back to login menu."""
        print("Showing login window.")
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the login window.
        self.login_window = LoginWindow(self)
        
        # Change the window title to reflect new window.
        self.setWindowTitle(f"{self.application_name} - Login")
        
        # Set the current window.
        self.current_window = self.login_window
    
    def show_profile_window(self):
        """A function to show the profile window."""
        print("Showing profile window.")
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the profile window.
        self.profile_window = ProfileWindow(self)
        
        # Change the window title to reflect new window.
        self.setWindowTitle(f"{self.application_name} - Profile")
        
        # Set the current window.
        self.current_window = self.profile_window
    
    def show_classes_window(self):
        """A function to show the classes window."""
        print("Showing the classes window.")
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the classes window.
        self.classes_window = ClassesWindow(self)
        
        # Change the window title to reflect new window.
        self.setWindowTitle(f"{self.application_name} - Classes")
        
        # Set the current window.
        self.current_window = self.classes_window

    def show_chat_window(self):
        """A function to show the chat window."""
        print("Showing the chat window.")
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the chat window.
        self.chat_window = ChatWindow(self)
        
        # Change the window title to reflect new window.
        self.setWindowTitle(f"{self.application_name} - Chat")
        
        # Set the current window.
        self.current_window = self.chat_window
    
    def show_billing_window(self):
        """A function to show the billing window."""
        print("Showing the billing window.")
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the billing window.
        self.billing_window = BillingWindow(self)
        
        # Change the window title to reflect new window.
        self.setWindowTitle(f"{self.application_name} - Billing")
        
        # Set the current window.
        self.current_window = self.billing_window
    
    def show_current_classes_window(self):
        """A function to show the current classes window."""
        print("Showing the current classes window.")
        
        # Delete the current window being displayed.
        self.current_window.deleteLater()
        
        # Create the current classes window.
        self.current_classes_window = CurrentClassesWindow(self)
        
        # Change the window title to reflect new window.
        self.setWindowTitle(f"{self.application_name} - Current Classes")
        
        # Set the current window.
        self.current_window = self.current_classes_window

    def move_to_screen(self, name: str):
        """A function to move the widget to a different screen with a given name.

        Args:
            name (str): Name of the screen to move to.
        """
        for screen in QApplication.screens(): # Iterate through application screens.
            if screen.name() == name:
                screen_centre = screen.geometry().center() # Centre point of screen.
                
                # Centre point of the screen with the widget in the centre.
                centre = QPoint(screen_centre.x() - (self.width() / 2), screen_centre.y() - (self.height() / 2))
                
                self.move(centre) # Move to adjusted centre point.