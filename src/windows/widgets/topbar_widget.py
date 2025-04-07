from src.shared.imports import *

class TopBarWidget(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        """A QWidget object to act as the topbar in the gym window.

        Args:
            parent (QWidget): Parent of the widget, typically the gym window.
        """
        super().__init__(parent)
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
        
        self._set_design()
        self._set_widgets()
    
    def _set_design(self):
        """A function to set the design of the top bar."""
        self.setFixedSize(
            self.parentWidget().width(),
            50
        ) # Fill parent width, height of 50px.
        
        # Create a background label for the top bar.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setStyleSheet(f"background-color: {self.colour_manager.header}")
    
    def _set_widgets(self):
        """A function to load the necessary widgets into the topbar widget."""
        self.buttons = self.Buttons(self)
    
    class Buttons(QWidget):
        def __init__(
                self,
                parent: QWidget
        ) -> None:
            """A QWidget subclasses, acting as the container for all buttons related to TopBar.

            Args:
                parent (QWidget): Parent of the container, typically the top bar widget.
            """
            super().__init__(parent)
            self._set_design()
            self._set_widgets()
            self._set_layout()
            
        def _set_design(self):
            """A function to set the design of the container."""
            self.setFixedSize(self.parentWidget().size())
        
        def _set_widgets(self):
            """A function to load all the relevant widgets to the buttons container."""
            self.profile_button = self.ProfileButton(self)
            self.classes_button = self.ClassesButton(self)
            self.chat_button = self.ChatButton(self)
        
        def _set_layout(self):
            """A function to set the layout of the container."""
            self.main_layout = QHBoxLayout(self)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add the widgets to the layout.
            self.main_layout.addWidget(self.profile_button)
            self.main_layout.addWidget(self.classes_button)
            self.main_layout.addWidget(self.chat_button)
            
            self.setLayout(self.main_layout)
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        class Button(QPushButton):
            def __init__(
                    self,
                    parent: QWidget,
                    icon_src: str
            ) -> None:
                """Base class for the buttons within the top bar.

                Args:
                    parent (QWidget): Parent of the button, typically top bar.
                    icon_src (str): Source directory of the icon to apply to the button.
                """
                super().__init__(parent)
                self.icon_src = icon_src
                
                self._set_design()
            
            def _set_design(self):
                self.setFixedSize(
                    self.parentWidget().height(),
                    self.parentWidget().height()
                ) # 1:1 Ratio using top bar height.
                
                # Set the icon.
                self.setIcon(QIcon(path(self.icon_src)))
                self.setIconSize(self.size())

                # Set the style of the button.
                self.setStyleSheet(
                    "background-color: transparent;"
                    "border: none;"
                ) # Remove default button style.
        
        class ProfileButton(Button):
            def __init__(
                    self,
                    parent: QWidget
            ) -> None:
                """A profile button subcless of Button, which is a QPushButton - used for displaying the profile window.

                Args:
                    parent (QWidget): Parent widget of the QPushButton, typically the top bar.
                """
                super().__init__(parent, "/assets/icons/account.png")
                self._set_connections()
                self._set_icon()
            
            def _set_connections(self):
                """A function to add the button connections."""
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                """A function called once the button is clicked."""
                main_window : QWidget = QApplication.instance().property("MainWindow") # Get the main window object form the QApplication.
                main_window.show_profile_window()
            
            def _set_icon(self):
                """Set a new profile icon for the button"""
                # Get the members profile picture from the QApplication.
                profile_picture : QPixmap = QApplication.instance().property("EclipseProfilePicture")
                
                self.setIcon(profile_picture.scaled(self.size(), mode = Qt.TransformationMode.SmoothTransformation))

        class ClassesButton(Button):
            def __init__(
                    self,
                    parent: QWidget
            ) -> None:
                """A classes button subclass of Button, which is a QPushButton - used for displaying the classes window.

                Args:
                    parent (QWidget): Parent widget of the QPushButton, typically the top bar.
                """
                super().__init__(parent, "/assets/icons/class.png")
                self._set_connections()
            
            def _set_connections(self):
                """A function to add the button connections."""
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                """A function called once the button is clicked."""
                main_window : QWidget = QApplication.instance().property("MainWindow") # Get the main window object form the QApplication.
                main_window.show_classes_window()
        
        class ChatButton(Button):
            def __init__(
                    self,
                    parent: QWidget
            ) -> None:
                """A chat button subclass of button, which is a QPushButton - used for displaying the chat window.

                Args:
                    parent (QWidget): Parent widget of the QPushButton, typically the top bar.
                """
                super().__init__(parent, "/assets/icons/chat.png")
                self._set_connections()
            
            def _set_connections(self):
                """A function to add the button connections."""
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                """A function called once the button is clicked."""
                main_window : QWidget = QApplication.instance().property("MainWindow") # Get the main window object form the QApplication.
                main_window.show_chat_window()