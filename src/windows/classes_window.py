from src.shared.imports import *

# Local imports.
from src.windows.widgets.topbar_widget import TopBarWidget

class ClassesWindow(QWidget):
    def __init__(self, parent: QWidget) -> None:
        """A subclass of QWidget, acting as the classes window widget.

        Args:
            parent (QWidget): Parent of the classes window, typically the main window.
        """
        super().__init__(parent)
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
    
        self._set_design()
        self._set_widgets()
        
        # Show the window.
        self.show()
        
    def _set_design(self):
        """A function to set the design of the classes window."""
        self.setFixedSize(self.parentWidget().size()) # Fill main window.
        
        # Set background
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
        """A function to load the neccesary widgets into the classes window."""
        self.top_bar = TopBarWidget(self) # Top bar.
        self.classes = ClassesWidget(self)

class ClassesWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_design()
        self._set_layout()
        
        self.add_available_classes()

    def _set_design(self):
        top_bar : TopBarWidget = self.parentWidget().top_bar
        
        # Size of window accounting for the top bar.
        self.setFixedSize(self.parentWidget().width(), self.parentWidget().height() - top_bar.height())
        
        self.move(0, top_bar.height()) # Just under the top_bar.
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.content_widget = QWidget(self)
        self.content_widget.setFixedWidth(self.width())
        self.content_widget.setStyleSheet("background-color: transparent;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 10, 5, 0)
        self.content_layout.setSpacing(15)
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.content_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("background-color: transparent;")
        
        self.main_layout.addWidget(scroll_area)
            
        self.setLayout(self.main_layout)
    
    def add_available_classes(self):
        database_manager : DatabaseManager = QApplication.instance().property("DatabaseManager")(path("/data/gym.sqlite"))

        # For each available class in the database.
        for available_class in database_manager.get_all_classes():
            self.content_layout.addWidget(ClassWidget(self, available_class))
        
class ClassWidget(QWidget):
    def __init__(self, parent: QWidget, available_class: AvailableClass) -> None:
        """A subclass of QWidget, used to display an available class in the content widget.
        
        Args:
            parent (QWidget): Parent of the class widget.
        """
        super().__init__(parent)
        self.available_class = available_class
        
        self._set_design()
        self._set_widgets()
        self._set_layout()
    
    def _set_design(self):
        """A function to set the design of a class widget."""
        self.setFixedSize(self.parentWidget().width() - 10, 100)
        
        # Get the classes image and set it as the background.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setPixmap(
            QPixmap(
                path("/assets/panels/class.png")
            ).scaled(
                self.background_label.size(),
                aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                mode = Qt.TransformationMode.SmoothTransformation
            )
        )
    
    def _set_widgets(self):
        """A function to set the widgets inside a class widget."""
        self.title_label = self.TextLabel(self, self.available_class.title)
        
        # Set the font of the title to bold.
        self.title_label.setFont(self.title_label.font_manager.geist.bold)
        title_font = self.title_label.font()
        title_font.setPointSize(15)
        self.title_label.setFont(title_font)
        
        self.description_label = self.TextLabel(self, self.available_class.description)
        self.start_date_label = self.TextLabel(self, str(self.available_class.start_date))
        self.tutor_profile_label = self.TutorProfile(self, self.available_class.tutor_id)
        
    def _set_layout(self):
        """A function to set the layout of a class widget."""
        self.main_layout = QVBoxLayout()
        
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.start_date_label)
    
        self.setLayout(self.main_layout)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Function called when a class is clicked."""
        if event.button() == Qt.MouseButton.LeftButton:
            main_window = get_property("MainWindow")
            main_window.show_class_window(self.available_class)
        
        return super().mousePressEvent(event)
    
    class TextLabel(QLabel):
        def __init__(self, parent: QWidget, text: str) -> None:
            """Base class for a text label within the class widget.

            Args:
                parent (QWidget): Parent of the text label, the class widget.
                text (str): Text to assign to the label.
            """
            super().__init__(parent, text = text)
            self.font_manager : FontManager = get_property("FontManager")
            
            self._set_design()
            
        def _set_design(self):
            font = self.font_manager.geist.regular
            
            self.setFont(font)
    
    class TutorProfile(QWidget):
        def __init__(self, parent: QWidget, tutor_id: int):
            super().__init__(parent)
            self.tutor = self.get_tutor_member(tutor_id)
        
            self._set_widgets()
            self._set_layout()
            
            # Set size again for any changes.
            self._set_design()
        
        def get_tutor_member(self, tutor_id: int) -> Member:
            database_manager : DatabaseManager = get_property("DatabaseManager")(path("/data/gym.sqlite"))
            return database_manager.get_member(id = tutor_id)
        
        def _set_design(self):
            self.setFixedSize(self.sizeHint())
            
            # Move to right side.
            self.move(
                self.parentWidget().width() - self.width() - 10,
                (self.parentWidget().height() / 2) - (self.height() / 2)
            )
        
        def _set_widgets(self):
            self.tutor_image = self.Image(self, self.tutor)
            self.tutor_name = self.Name(self, self.tutor)
        
        def _set_layout(self):
            self.main_layout = QVBoxLayout()
            self.main_layout.setSpacing(0)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.main_layout.addWidget(self.tutor_image, alignment = Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(self.tutor_name, alignment = Qt.AlignmentFlag.AlignCenter)
            
            self.setLayout(self.main_layout)
        
        class Name(QLabel):
            def __init__(self, parent: QWidget, tutor: Member):
                super().__init__(parent)
                self.tutor = tutor
                
                self.setFixedHeight(25)
                
                self.setText(f"{self.tutor.forename} {self.tutor.surname}")
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        class Image(QLabel):
            def __init__(self, parent: QWidget, tutor: Member):
                super().__init__(parent)
                self.tutor = tutor
                
                self._set_design()
                
            def _set_design(self):
                self.setFixedSize(50, 50)
                
                self.setPixmap(
                    QPixmap(
                        path(f"/assets/profiles/{self.tutor.profile}")
                    ).scaled(
                        self.size(),
                        aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                        mode = Qt.TransformationMode.SmoothTransformation
                    )
                )
                
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)