from src.shared.imports import *

# Local imports.
from src.windows.widgets.topbar_widget import TopBarWidget

class ProfileWindow(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        """A subclass of QWidget, acting as the profile window widget.

        Args:
            parent (QWidget): Parent of the profile window, typically the main window.
        """
        super().__init__(parent)
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
    
        self._set_design()
        self._set_widgets()
        
        # Show the window.
        self.show()
        
    def _set_design(self):
        """A function to set the design of the profile window."""
        self.setFixedSize(self.parentWidget().size()) # Fill main window.
        
        # Set background as static colour.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setStyleSheet(f"background-color: {self.colour_manager.background}")
    
    def _set_widgets(self):
        """A function to load the neccesary widgets into the profile window."""
        self.top_bar = TopBarWidget(self) # Top bar.
        self.info_container = self.InfoContainer(self)
        self.bottom_bar = self.BottomBar(self)
    
    class InfoContainer(QWidget):
        def __init__(self, parent: QWidget):
            """A QWidget subclass, containing the information about the logged in member."""
            super().__init__(parent)
            self._set_design()
            self._set_widgets()
            self._set_layout()
            self._update_design()
        
        def _set_design(self):
            self.setFixedWidth(self.parentWidget().width())
        
        def _set_widgets(self):
            self.profile_image_label = self.ProfileImage(self)
            self.name_label = self.NameLabel(self)
            self.email_label = self.EmailLabel(self)
            self.phone_label = self.PhoneLabel(self)
        
        def _set_layout(self):
            self.main_layout = QVBoxLayout()
            
            # Add the widgets to the layout.
            self.main_layout.addWidget(self.profile_image_label, alignment = Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(self.name_label, alignment = Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(self.email_label, alignment = Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(self.phone_label, alignment = Qt.AlignmentFlag.AlignCenter)
            
            self.setLayout(self.main_layout)
        
        def _update_design(self):
            """A function to be called once the widgets have been added, for resizing and moving relative to new size."""
            self.setFixedHeight(self.sizeHint().height()) # Set the height of the widget relative to the items within the layout.
            
            # Move the container to the centre of the profile window.
            self.move(
                0,
                (self.parentWidget().height() / 2)
                - (self.height() / 2)
            )
    
        class ProfileImage(QLabel):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
                self.setFixedSize(200, 200)
                
                # Get the members profile picture from the QApplication.
                profile_picture : QPixmap = QApplication.instance().property("EclipseProfilePicture")
                
                self.setPixmap(profile_picture.scaled(self.size(), mode = Qt.TransformationMode.SmoothTransformation))
        
        class NameLabel(QLabel):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
                logged_member : Member = QApplication.instance().property("LoggedMember") # Get the logged in member from QApplication.
                colour_manager : ColourManager = QApplication.instance().property("ColourManager") # Get the colour manager from QApplication.
                font_manager : FontManager = QApplication.instance().property("FontManager") # Get the font manager from QApplication.

                self.setText(f"{logged_member.forename.capitalize()} {logged_member.surname.capitalize()}") # Set to the users full name.
                
                # Set the font.
                self.setFont(font_manager.geist.bold) # Create a new instance of the font.
                font = self.font()
                font.setPointSize(15) # Set the size of the font.
                self.setFont(font)
                
                # Set the design of the label.
                self.setStyleSheet(
                    f"color: {colour_manager.text};" # Text colour.
                )
        
        class EmailLabel(QLabel):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
                logged_member : Member = QApplication.instance().property("LoggedMember") # Get the logged in member from QApplication.
                colour_manager : ColourManager = QApplication.instance().property("ColourManager") # Get the colour manager from QApplication.
                font_manager : FontManager = QApplication.instance().property("FontManager") # Get the font manager from QApplication.

                self.setText(f"{logged_member.email}") # Set to the users email.
                
                # Set the font.
                self.setFont(font_manager.geist.regular) # Create a new instance of the font.
                font = self.font()
                font.setPointSize(10) # Set the size of the font.
                self.setFont(font)
                
                # Set the design of the label.
                self.setStyleSheet(
                    f"color: {colour_manager.text};" # Text colour.
                )
        
        class PhoneLabel(QLabel):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
                logged_member : Member = QApplication.instance().property("LoggedMember") # Get the logged in member from QApplication.
                colour_manager : ColourManager = QApplication.instance().property("ColourManager") # Get the colour manager from QApplication.
                font_manager : FontManager = QApplication.instance().property("FontManager") # Get the font manager from QApplication.

                self.setText(f"{logged_member.phone}") # Set to the users phone number.
                
                # Set the font.
                self.setFont(font_manager.geist.regular) # Create a new instance of the font.
                font = self.font()
                font.setPointSize(10) # Set the size of the font.
                self.setFont(font)
                
                # Set the design of the label.
                self.setStyleSheet(
                    f"color: {colour_manager.text};" # Text colour.
                )

    class BottomBar(QWidget):
        def __init__(self, parent: QWidget):
            """A function containing the bottom bar, which will have buttons for the profile."""
            super().__init__(parent)
            self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
            
            self._set_design()
            self._set_widgets()
            self._set_layout()
        
        def _set_design(self):
            self.setFixedSize(
                self.parentWidget().width(),
                50
            ) # Set to the width of the parent, with 50px height.
            
            # Move the bar to the bottom of the screen.
            self.move(
                0,
                self.parentWidget().height()
                - self.height()
            )
            
            # Add a background to the bottom bar.
            self.background_widget = QLabel(self)
            self.background_widget.setFixedSize(self.size())
            self.background_widget.setStyleSheet(f"background-color: {self.colour_manager.header}")
        
        def _set_widgets(self):
            self.billing_button = self.BillingButton(self)
            self.current_classes_button = self.CurrentClassesButton(self)
        
        def _set_layout(self):
            self.main_layout = QHBoxLayout()
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add the widgets to the layout.
            self.main_layout.addWidget(self.billing_button)
            self.main_layout.addWidget(self.current_classes_button)
            
            self.setLayout(self.main_layout)
        
        class Button(QPushButton):
            def __init__(
                    self,
                    parent: QWidget,
                    icon_src: str
            ):
                """Subclass of QPushButton, made to be the subclass of buttons within the bottom bar."""
                super().__init__(parent)
                size = min(self.parentWidget().height(), self.parentWidget().width())
                self.setFixedSize(size, size) # 1:1 from parent.
                
                self.setIcon(QPixmap(path(icon_src)))
                self.setIconSize(self.size()) # Fill button.
    
                # Set the style of the button.
                self.setStyleSheet(
                    "background-color: transparent;"
                    "border: none;"
                ) # Remove default button style.
        
        class BillingButton(Button):
            def __init__(self, parent: QWidget):
                """Subclass of button, acting as the billing button to show the billing window."""
                super().__init__(parent, "/assets/icons/receipt.png")
                self._set_connections()
            
            def _set_connections(self):
                """A function to add connections to the button."""
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                main_window : QWidget = QApplication.instance().property("MainWindow")
                
                main_window.show_billing_window()
        
        class CurrentClassesButton(Button):
            def __init__(self, parent: QWidget):
                """Subclass of button, acting as the current lessons button to show the current lessons window."""
                super().__init__(parent, "/assets/icons/class.png")
                self._set_connections()
            
            def _set_connections(self):
                """A function to add connections to the button."""
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                main_window : QWidget = QApplication.instance().property("MainWindow")
                
                main_window.show_current_classes_window()