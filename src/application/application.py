from PySide6.QtWidgets import QApplication

# Local imports.
from src.application.modules.font_manager import FontManager

class Application(QApplication):
    def __init__(
            self,
            args: str
    ):
        super().__init__(args)
        
        self._load_modules()
        self._load_properties()
    
    def _load_modules(self):
        self.font_manager = FontManager()
    
    def _load_properties(self):
        self.setProperty("FontManager", self.font_manager)