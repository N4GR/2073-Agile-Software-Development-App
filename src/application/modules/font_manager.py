from PySide6.QtGui import (
    QFont, QFontDatabase
)

from src.shared.funcs import *

class FontManager(QFontDatabase):
    def __init__(self):
        super().__init__()
        
        self.caskaydia = self.Caskaydia(self)

    class Caskaydia:
        def __init__(
                self,
                font_manager = QFontDatabase
        ):
            self.font_manager = font_manager

            self.bold = self.get_font(path("/assets/fonts/CaskaydiaCoveNerdFont-Bold.ttf"))
            self.light = self.get_font(path("/assets/fonts/CaskaydiaCoveNerdFont-Light.ttf"))
            self.regular = self.get_font(path("/assets/fonts/CaskaydiaCoveNerdFont-Regular.ttf"))
        
        def get_font(self, src: str):
            font_id = self.font_manager.addApplicationFont(src)
            font_family = self.font_manager.applicationFontFamilies(font_id)[0]
            
            return QFont(font_family)
            