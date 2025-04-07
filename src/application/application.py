# Third-Party imports.
from PySide6.QtWidgets import QApplication

# Local imports.
from src.application.managers.font_manager import FontManager
from src.application.managers.database_manager import DatabaseManager
from src.application.managers.colour_manager import ColourManager

class Application(QApplication):
    def __init__(self):
        """Class object to handle attributes shared across the entire application."""
        super().__init__()
    
        self.load_managers()
        self.set_properties()
    
    def load_managers(self):
        """A function to load the managers into the application object; to avoid python cleaning."""
        self.font_manager = FontManager()
        self.database_manager = DatabaseManager # Don't initialise it!
        self.colour_manager = ColourManager()
    
    def set_properties(self):
        """A function to set the properties of the managers to the application so they can be accessed within the application runtime."""
        self.setProperty("FontManager", self.font_manager)
        self.setProperty("DatabaseManager", self.database_manager)
        self.setProperty("ColourManager", self.colour_manager)
    
    def setProperty(self, name, value):
        print(f"QAPPLICATION | PROPERTY ADD | {name}, {value}")
        
        return super().setProperty(name, value)

    def property(self, name):
        print(f"QAPPLICATION | PROPERTY GET | {name}")
        
        return super().property(name)