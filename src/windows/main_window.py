from src.imports import *

# Local imports.
from src.windows.widgets.login_window import LoginWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self._set_design()
        self._set_widgets()
        self.show()
    
    def _set_design(self):
        self.background = self.Background(self)

        self.setMinimumSize(800, 600)
        self.background.setFixedSize(self.size())
    
    def _set_widgets(self):
        self.login_window = LoginWindow(self)
    
    def resizeEvent(self, event: QResizeEvent):
        def resize_to_window(widget: QWidget):
            try:
                widget.setFixedSize(self.size())
            
            except AttributeError: # Widget reference hasn't been created yet.
                pass
            
            except RuntimeError: # Widget has been deleted during runtime.
                pass
        
        resize_to_window(self.background)
        
        return super().resizeEvent(event)
    
    class Background(QLabel):
        def __init__(
                self,
                parent: QWidget
        ):
            super().__init__(parent)
            self._set_design()
        
        def _set_design(self):
            self.setStyleSheet(
                "background-color: red;"
            )