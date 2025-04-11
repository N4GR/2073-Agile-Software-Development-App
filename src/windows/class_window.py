from src.shared.imports import *

# Local imports.
from src.windows.widgets.topbar_widget import TopBarWidget

class ClassWindow(QWidget):
    def __init__(self, parent: QWidget, available_class: AvailableClass) -> None:
        """A subclass of QWidget, acting as the class window widget.

        Args:
            parent (QWidget): Parent of the class window, typically the main window.
        """
        super().__init__(parent)
        self.available_class = available_class
        self.tutor_member = self.get_tutor_member(self.available_class.tutor_id)
        
        self._set_design()
        self._set_widgets()
        self._set_layout()
        
        # Show the window.
        self.show()
        
    def _set_design(self):
        """A function to set the design of the class window."""
        self.setFixedSize(self.parentWidget().size()) # Fill main window.
        
        # Get the background and set it.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setPixmap(
            QPixmap(
                path("/assets/panels/background_gradient.png")
            ).scaled(
                self.size(),
                aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                mode = Qt.TransformationMode.SmoothTransformation
            )
        )
    
    def _set_widgets(self):
        """A function to load the neccesary widgets into the class window."""
        self.top_bar = TopBarWidget(self) # Top bar.
    
        self.tutor_profile = self.TutorProfile(self, path(f"/assets/profiles/{self.tutor_member.profile}"))
        self.class_title = self.ClassTitle(self, self.available_class.title)
        self.start_date = self.StartDateLabel(self, str(self.available_class.start_date))
        self.description_label = self.DescriptionLabel(self, self.available_class.description)
        
        self.buttons = self.Buttons(self)
    
        self.error_label = self.ErrorLabel(self)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addWidget(self.class_title, alignment = Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.tutor_profile, alignment = Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.start_date, alignment = Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.description_label, alignment = Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.buttons, alignment = Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.error_label, alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.main_layout)
    
    def get_tutor_member(self, tutor_id: int) -> Member:
        database_manager : DatabaseManager = get_property("DatabaseManager")(path("/data/gym.sqlite"))
        
        return database_manager.get_member(tutor_id)
    
    class TutorProfile(QLabel):
        def __init__(self, parent: QWidget, src: str):
            super().__init__(parent)
            self.src = src
            
            self._set_design()
        
        def _set_design(self):
            self.setFixedSize(200, 200)
            
            self.setPixmap(
                circular_pixmap(
                    QPixmap(
                        path(self.src)
                    ).scaled(
                        self.size(),
                        aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                        mode = Qt.TransformationMode.SmoothTransformation
                    )
                )
            )
            
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    class ClassTitle(QLabel):
        def __init__(self, parent: QWidget, title: str):
            super().__init__(parent, text = title)
            self.font_manager : FontManager = get_property("FontManager")
            
            self._set_design()
            self._set_font()
        
        def _set_design(self):
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.setStyleSheet("color: white;")
        
        def _set_font(self):
            self.setFont(self.font_manager.geist.bold)
            font = self.font()
            font.setPointSize(30)
            self.setFont(font)
    
    class StartDateLabel(QLabel):
        def __init__(self, parent: QWidget, start_date: str):
            super().__init__(parent, text = start_date)
            self.font_manager : FontManager = get_property("FontManager")
            
            self._set_design()
            self._set_font()
        
        def _set_design(self):
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        def _set_font(self):
            self.setFont(self.font_manager.geist.regular)
            font = self.font()
            font.setPointSize(15)
            self.setFont(font)
    
    class DescriptionLabel(QLabel):
        def __init__(self, parent: QWidget, description: str):
            super().__init__(parent, text = description)
            self.font_manager : FontManager = get_property("FontManager")
            
            self._set_design()
            self._set_font()
        
        def _set_design(self):
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.setStyleSheet("color: white;")
        
        def _set_font(self):
            self.setFont(self.font_manager.geist.regular)
            font = self.font()
            font.setPointSize(10)
            self.setFont(font)
    
    class ErrorLabel(QLabel):
        def __init__(self, parent: QWidget):
            super().__init__(parent, text = "ERROR")
            self.font_manager : FontManager = get_property("FontManager")
            
            self._set_design()
            self._set_font()
        
        def _set_design(self):
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
            self.setStyleSheet("color: red;")
            
            # Start the widget hidden.
            self.hide()
        
        def _set_font(self):
            self.setFont(self.font_manager.geist.regular)
            font = self.font()
            font.setPointSize(10)
            self.setFont(font)
    
    class Buttons(QWidget):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._set_design()
            self._set_widget()
            self._set_layout()
        
        def _set_design(self):
            pass
        
        def _set_widget(self):
            self.return_button = self.ReturnButton(self)
            self.apply_button = self.ApplyButton(self)
        
        def _set_layout(self):
            self.main_layout = QHBoxLayout()
            
            self.main_layout.addWidget(self.return_button)
            self.main_layout.addWidget(self.apply_button)
            
            self.setLayout(self.main_layout)
        
        class Button(QPushButton):
            def __init__(self, parent: QWidget, icon_src: str):
                super().__init__(parent)
                self.setFixedSize(100, 100)
                self.setIcon(QPixmap(path(icon_src)))
                self.setIconSize(self.size())
                
                self.setStyleSheet("background-color: transparent; border: none")
        
        class ReturnButton(Button):
            def __init__(self, parent: QWidget):
                super().__init__(parent, path("/assets/icons/logout.png"))
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                main_window = get_property("MainWindow")
                main_window.show_classes_window()
        
        class ApplyButton(Button):
            def __init__(self, parent: QWidget):
                super().__init__(parent, path("/assets/icons/add.png"))
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                buttons = self.parentWidget()
                window = buttons.parentWidget()
                available_class : AvailableClass = window.available_class
                error_label : QLabel = window.error_label
                logged_member : Member = get_property("LoggedMember")
                database_manager : DatabaseManager = get_property("DatabaseManager")(path("/data/gym.sqlite"))
                tutor_member : Member = database_manager.get_member(available_class.tutor_id)
                
                # Check if user is already in the class or not.
                # Get updated class value.
                applying_class = database_manager.get_class(available_class.id)
                
                if logged_member.id in applying_class.applied_members:
                    error_label.setText("YOU'RE ALREADY IN THE CLASS")
                    error_label.show()

                    return # Return early.
                
                # Add the member to the class.
                database_manager.add_member_to_class(logged_member, available_class)
                
                # Create a new chat with the tutor.
                class_database : DatabaseManager = get_property("DatabaseManager")(path("/data/chat.sqlite"))
                class_database.create_chat(logged_member, tutor_member)
                
                # Get the chat created.
                new_chat = class_database.get_personal_chat(tutor_member, logged_member)
                class_database.add_message(
                    new_chat,
                    Message(
                        tutor_member,
                        (
                            f"Hey, {logged_member.forename.capitalize()}! "
                            f"You applied for {applying_class.title}, "
                            f"please attend on: {str(applying_class.start_date)}"
                        )
                    )
                )