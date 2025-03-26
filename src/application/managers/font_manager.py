# Third-party imports.
from PySide6.QtGui import QFont, QFontDatabase

class FontManager(QFontDatabase):
    def __init__(self):
        """A class object of QFontDatabase containing the font manager shared across the application."""
        super().__init__()