from src.shared.imports import *

# Local imports.
from src.windows.login_window import LoginWindow

class MainWindow(QWidget):
    def __init__(self):
        """A QWidget subclass containing the main window of the QApplication."""
        super().__init__()
        
        self._set_design()
        self._set_widgets()
    
    def _set_design(self):
        """A function to set the design of a QWidget."""
        self.setFixedSize(360, 640) # Low resolution mobile to fit in window.
    
        self.move_to_screen("Acer P226HQ")
    
    def _set_widgets(self):
        """A function to load widgets into the widget."""
        self.login_window = LoginWindow(self)
    
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