from src.imports import *

class LoginWindow(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self._set_design()
        self._set_widgets()
        self._set_layout()
    
    def _set_design(self):
        self.setFixedSize(500, 500)
    
    def _set_widgets(self):
        self.username = self.Username(self)
        self.password = self.Password(self)
        
        self.buttons = self.Buttons(self)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.main_layout.addWidget(self.username)
        self.main_layout.addWidget(self.password)
        self.main_layout.addWidget(self.buttons)
        
        self.setLayout(self.main_layout)
    
    class TextEntry(QWidget):
        def __init__(
                self,
                parent: QWidget,
                name: str
        ):
            super().__init__(parent)
            self.name = name
            
            self._set_design()
            self._set_widgets()
            self._set_layout()
        
        def _set_design(self):
            self.setFixedHeight(100)
        
        def _set_widgets(self):
            self.label = self.Label(self, self.name)
            self.text_edit = self.TextEdit(self, self.name)
        
        def _set_layout(self):
            self.main_layout = QVBoxLayout()
            self.main_layout.setSpacing(0)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            
            self.main_layout.addWidget(self.label)
            self.main_layout.addWidget(self.text_edit)
            
            self.setLayout(self.main_layout)

        class Label(QLabel):
            def __init__(
                    self,
                    parent: QWidget,
                    name: str
            ):
                super().__init__(parent)
                self.name = name
                
                self.setFixedHeight(50)
                self.setText(self.name)
        
        class TextEdit(QTextEdit):
            def __init__(
                    self,
                    parent: QWidget,
                    name: str
            ):
                super().__init__(parent)
                self.name = name
                
                self.setFixedHeight(50)
                self.setPlaceholderText(self.name)
    
    class Username(TextEntry):
        def __init__(self, parent: QWidget):
            super().__init__(parent, "Username")
    
    class Password(TextEntry):
        def __init__(self, parent: QWidget):
            super().__init__(parent, "Password")
    
    class Buttons(QWidget):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._set_design()
            self._set_widgets()
            self._set_layout()
        
        def _set_design(self):
            self.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed
            )
            
            self.setFixedHeight(50)
        
        def _set_widgets(self):
            pass
        
        def _set_layout(self):
            self.main_layout = QHBoxLayout()
            
            self.main_layout.addWidget(self.login_button)
            self.main_layout.addWidget(self.register_button)
            
            self.setLayout(self.main_layout)
        
        class Button(QPushButton):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
        
        class LoginButton(Button):
            def __init__(self, parent: QWidget):
                super().__init__(parent)