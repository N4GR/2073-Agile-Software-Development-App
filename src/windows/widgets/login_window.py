from src.imports import *

class LoginWindow(QWidget):
    def __init__(
            self,
            parent: QWidget
    ):
        super().__init__(parent)
        self._set_design()
    
    def _set_design(self):
        self.background = self.Background(self)
        self.setFixedSize(self.parentWidget().size())
    
    def resizeEvent(self, event: QResizeEvent):
        self.background.setFixedSize(self.size())
        
        return super().resizeEvent(event)
    
    class Background(QLabel):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._set_design()
        
        def _set_design(self):
            self.setFixedSize(self.parentWidget().size())