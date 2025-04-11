from src.shared.imports import *

# Local imports.
from src.windows.widgets.topbar_widget import TopBarWidget

class GymWindow(QWidget):
    def __init__(self, parent: QWidget) -> None:
        """A QWidget object to act as the gym window once the user logs in.

        Args:
            parent (QWidget): Parent of the gym window, typically the main window.
        """
        super().__init__(parent)
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
    
        self._set_design()
        self._set_widgets()
        
        # Show the window.
        self.show()
        
    def _set_design(self):
        """A function to set the design of the gym window."""
        self.setFixedSize(self.parentWidget().size()) # Fill main window.
        
        # Set background.
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
        """A function to load the neccesary widgets into the gym window."""
        self.top_bar = TopBarWidget(self) # Top bar.