# Third-party imports.
from PySide6.QtGui import QFont, QFontDatabase
from src.shared.funcs import path

class FontManager(QFontDatabase):
    def __init__(self):
        """A class object of QFontDatabase containing the font manager shared across the application."""
        super().__init__()

        self.geist = Geist(self)
        
    def load_font(self, font_src: str) -> QFont:
        """A function to load a QFont from a file.
        
        Args:
            font_src (str): Path to the font file.
        """
        font_id = self.addApplicationFont(path(font_src))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        font = QFont(font_family)
        
        if "bold" in font_src.lower():
            font.setBold(True)
        
        return font        
    
class Geist:
    def __init__(self, font_manager: FontManager) -> None:
        """Class containing QFonts from the Geist font family.

        Args:
            font_manager (FontManager): FontManager object, a subclass of QFontDatabase.
        """
        self.regular = font_manager.load_font("/assets/fonts/GeistMonoNerdFont-Regular.otf")
        self.bold = font_manager.load_font("/assets/fonts/GeistMonoNerdFont-Bold.otf")